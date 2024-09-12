import cpsar.runtime as R
import cpsar.util as U
import cpsar.ws as W

from cpsar import txlib

class Program(W.GProgram):
    """ Create negative distribution records
    """
    def main(self):
        fs = self.fs
        trans_id = fs.getvalue('trans_id')

        cursor = R.db.cursor()
        cursor.execute("""
            insert into distribution (trans_id, distribution_account, amount, referring_pharmacy)
            select trans_id, distribution_account, amount * -1, referring_pharmacy
            from distribution
            where trans_id=%s
            """, (trans_id,))
        R.flash("Reverse distributions created")
        R.db.commit()
        self.redirect("/view_trans?trans_id=%s" % trans_id)

application = Program.app



