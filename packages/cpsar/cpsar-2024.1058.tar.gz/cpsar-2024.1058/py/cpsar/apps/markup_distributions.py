from decimal import Decimal, InvalidOperation
import cpsar.runtime as R
import cpsar.util as U
import cpsar.ws as W

class Program(W.PIMixIn, W.GProgram):
    @W.publish
    def add(self):
        account = self.fs.getvalue('account')
        if not account:
            R.flash("No account given")
            return self.redir()
        gn = self.fs.getvalue("group_number")
        if not gn:
            R.flash("no group")
            return self.redir()
        percent = self.fs.getvalue("percent", "")
        try:
            percent = Decimal(percent)
        except InvalidOperation:
            R.flash("invalid percent %s", percent)
            return self.redir()
        tx_type = self.fs.getvalue("tx_type")
        if not tx_type:
            R.flash("no tx type")
            self.redir()

        sql = U.insert_sql("distribution_on_markup", 
            {"tx_type": tx_type,
             "group_number": gn,
             "percent": percent,
             "account": account})
        cursor = R.db.cursor()
        cursor.execute(sql)
        R.db.commit()
        R.flash("Markup-based Distribution Rule Added")
        self.redir()
    
    def redir(self):
        gn = self.fs.getvalue("group_number")
        if not gn:
            self.redirect("/")
        else:
            self.redirect("/view_client?group_number=%s", gn)

    @W.publish
    def delete(self):
        comu_id = self.fs.getvalue("comu_id")
        cursor = R.db.cursor()
        cursor.execute("""
          delete from distribution_on_markup where comu_id=%s
          returning group_number
          """, (comu_id,))
        if not cursor.rowcount:
            R.flash("Rule not found")
            self.redirect("/")
        group_number, = cursor.fetchone()
        R.db.commit()
        R.flash("Rule deleted")
        self.redirect("/view_client?group_number=%s", group_number)

application = Program.app
