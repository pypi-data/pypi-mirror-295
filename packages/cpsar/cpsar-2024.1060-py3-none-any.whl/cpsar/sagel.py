#!/usr/bin/env python
"""
Sagel: Selector & Aggregator Library
====================================

Functional Specification
------------------------

Overview
~~~~~~~~
The selector & aggregator library (Sagel) is a python library to that computes
aggregate functions over table-oriented sets of data. I have written so many
reports over the years that had to have multiple total lines for different
kinds of data in the report. The more groupings you have, the harder the code
becomes. Some fancy databases have a grouping set clause that will do this
grouping for you. My database of choice, PostgreSQL, alas, does not. So this is
my attempt at reinventing that wheel and making SQL report writing in pure
Python suck less.

The top priorities of the library are:
 1.	Keep the interface dead simple to use, like being able to do something
    useful in 1 line of code.
 2.	Easily expandable, like registering new selectors and aggregators with
    simple functions.
 3. Performance. My reports sometimes have tens of thousands of rows. I can't
    sit here and wait for 30 minutes while the totals are getting calculated.
 4.	Produce enough meta data for other programs to do fancy, generalized things with the output.

Scenario
~~~~~~~~
Gonzo works for the government on the department of peanut butter and squash
regulation committee.  It's his job to write a report displaying the number of
peanut butter bars sold in Canada last year. They want the number of bars
broken down by month and province.

Gonzo, the Pythoneer, writes a SQL query in a simple python script using the
MySQLdb database module.  He uses sagel to break down the results of the query
into groupings by month and province showing each peanut butter bar sold, the
total number of peanut butter bars sold each month and the total number sold in
each province for each month::

    cursor = conn.cursor(MySQLdb.cursor.DictCursor)
    cursor.execute('''
        SELECT ship_date, ingredient, province, cost
        FROM peanut_butter_bars
        WHERE ship_date BETWEEN '20090101' AND '20091231'
        ''')
    grouper = sagel.grouper(
        (sagel.month("ship_date"), sagel.count()),
        (sagel.value("province"), sagel.sum("cost")))
    records = grouper(cursor)

Concepts
~~~~~~~~
The library is broken down into two general concepts: selectors and
aggregators.  Selectors are like the GROUP BY clause in SQL. The most common
selector by far is "value." The selector groups by the particular value of the
given field. So each unique value of the given field will have records put in
their own group. The other common selectors are for dates. Grouping by the year
and month is a common business use case. There are also some interesting
numeric selectors that could be written, like with ranges, but they aren't in
the scope of the original project.

The other concept is an aggregator. This is the function that is computed
across the records for a given grouping. We have the usual suspects from SQL
including COUNT, SUM, AVG, MAX and MIN.

Interface
~~~~~~~~~
sagel.grouper provides the main user interface to the library. It can be called
with a number of different configurations. The basic form is::

    grouper((selector, aggregator), ...)

Where each argument is a pair of a selector and an aggregator. Each selector
and aggregator can themselves be a tuple.::

    grouper(((selector1, selector2, selector3), (aggregator1, aggregator2)), 
             (selector4, aggregator3))

It is common to want to group by more than one field per level. What if Gonzo
wanted to also show  the capitol of the province with each grouping? He could
give them both as selectors. What if gonzo wanted to show the total cost as
well as the average cost? He could give them both as aggregators. What if gonzo
wanted to do all of that? He would have something like this::

    grouper = sagel.grouper(
        (sagel.month("ship_date"), sagel.count()),
        ((sagel.value("province") sagel.value("province_capitol")), 
             (sagel.sum("cost"), sagel.avg("cost"))))

Complex aggregates and selectors and make for some very ugly Lispy-looking code
(I've got my foil hat on. You can't hurt me Lisper!), so we've also got a way
to feed in a description of the aggregators in yaml.

    - select:
      - month("ship_date")
      aggregate:
      - count()
    - select:
      - "province"
      - "province_capitol"
     aggregate:
     - sum("cost")
     - avg("cost")

    GROUP count() BY month("ship_date")
    GROUP sum("cost"), avg("cost") BY "province", "province_capitol"
"""
from __future__ import print_function
from collections import OrderedDict
from pprint import pprint
import os

