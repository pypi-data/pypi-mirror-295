""" Get in the zone """
import cpsar.runtime as R
import cpsar.ws as W

from cpsar import pg

class Program(W.MakoProgram):
    def flagged_tx(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_log.*
            FROM trans_log
            WHERE trans_log.flagged = TRUE
            """)
        return pg.all(cursor)

    def recent_batches(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT *
            FROM batch_file
            order by batch_file_id DESC
            LIMIT 100
            """)
        return pg.all(cursor)

    def main(self):
        if self.fs.getvalue('blowup') == 'true':
            raise ValueError('boom')

application = Program.app
