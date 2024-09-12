import cpsar.runtime as R
import cpsar.ws as W

from cpsar import pg

class Program(W.HTTPMethodMixIn, W.MakoProgram):
    authentication_required = False

    def do_post(self):
        username = self._req.params.get('username')
        password = self._req.params.get('password')
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM user_info
            WHERE username=%s
              AND password=%s
              AND accounting_flag = true
            """, (username.lower(), password))
        if cursor.fetchone()[0] == 0:
            R.error("Login failed")
            return

        R.session['username'] = username
        R.session.save()
        self.redirect("/")

application = Program.app
