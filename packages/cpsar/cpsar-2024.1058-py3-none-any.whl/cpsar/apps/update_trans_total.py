import decimal
from cpsar import ajson as json
from cpsar.runtime import db
import cpsar.runtime as R
from cpsar import txlib
from cpsar import ws

class Program(ws.GProgram):
    def main(self):
        fs = self.fs
        trans_id = fs.getvalue('trans_id')
        cursor = db.cursor()
        cursor.execute("""
            select  balance, total
            from trans
            where trans_id=%s
            """, (trans_id,))
        if not cursor.rowcount:
            return self._reply("trans not found")
        existing_balance, existing_total = next(cursor)
        if existing_balance != existing_total:
            return self._reply("cannot change transaction when total != balance")
        total = self.decimal_value("total")
        cost_allowed = self.decimal_value("cost_allowed")
        dispense_fee = self.decimal_value("dispense_fee")
        processing_fee = self.decimal_value("processing_fee")

        difference = total - existing_total
        if difference == 0:
            return self._reply("total not changed")

        cursor.execute("""
            update trans set total = %s, cost_allowed = %s, dispense_fee = %s,
                processing_fee = %s, balance=%s
            where trans_id = %s
            """, (total, cost_allowed, dispense_fee, processing_fee, total, trans_id))


        cursor.execute("""
            insert into distribution (trans_id, distribution_account, amount)
            values (%s, %s, %s)
            """, (trans_id, 'cps', difference))
        msg = 'Transaction total fixed from %s to %s' % (existing_total, total)
        cursor.execute("""
            insert into trans_log (trans_id, message, username)
            values (%s, %s, %s)
            """, (trans_id, msg, R.username()))
        txlib.check(trans_id)
        db.commit()
        lb = self.fs.getvalue('linkback')
        if lb:
            self.redirect(lb)
        else:
            self._reply()

    def _reply(self, *errs):
        self._res.content_type = 'application/json'
        self._res.write(json.write({'errors': list(errs)}))


    def decimal_value(self, field):
        f = self.fs.getvalue(field, '').strip()
        if not f:
            return decimal.Decimal("0")
        try:
            return decimal.Decimal(f)
        except decimal.InvalidOperation:
            return decimal.Decimal("0")

application = Program.app
