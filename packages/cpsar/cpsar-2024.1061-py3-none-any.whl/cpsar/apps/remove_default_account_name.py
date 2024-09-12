import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):

    def main(self):
        fs = self.fs
        group_number = fs.getvalue('group_number')
        tx_type = fs.getvalue('tx_type')

        if not group_number and not tx_type:
            self._res.error('no id')
            return

        cursor = R.db.cursor()
        cursor.execute("""
            delete from
            client_default_account_name
            where group_number=%s and tx_type=%s
            returning default_account
            """, (group_number, tx_type))

        if not cursor.rowcount:
            self._res.error('')
            self._res.redirect("/view_client?group_number=%s", group_number)

        account, = next(cursor)
        msg = 'Removed default account %s:%s -> %s' % (group_number, tx_type, account)
        R.log.info(msg)
        R.flash(msg)
        R.db.commit()
        self._res.redirect("/view_client?group_number=%s", group_number)

application = Program.app
