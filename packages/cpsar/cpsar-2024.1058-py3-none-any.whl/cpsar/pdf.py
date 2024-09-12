import logging; log=logging.getLogger('')
import os
import subprocess
import sys

BASEPATH = '/server/ar/www/'

def html2pdf(html_path, pdf_path, psc_path=''):
    """ Create a PDF file from the html_path """
    ps_path = '%s.ps' % html_path
    if psc_path:
        ps_cmd = 'html2ps -b %s -f %s -o %s %s' % (
            BASEPATH,
            psc_path,
            ps_path,
            html_path)
    else:
        ps_cmd = 'html2ps -b %s -o %s %s' % (
            BASEPATH,
            ps_path,
            html_path)

    log.debug('Generating PS file %s with command %s',
        ps_path, ps_cmd)

    run_or_die(ps_cmd)

    pdf_cmd = 'ps2pdf %s %s' % (ps_path, pdf_path)
    log.debug('Generating PDF File %s with command %s',
        pdf_path, pdf_cmd)
    run_or_die(pdf_cmd)
    os.remove(ps_path)

def run_or_die(cmd):
    s, o = subprocess.getstatusoutput(cmd)
    if s:
        log.error('The command %s failed' % cmd)
        log.error('Output: %s', o)
        sys.exit()
    if o:
        log.debug("Output from %r:\n%s", cmd, o)
