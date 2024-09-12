import datetime

import cpsar.scsaflib as CS
import cpsar.ws as W
import cpsar.runtime as R

class Program(W.GProgram):
    def main(self):
        e = CS.RebillEDIWriter(datetime.datetime.now())
        try:
            e.create_file()
        except CS.NoTransactionsError:
            self._res.error("Nothing to do")
            return

        if e.send_status:
            self._res.write('<p>An error occured: %s. Try again.</p>' % e.send_status)
        else:
            self._res.write('<p>File successfully sent to server</p>')
            e.reset_rebill()
            R.db.commit()

application = Program.app
