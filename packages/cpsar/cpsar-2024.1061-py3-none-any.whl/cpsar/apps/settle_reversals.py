import cpsar.pg
import cpsar.runtime as R
import cpsar.ws as W

class Program(W.MakoProgram):
    messages = {
        'd' : 'Reversals settled'
    }

    def main(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans.group_number,
                   client.client_name,
                   SUM(pending_reversal_settlement.amount) as total,
                   COUNT(*) as cnt
            FROM trans
            JOIN reversal USING(trans_id)
            JOIN pending_reversal_settlement USING(reversal_id)
            JOIN client ON client.group_number = trans.group_number
            GROUP BY trans.group_number, client.client_name
            ORDER BY trans.group_number
        """)
        self.group_reversals = cpsar.pg.all(cursor)

        self.group_number = self.fs.getvalue('group_number')
        cursor.execute("""
            SELECT trans.group_number,
                    client.client_name,
                   SUM(pending_reversal_settlement.amount) as total,
                   COUNT(*) as cnt
            FROM trans
            JOIN reversal USING(trans_id)
            JOIN pending_reversal_settlement USING(reversal_id)
            JOIN client ON
                client.group_number = trans.group_number AND
                client.group_number = %s
            GROUP BY trans.group_number, client.client_name
        """, (self.group_number,))
        self.group = cpsar.pg.one(cursor)

        if self.group_number:
            cursor.execute("""
                SELECT trans.trans_id,
                       pending_reversal_settlement.amount,
                       patient.first_name || ' ' || patient.last_name AS name,
                       drug.name AS drug,
                       pending_reversal_settlement.entry_date,
                       pending_reversal_settlement.prs_id
                FROM trans
                JOIN reversal USING(trans_id)
                JOIN drug USING(drug_id)
                JOIN patient USING(patient_id)
                JOIN pending_reversal_settlement USING(reversal_id)
                WHERE trans.group_number = %s 
                ORDER BY trans.trans_id
                """, (self.group_number,))
            self.reversals = cpsar.pg.all(cursor)
        else:
            self.reversals = None

application = Program.app
