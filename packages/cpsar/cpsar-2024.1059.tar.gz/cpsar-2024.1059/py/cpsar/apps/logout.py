import cpsar.runtime as R
import cpsar.ws as W

from cpsar import pg

class Program(W.MakoProgram):
    authentication_required = False

    def main(self):
        try:
            del R.session['username']
            R.session.save()
        except KeyError:
            pass
        self.redirect("/login")

application = Program.app
