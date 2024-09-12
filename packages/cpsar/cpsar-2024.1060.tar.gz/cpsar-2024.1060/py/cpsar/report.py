import csv
import sys
from six import StringIO
import time

import cpsar.pg
from cpsar.sales import filter_group_numbers
import cpsar.runtime as R
import cpsar.wsgirun as W

__metaclass__ = type

class WSGIReport:
    """ I want to have something more composable, but this is
    written to provide interface compatability with the old CGI
    report class.
    """
    label = 'Generic Report'
    summary = ''
    description = 'This query does not have a description'
    display_errors = False

    sql = None
    expanded_sql = None
    confirm = False

    csv_exportable = True
    csv_file_name = "records.csv"

    sql_tmpl_file = 'query_show_sql.tmpl'
    confirm_tmpl_file = 'query_confirm.tmpl'
    form_tmpl_file = 'query_form.tmpl'

    params = []
    form_resources = """
    <link rel='stylesheet' type='text/css'
          href='/repo/css/kcontrol/calendar.css' />
    <link rel='stylesheet' type='text/css'
          href='/css/report.css' />
    <script language='JavaScript' type='text/javascript' 
            src='/repo/js/kcontrol/calendar.js'></script>
    <script language='JavaScript' type='text/javascript' 
            src='/repo/js/kcontrol/lang/calendar-en.js'></script>
    <script language='JavaScript' type='text/javascript' 
            src='/repo/js/kcontrol/calendar-setup.js'></script>
    """

    debug = False

    csv_export = False
    query_css = ""

    ###########################################################################
    ## WSGI INTERFACE
    def wsgi(self):
        return W.wsgi(self.app)

    def app(self, req, res):
        self.req = req
        self.res = res

        self.form_params()
        if not req.get('_q_submit'):
            self.html_form()
        elif req.get('_q_csv'):
            self.csv_export = True
            self.csv()
        else:
            self.run()

    ###########################################################################
    ## Interfaced used by mako templates to show forms and reports

    @property
    def script_name(self):
        return self.req.script_name

    legend_items = []
    def legend(self):
        if not self.legend_items:
            return ""

        buf = StringIO()
        buf.write("""
        <table border="1" align="center">
        <tr>
            <th colspan="2">Legend</th>
        </tr>""")
        for cap, val in self.legend_items:
            buf.write("<tr><td>%s</td><td>%s</td></tr>" % (cap, val))
        buf.seek(0)
        return buf.getvalue()

    def group_header(self):
        return ", ".join("%s: %s" % (c['group_number'], c['client_name'])
                for c in self.get_clients())

    ###########################################################################
    ## REPORT INTERFACE

    def form_params(self):
        pass

    def confirm_form(self):
        mako = W.MakoRecord(self.req, self.res,
                            tmpl_name=self.confirm_tmpl_file)
        mako['q'] = self
        mako()

    def html_form(self):
        mako = W.MakoRecord(self.req, self.res, tmpl_name=self.form_tmpl_file)
        mako['q'] = self
        mako()

    def query_args(self):
        args = {}
        for v in self.params:
            key = v[1].name
            if self.req.get(key):
                args[key] = cpsar.pg.qstr(str(self.req.get(key)))
            else:
                args[key] = None
        gn = self.client_requested_group_numbers()
        if not gn:
            self.group_number = None
            args['gn_frag'] = ' IS NOT NULL'
        elif len(gn) == 1:
            self.group_number = gn[0]
            args['gn_frag'] = '= %s' % cpsar.pg.qstr(self.group_number)
        else:
            self.group_number = filter_group_numbers(gn)
            args['gn_frag'] = 'IN (%s)' % ", ".join(cpsar.pg.qstr(c) for c in
                                                    self.group_number)
        return args

    def client_requested_group_numbers(self):
        """ Provide a list of group numbers requested by the user, taking
        into consideration report codes.
        """
        report_code = self.req.get('report_code')
        if report_code:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT group_number
                FROM client_report_code
                WHERE report_code=%s
                """, (report_code,))
            gn = [c for c, in cursor]
        else:
            gn = []
        gn.extend(filter(None, self.req.params.getall('group_number')))
        return gn

    def record_fields(self):
        try:
            return [c[0] for c in self.cursor.description]
        except TypeError:
            return []

    def records(self):
        """ If you override records and you do not set self.cursor to be a
        database cursor that will have the fields on the report, then you must
        also override record_fields and return back a list of field names 
        to use on the report, unless you have your own display mako template
        in which case record_fields is never used.
        """
        self.cursor = R.db.cursor()
        self.expanded_sql = self.sql % self.query_args()
        self.cursor.execute(self.expanded_sql)
        return self.cursor

    def preamble(self):
        return None

    def validate_form_input(self):
        """ Ensure that the given paramaters are provided. """
        for caption, ctrl in self.params:
            if getattr(ctrl, 'required', False):
                if not self.req.params.get(ctrl.name):
                    R.error("Missing required %s" % caption)

    def run(self):
        self.validate_form_input()
        if R.get_errors():
            self.html_form()
            return

        mako = self._mako_record()
        if R.get_errors():
            self.html_form()
        else:
            mako()

    def _mako_record(self):
        mako = W.MakoRecord(self.req, self.res, tmpl_name=self.sql_tmpl_file)
        mako.update({
            'q': self,
            'cursor' : self.records(),
            'sql' : self.expanded_sql})
        return mako

    def csv(self):
        self.res.content_type = 'text/csv'

        h = self.res.headers
        h.add("Expires", "0")
        h.add("Content-Transfer-Encoding", "binary")
        h.add("Pragma", "public")
        h.add("Content-Disposition", "attachment; filename=%s" %
                                     self.csv_file_name)
        cursor = self.records()
        writer = csv.writer(self.res)
        preamble = self.preamble()
        if preamble is not None:
            writer.writerow(preamble)
        writer.writerow(self.record_fields())
        for rec in cursor:
            writer.writerow(rec)

    ###########################################################################
    ## Utility
    def print_params(self):
        p = []
        for key, value in self.req.params.items():
            if value and not key.startswith('_q'):
                p.append("%s: %s" % (key, value))
        return " ".join(p)

    def get_clients(self):
        cursor = R.db.dict_cursor()
        gn = self.fs.getvalue('group_number', [])
        if not isinstance(gn, list):
            gn = [gn]
        gn = filter_group_numbers(gn)
        clients = []
        for number in gn:
            cursor.execute("""
                SELECT *
                FROM client
                WHERE group_number=%s""", (number,))
            clients.append(cursor.fetchone())
        return clients

