#!/usr/bin/env python
import cpsar.ajson as json
import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    @property
    def group_number(self):
        return self.fs.getvalue('group_number')

    @property
    def report_code(self):
        return self.fs.getvalue('report_code')

    def main(self):
        if self.group_number:
            adjusters = self._adjusters_by_group_number()
        elif self.report_code:
            adjusters = self._adjusters_by_report_code()
        else:
            adjusters = []
        self._res.content_type = 'application/json'
        self._res.write(json.write(adjusters))

    def _adjusters_by_group_number(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT email, first_name, last_name, initials
            FROM user_info
            WHERE group_number = %s
            ORDER BY last_name, first_name
            """, (self.group_number,))
        return list(map(dict, cursor))

    def _adjusters_by_report_code(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT email, first_name, last_name, initials
            FROM user_info
            JOIN client_report_code USING(group_number)
            WHERE report_code = %s
            ORDER BY last_name, first_name
            """, (self.report_code,))
        return list(map(dict, cursor))

application = Program.app
