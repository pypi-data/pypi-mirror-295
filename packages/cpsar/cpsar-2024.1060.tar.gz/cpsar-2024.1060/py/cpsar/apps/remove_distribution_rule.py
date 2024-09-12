import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    """ Management of Client Record - Remove distribution rule from the
    given client. """

    def main(self):
        dr_id = self.fs.getvalue('dr_id')
        if not dr_id:
            raise W.HTTPNotFound()
        
        cursor = R.db.dict_cursor()
        cursor.execute("""
            delete from distribution_rule
            where dr_id = %s
            returning group_number, distribution_account, tx_type, percent,
                      amount
            """, (dr_id,))
        if not cursor.rowcount:
            raise W.HTTPNotFound()
        
        rec = cursor.fetchone()
        if rec['amount']:
            R.log.info('Removed fixed amount distribution rule '
                'from %(group_number)s: %(tx_type)s, '
                '%(distribution_account)s for %(amount)s' % rec)
        elif rec['percent']:
            R.log.info('Removed percentage distribution rule '
                'from %(group_number)s: %(tx_type)s, '
                '%(distribution_account)s for %(percent)s' % rec)
        R.db.commit()
        R.flash("Distribution rule removed successfully")
        self._res.redirect("/view_client?group_number=%s", rec['group_number'])

application = Program.app
