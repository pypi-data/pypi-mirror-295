""" Configuration module for all CPS/AR programs. We use the bd.config module
to actually provide config loading services (as it has private label
supporting functionality in it).
"""
import configparser
import os
import re
import threading

opj = os.path.join

_CONFIG_FILE = "/etc/bd3.cfg"

_config = None          # configparser.ConfigParser
# used to store sub list for request-level configuration
_env = threading.local()

class ConfigError(Exception):
    pass

def billing_recipients(): return _comma_list_config_var("billing_recipients")
def cobol_server_url(): return _str_config_var('cobol_server_url')
def customer_service_email(): return _str_config_var('customer_service_email')
def development():
    try:
        val = _str_config_var('development')
    except:
        return False
    return True if val == '1' else False

def expiration_notify_email(): return _comma_list_config_var("expiration_notify_email")
def ar_conn_str(): return _str_config_var('ar_conn_str')
def data_dir(*extra): return os.path.join(_str_config_var('data_dir'), *extra)
def dev_mode():
    try:
        return bool(_str_config_var('dev_mode'))
    except ConfigError:
        return False
def dbname(): return re.findall("dbname='(.*?)'", ar_conn_str())[0]
def dbhost(): return re.findall("host='(.*?)'", ar_conn_str())[0]
def font_path(*extra): return virtualenv_root('res/fonts', *extra)
def import_dir(*extra): return opj(_dir_config_var('import_dir'), *extra)
def inv_base(*extra): return virtualenv_root('www', *extra)
def invoice_class(): return _str_config_var('invoice_class')
def mako_cache_dir(*extra):
    return opj(_dir_config_var('ar_mako_cache_dir', False, True), *extra)
def mako_template_dir(): return virtualenv_root('mako')
def monthly_trans_file_glob(): return _str_config_var("monthly_trans_file_glob")
def production_url(): return _str_config_var('production_url')
def session_dir(): return _dir_config_var('session_dir', False, True)
def smtp_host(): return _str_config_var('smtp_host', False, 'localhost')
def sql_dir(*parts): return virtualenv_root("sql", *parts)
def trans_file_glob(): return _str_config_var("trans_file_glob")
def site_sender_email():
    """ the email address that is used in the from section of emails sent
    from the web site. This used to be customer service email but we had problems
    with that for mjoseph.
    """
    return _str_config_var('site_sender_email')
def virtualenv_root(*extra): return opj(_dir_config_var('ar_virtualenv_root'), *extra)

## Private Label Configuration
def set_private_label(s):
    """ Configure which private label the current process is running under.
    This should only be set once, usually in the .wsgi script that kicks off the
    process, or perhaps during console application initialization if the program
    is not web-based and private-label configuration needs to be done.
    """
    _env.private_label = s

def private_label():
    """ Is the current process running as a private label? Returns None if not
    or a string representing which private label if so """
    return getattr(_env, 'private_label', None)

## Private
def _comma_list_config_var(name):
    v = _str_config_var(name, False, '')
    v = [f.strip() for f in v.split(",")]
    return [f for f in v if f]

def _dir_config_var(name, required=True, ondemand=False):
    _load_if_needed()
    path = _str_config_var(name, required)
    if not os.path.isdir(path) and ondemand:
        try:
            os.mkdir(path)
        except (IOError, OSError) as e:
            raise ConfigError("Could not create %s %s on demand: %s"
                    % (name, path, e))
    if path and not os.path.isdir(path):
        raise ConfigError("%s %s is not a directory" % (name, path))
    return path

def _load():
    global _config
    _config = configparser.RawConfigParser()
    try:
        fd = open(_CONFIG_FILE)
    except (IOError, OSError) as e:
        raise ConfigError("Error opening config file %s: %s" % (_CONFIG_FILE, e))
    _config.readfp(fd)
    fd.close()

def _load_if_needed():
    """ Only load the configuration file if it hasn't already been loaded. """
    if _config is None:
        _load()

def _section_search_list():
    x = []
    if getattr(_env, 'sublist', None):
        x.extend(_env.sublist)
    if private_label():
        x.append(private_label())
    x.append("default")
    return x

def _str_config_var(name, required=True, default=None, inherit=True):
    _load_if_needed()
    val = None
    if inherit:
        search_list = _section_search_list()
    elif private_label():
        search_list = [private_label()]
    else:
        search_list = ['default']
    for section in search_list:
        try:
            val = str(_config.get(section, name))
            break
        except configparser.Error as e:
            pass
    if required and val is None:
        raise ConfigError("Missing required config var %s" % name)
    return val or default

