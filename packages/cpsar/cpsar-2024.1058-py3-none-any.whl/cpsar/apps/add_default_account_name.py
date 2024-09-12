import logging
import os

import cpsar.controls as C
import cpsar.runtime as R
import cpsar.ws as W

log = None

class Program(W.GProgram):
    def main(self):
        fs = self.fs
        group_number = fs.getvalue('group_number')
        tx_type = fs.getvalue('tx_type')
        account = fs.getvalue('default_account')

        if not group_number:
            R.error('Missing group number')
        if not tx_type:
            R.error('Missing TX Type')
        if not account:
            R.error("Missing account")

        # Bomb out
        if R.has_errors():
            for e in R.get_errors():
                self._res.error(e)
            return

        cursor = R.db.cursor()
        cursor.execute("""
            insert into client_default_account_name (
                group_number,
                tx_type,
                default_account)
            values (%s, %s, %s)
            on conflict(group_number, tx_type) do update set
                default_account=EXCLUDED.default_account
            """, (group_number, tx_type, account))

        msg = 'Added Default Account  %s:%s -> %s' % (
                group_number, tx_type, account)
        R.log.info(msg)
        R.flash(msg)
        R.db.commit()
        self._res.redirect('/view_client?group_number=%s', group_number)

application = Program.app
