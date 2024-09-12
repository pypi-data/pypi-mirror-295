import cpsar.pg
import cpsar.runtime as R
import cpsar.ws as W

class Program(W.MakoProgram):
    def main(self):
        cursor = R.db.dict_cursor()

        self.filter_user = self.fs.getvalue('user')
        if self.filter_user:
            cond = 'username = %s' % cpsar.pg.qstr(self.filter_user)
        else:
            cond = 'True'
        cursor.execute("""
            SELECT entry_date, trans_id, username, COUNT(*) AS msg_cnt
            FROM trans_log
            WHERE entry_date > 'today' AND %s AND username <> 'jeremy'
            GROUP BY entry_date, trans_id, username
            ORDER BY entry_date DESC
            LIMIT 1000
            """ % cond)
        self.recent_log = cpsar.pg.all(cursor)
        cursor.execute("""
            SELECT username, COUNT(*) as cnt
            FROM trans_log
            WHERE entry_date::date = NOW()::date
            GROUP BY username
            ORDER BY username
            """)
        self.log_users = cpsar.pg.all(cursor)

application = Program.app