import cpsar.runtime as R

class aggregator:
    def __init__(self):
        self.agg_stack = []

    def add_level(self, selectors, aggregators):
        if not isinstance(selectors, tuple):
            selectors = (selectors,)
        if not isinstance(aggregators, tuple):
            aggregators = (aggregators,)
        self.agg_stack.append((selectors, aggregators))

    def transform(self, recordset, inc_detail=True):
        agg_result = OrderedDict()
        for rec in recordset:
            self._agg(self.agg_stack, agg_result, rec)
        return self._flatten(agg_result, inc_detail)

    def _agg(self, agg_stack, agg_result, rec):
        """ Work off a list of aggregators and selectors. more general than 
        original aggregate

        the selector determines the key in agg_result
        """
        #agg_field, sum_fields = agg_stack[0]
        selectors, aggregators = agg_stack[0]
        key = tuple(s.compute_key(rec) for s in selectors)

        try:
            agrec = agg_result[key]
        except KeyError:
            agrec = agg_record()
            for value, sel in zip(key, selectors):
                agrec.agg[sel.field_name] = value
            agg_result[key] = agrec

        for aggregator in aggregators:
            aggregator(agrec, rec)
        
        if len(agg_stack) > 1:
            self._agg(agg_stack[1:], agrec.sub, rec)
        else:
            agrec.add_record(rec)

    def _flatten(self, agg_result, inc_detail, lvl=0):
        for key, agg_record in agg_result.items():
            head = dict(agg_record.agg)
            head['_type'] = 'ah'
            head['_level'] = lvl
            yield head
            for rec in self._flatten(agg_record.sub, inc_detail, lvl+1):
                yield rec
            if inc_detail:
                for rec in agg_record.recs:
                    detail = dict(rec)
                    detail['_type'] = 'd'
                    yield detail

            foot = dict(agg_record.agg)
            foot['_type'] = 'af'
            foot['_level'] = lvl
            yield foot


class agg_record:
    """ Stores the running results of aggregate computation
    """
    def __init__(self):
        # all the aggregate values
        self.agg = OrderedDict()
        self.sub = OrderedDict()
        self.recs = []

    def __iter__(self):
        return iter(self.agg)

    def add_record(self, record):
        self.recs.append(record)

    def set(self, agg_field_name, value):
        self.agg[agg_field_name] = value

    def get(self, agg_field_name):
        return self.agg[agg_field_name]

class sum:
    def __init__(self, field, calc_field=None):
        self.field = field
        if calc_field is None:
            calc_field = field
        self.calc_field = calc_field
    def __call__(self, agrec, rec):
        try:
            cur = agrec.get(self.calc_field)
        except KeyError:
            cur = 0
        agrec.set(self.calc_field, cur + rec[self.field])

class count:
    def __init__(self, field='count'):
        self.field = field
    def __call__(self, agrec, rec):
        try:
            cur = agrec.get(self.field)
        except KeyError:
            cur = 0
        agrec.set(self.field, cur + 1)

class select_all:
    def __init__(self, field_name=None):
        self.field_name = field_name
    def compute_key(self, record):
        return None

class field:
    def __init__(self, value_field_name, field_name=None):
        if field_name is None:
            field_name = value_field_name
        self.field_name = field_name
        self.value_field_name = value_field_name

    def compute_key(self, record):
        return record[self.value_field_name]

def test():
    cursor = R.db.dict_cursor()

    cursor.execute("""
     SELECT batch_date, patient.first_name, patient.last_name, 
            trans.patient_id, rx_number, total
     FROM trans
     JOIN patient ON
        trans.patient_id = patient.patient_id
     WHERE 
     batch_date BETWEEN '2010-01-01' AND '2010-01-31' AND
           trans.group_number = '56500'
    """)

    agg = aggregator()
    agg.add_level(select_all(), (count(), sum('total')))
    agg.add_level(field('batch_date'), sum('total'))
    agg.add_level((field('first_name'),
                   field('last_name'),
                   field('patient_id')), count())
    result = agg.transform(cursor)

    for rec in result:
        print(rec)

if __name__ == '__main__':
    test()
