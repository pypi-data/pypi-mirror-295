#!/usr/bin/env python
import cpsar.runtime as R
import cpsar.ws as W
from cpsar import pg
from cpsar import util

class Program(W.HTTPMethodMixIn, W.MakoProgram):

    @property
    def clone(self):
        return self.fs.getvalue('clone')

    def do_post(self):
        group_number = self.fs.getvalue('group_number')
        if not group_number:
            R.error('Missing Group Number')
        client_name = self.fs.getvalue('client_name')
        if not client_name:
            R.error('Missing Client Name')

        if R.has_errors():
            return

        if self.clone:
            sql = """
                create temp table c as
                   select *
                   from client
                   where group_number=%(clone)s;
                update c set group_number=%(group_number)s,
                             client_name=%(client_name)s;
                insert into client select * from c;
                drop table c;

                create temp table c as
                    select *
                    from distribution_rule
                    where group_number=%(clone)s;
                insert into distribution_rule (group_number,
                    tx_type, distribution_account, amount, percent,
                    show_on_invoice, min_cost, max_cost)
                  select
                    %(group_number)s,
                    tx_type,
                    distribution_account,
                    amount,
                    percent,
                    show_on_invoice,
                    min_cost,
                    max_cost
                  from c;
                  drop table c;

                create temp table c as
                    select *
                    from distribution_on_markup
                    where group_number=%(clone)s;
                insert into distribution_on_markup (
                    tx_type, group_number, percent, account)
                select tx_type, %(group_number)s, percent, account from c;
                drop table c;

                create temp table c as
                    select *
                    from payment_type
                    where group_number=%(clone)s;
                insert into payment_type (
                    group_number, type_name, default_ref_no, expiration_date)
                  select %(group_number)s, type_name, default_ref_no, expiration_date
                  from c;
                drop table c;

                create temp table c as
                    select *
                    from client_dispense_fee_rule
                    where group_number=%(clone)s;
                insert into client_dispense_fee_rule (
                    group_number, tx_type, amount)
                  select %(group_number)s, tx_type, amount
                  from c;
                drop table c;

                create temp table c as
                    select *
                    from client_bill_rule
                    where group_number=%(clone)s;
                insert into client_bill_rule (
                    group_number, tx_type, rule_type, amount)
                  select %(group_number)s, tx_type, rule_type, amount
                  from c;
                drop table c;

                create temp table c as
                    select *
                    from client_report_code
                    where group_number=%(clone)s;
                insert into client_report_code (
                   group_number, report_code, internal)
                  select %(group_number)s, report_code, internal
                  from c;
                drop table c;
                """ % pg.qstr({'clone': self.clone,
                               'group_number': group_number,
                               'client_name': client_name})
        else:
            sql = util.insert_sql('client', {
                'group_number': group_number,
                'client_name': client_name})

        cursor = R.db.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            R.error(e)
            return

        R.db.commit()
        self.redirect('/view_client?group_number=%s&refresh=1',
                      self.fs.getvalue('group_number'))

application = Program.app
