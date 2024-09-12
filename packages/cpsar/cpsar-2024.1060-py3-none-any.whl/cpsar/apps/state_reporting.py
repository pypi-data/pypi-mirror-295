# -*- coding: utf-8 -*-
""" State Reporting System Bill Import Program

This is a program that create state report files, bills and entries
from trans and reversal records in the system.

The system works off of a flag that is stored on transaction and
reversal records. If the sr_mark flag can be in 3 states.

 '' - Do not send for state reporting.
 'Y' - The next time a file is sent, send this transaction
 'H' - Hold the transaction. Show it on the transaction listing on 
       the state reporting page, but do not send it when we click
       send.

When a file is created to be sent, a state_reporting_entry record is made for
each transaction, creating a state reporting id (srid).

The srid is used for the bill number and is subsequently submitted on
replacements/voids.

Reversals will pull the highest srid for the transaction linked to the reversal
to send in as a void.
"""
import csv
import datetime
import paramiko
import tempfile

from cpsar import db
from cpsar import ws
from cpsar.sr import conduent
from cpsar.sr import bishop
import cpsar.runtime as R

class Program(ws.PIMixIn, ws.MakoProgram):
    # template data
    def pending_trans_count(self):
        c = mcursor()
        c.pending_trans_count()
        return next(c)[0]

    def pending_reversal_count(self):
        c = mcursor()
        c.pending_reversal_trans_count()
        return next(c)[0]

    def pending_trans(self):
        cursor = mdict_cursor()
        cursor.pending_trans()
        return list(cursor)

    def pending_reversals(self):
        cursor = mdict_cursor()
        cursor.pending_reversals()
        return list(cursor)


    # handlers

    @ws.publish
    def file(self):
        fname = self.fs.getvalue("fname")
        if not fname:
            return

        cursor = db.cursor()
        cursor.execute("""
            select contents
            from state_report_file
            where file_name = %s
              and contents is not null
        """, (fname,))
        if not cursor.rowcount:
            return

        self.mako_auto_publish = False
        contents = cursor.fetchone()[0]
        if contents is None:
            self._res.write("Empty File Contents for %s<br />" % fname)
            return
        self._res.content_type = 'application/csv'
        self._res.headers['Content-Disposition'] = 'attachment;filename=%s' % str(fname)
        self._res.write(str(contents))

    @ws.publish
    def unmark(self):
        try:
            trans_id = int(self.fs.getvalue('trans_id'))
        except (ValueError, TypeError):
            return
        c = mcursor()
        c.unmark_trans(trans_id)
        db.commit()
        self._send_ok()

    @ws.publish
    def set_hold(self):
        try:
            trans_id = int(self.fs.getvalue('trans_id'))
        except (ValueError, TypeError):
            trans_id = None
        try:
            reversal_id = int(self.fs.getvalue('reversal_id'))
        except (ValueError, TypeError):
            reversal_id = None
        hold = 'H' if self.fs.getvalue('hold') == '1' else 'Y'
        cursor = db.cursor()
        if trans_id:
            cursor.execute("""
                update trans set sr_mark=%s
                where trans_id=%s
                """, (hold, trans_id))
        if reversal_id:
            cursor.execute("""
                update reversal set sr_mark=%s
                where reversal_id=%s
                """, (hold, reversal_id))
        db.commit()
        self._send_ok()

    @ws.publish
    def update_trans(self):
        try:
            trans_id = int(self.fs.getvalue('trans_id'))
        except (ValueError, TypeError):
            return
        mark = self.fs.getvalue('sr_mark', '')
        if mark not in ('', 'H', 'Y'):
            mark = ''

        control_number = self.fs.getvalue('sr_control_number', '').strip()
        if not control_number:
            control_number = None
        claim_freq = self.fs.getvalue('sr_claim_freq_type_code', '')
        try:
            int(claim_freq)
        except ValueError:
            claim_freq = None

        cursor = db.cursor()
        cursor.execute("""
            update trans set sr_mark=%s, sr_control_number=%s, sr_claim_freq_type_code=%s
            where trans_id=%s
            """, (mark, control_number, claim_freq, trans_id))

        cursor.execute("""
            select reversal_id from reversal where trans_id=%s
            """, (trans_id,))
        if cursor.rowcount:
            reversal_id, = next(cursor)
            if reversal_id:
                reversal_mark = self.fs.getvalue('sr_reversal_mark', '')
                if mark not in ('', 'H', 'Y'):
                    mark = ''
                cursor.execute("""
                    update reversal set sr_mark = %s
                    where reversal_id =%s
                    """, (reversal_mark, reversal_id))

        db.commit()
        R.flash("State reporting values updated")
        self.redirect("/view_trans?trans_id=%s", trans_id)

    @ws.publish
    def load_new_pending(self):
        cursor = mcursor()
        cursor.load_new_pending()
        db.commit()
        self.redirect('/state_reporting')

    @ws.publish
    def reset_pending(self):
        cursor = mcursor()
        cursor.reset_pending()
        db.commit()
        self.redirect('/state_reporting')

    @ws.publish
    def save(self):
        """ Save the selected transactions into state report files, bills, and
        entries. Reporting is done later from the files menu. This handler
        takes all of the selected transactions, creates one
        file for them, and then multiple bills, each bill has 1 line.
        """
        status_flag = self.fs.getvalue('status_flag')
        if status_flag not in ('T', 'P'):
            R.error("No status flag mode selected. Test or Production")
            return

        ctime = datetime.datetime.now()
        file_name = "CPS_%s%s_0001.bbr" % (
            ctime.strftime("%Y%m%d%H%M%S"),
            ctime.microsecond / 1000)
        cur = mdict_cursor()
        cur.execute("""
            select SUM(cnt) FROM (
            select count(*) as cnt from trans where sr_mark = 'Y'
            union
            select count(*) from reversal where sr_mark = 'Y'
            ) as t""")
        if next(cur)[0] == 0:
            self.redirect("/state_reporting")
            return

        sr_file_id = self.fs.getvalue('sr_file_id')
        if sr_file_id:
            try:
                sr_file_id = int(sr_file_id)
            except ValueError:
                R.error("sr_file_id must be an integer")
                return
            cur.execute("""
                select count(*) from state_report_file
                where sr_file_id=%s
                """, (sr_file_id,))
            if not cur.rowcount:
                R.error("File ID %s not found" % sr_file_id)
                return
        else:
            cur.create_sr_file(file_name, status_flag, R.username())
            sr_file_id = next(cur)[0]

        bill_group = self.fs.getvalue('bill_group')
        if bill_group not in ('B', 'O'):
            R.error("Invalid bill group %r" % bill_group)
            return

        try:
            if bill_group == 'B':
                cur.save_on_one_bill(sr_file_id, R.username())
            else:
                cur.save_on_own_bill(sr_file_id, R.username())
        finally:
            with open("/tmp/debug.sql", "wt") as fd:
                fd.write(cur._last_executed_sql)

        link = "/sr_manual/report_file?sr_file_id=%s" % sr_file_id
        db.commit()
        self.redirect(link)

    def _send_to_browser(self, csv_data, file_name):
        self.mako_auto_publish = False
        self._res.content_type = 'text/csv'
        self._res.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name
        self._res.write(csv_data)

    def _send_to_sftp(self, csv_data, file_name, target, status_flag):
        target_map = {
            'bishop': dict(
                host = 'sftp.bishopht.com',
                port = 22,
                username='ftpCPS',
                password='!931I$Gr8t!',
                prod_path = 'Inbound/%s' % file_name,
                test_path = 'Inbound/Test/%s' % file_name,
                )}
        dest = target_map[target]
        if status_flag == 'T':
            target_path = dest['test_path']
        else:
            target_path = dest['prod_path']
        t = paramiko.Transport((dest['host'], dest['port']))
        t.connect(username=dest['username'], password=dest['password'])
        sftp = paramiko.SFTPClient.from_transport(t)
        f = tempfile.NamedTemporaryFile("a+t")
        try:
            f.write(csv_data)
            f.flush()
            sftp.put(f.name, target_path)
        finally:
            t.close()
            f.close()

    def _send_ok(self):
        self.mako_auto_publish = False
        self._res.content_type = 'text/plain'
        self._res.write('OK')

def mcursor():
    return db.mako_cursor('ar/state_reporting.sql')

def mdict_cursor():
    return db.mako_dict_cursor('ar/state_reporting.sql')

application = Program.app
