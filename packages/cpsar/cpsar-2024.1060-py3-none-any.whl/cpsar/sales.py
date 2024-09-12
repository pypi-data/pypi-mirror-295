""" Sales Reporting Library

"""
from __future__ import absolute_import
import cpsar.runtime as R
import csv
import kcontrol
import os
import sys
import time

from . import auth
from . import pg
import cpsar.runtime as R

ACCESS_FILE = R.app_path('res', 'sales_access.txt')


def filter_group_numbers(groups):
    """ Only give back the groups the user has access to. """
    return groups

class ReportCodeListBox(kcontrol.ListBox):
    def __init__(self, name='report_code', blankOption=True, **k):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT DISTINCT report_code
            FROM client_report_code
            ORDER BY report_code
            """)
        values = [(c, c) for c, in cursor]
        kcontrol.ListBox.__init__(self, name, values=values, 
                                  blankOption=blankOption, **k)

class ClientListBox(kcontrol.ListBox):
    """ A special client list box that only includes groups that
    the current user has access to.
    """
    def __init__(self, name, class_='group_number', **k):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, group_number || ' ' || client_name
            FROM client
            ORDER BY group_number
            """)
        values = [('', '')] + list(cursor)
        kcontrol.ListBox.__init__(self, name, values=values, class_=class_, **k)

class DistributionAccountListBox(kcontrol.ListBox):
    def __init__(self, name):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT DISTINCT distribution_account v1, distribution_account v2
            FROM distribution_rule
            UNION
            SELECT 'rebate', 'rebate'
            ORDER BY v1
            """)

        values = [('', '')] + list(cursor)
        kcontrol.ListBox.__init__(self, name, values=values)

