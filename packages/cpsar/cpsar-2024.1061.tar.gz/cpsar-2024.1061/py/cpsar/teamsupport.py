""" Shared teamsupport library """
import os

import requests

def url(*extra):
    """ Build a team support API url for the given path fragments. """
    base = 'https://app.teamsupport.com/api/xml'
    args = (base,) + extra
    return os.path.join(*args)

def session():  
    """ Provide a request session which can be used to query the API """
    s = requests.Session()
    s.auth = _auth_token()
    return s

def _auth_token():
    """ Authentication username and password for CPS to connect. Returned as a
    tuple to interface with the requests module easily.
    """
    return ('555035', '017a4ac0-8738-4f9e-810b-0ca9df3c78a8')

