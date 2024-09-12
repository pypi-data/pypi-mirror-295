import decimal

import cpsar.runtime as R
import cpsar.txlib
import cpsar.util as U
import cpsar.ws as W

class Program(W.GProgram):
    """ Write off an amount from a transaction
    """
    def main(self):
        fs = self.fs
        trans_id = fs.getvalue('trans_id')
        try:
            amount = U.parse_currency(fs.getvalue('amount', ''))
        except U.ParseError as e:
            return self._res.error(e)
        account = fs.getvalue('distribution_account')
        cpsar.txlib.add_distribution(trans_id, account, amount)
        if R.has_errors():
            R.flash(", ".join(R.get_errors()))
        else:
            R.db.commit()
            self._res.redirect('/view_trans?trans_id=%s', trans_id)

application = Program.app
