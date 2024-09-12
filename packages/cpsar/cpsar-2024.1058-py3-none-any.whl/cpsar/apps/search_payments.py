import cpsar.runtime as R
import cpsar.ws as W

class Program(W.MakoProgram):

    def client_values(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, group_number || ' ' || client_name
            FROM client
            ORDER BY group_number
            """)
        return [('', '')] + list(cursor)

    @property
    def ref_no(self):
        return self.fs.getvalue('ref_no')

    @property
    def group_number(self):
        return self.fs.getvalue('group_number')

    def main(self):
        if not self.ref_no:
            return self._res.redirect("/")

        cursor = R.db.dict_cursor()
        if self.group_number:
            cursor.execute("""
             CREATE TEMP TABLE group_constraint (group_number VARCHAR(8));
             INSERT INTO group_constraint VALUES(%s);
             """, (self.group_number,))
        else:
            cursor.execute("""
             CREATE TEMP TABLE group_constraint AS
             SELECT group_number FROM client
            """)

        cursor.execute("""
         CREATE TEMP TABLE search_results AS
            SELECT trans.trans_id,
                   trans.invoice_id,
                   trans.line_no,
                   trans_payment.entry_date,
                   trans_payment.amount,
                   payment_type.type_name,
                   trans_payment.ref_no,
                   FALSE AS overpayment
            FROM trans_payment
            JOIN trans USING(trans_id)
            JOIN group_constraint USING(group_number)
            JOIN payment_type USING(ptype_id)
            WHERE trans_payment.ref_no = %(ref_no)s
            UNION ALL
            SELECT trans.trans_id,
                   trans.invoice_id,
                   trans.line_no,
                   overpayment.entry_date,
                   overpayment.amount,
                   payment_type.type_name,
                   overpayment.ref_no,
                   TRUE AS overpayment
            FROM overpayment
            JOIN trans USING(trans_id)
            JOIN group_constraint USING(group_number)
            JOIN payment_type USING(ptype_id)
            WHERE overpayment.ref_no = %(ref_no)s
            """,  {'ref_no': self.ref_no})
        
        cursor.execute("SELECT * FROM search_results ORDER BY trans_id")
        self.results = list(cursor)

        cursor.execute("SELECT SUM(amount) AS s FROM search_results")
        self.total, = cursor.fetchone()

        cursor.execute("DROP TABLE search_results, group_constraint")

application = Program.app
