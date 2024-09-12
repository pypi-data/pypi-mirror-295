""" E-mail Sending Services """
try:
    import email.utils as eutils
except ImportError:
    import email.Utils as eutils
import mimetypes
import os
import smtplib
import imaplib
import io
import textwrap
import time
import warnings

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from smtplib import SMTPException

from cpsar import config
from cpsar import db

class Mailer(object):
    """ Stateful abstraction on top of sending an email. """
    subject = ''
    recipients = ()
    bcc = []
    reply_to = None

    _sender = None

    @property
    def sender(self):
        if self._sender is not None:
            return self._sender
        return config.site_sender_email()

    @sender.setter
    def sender(self, value):
        self._sender = value

    auto_line_feed = True
    log_message = False
    def __init__(self, subject=None, recipients=None, copy_to_imap=True):
        self.body = io.StringIO()
        if subject:
            self.subject = subject
        if recipients is not None:
            self.recipients = recipients
        self._attachments = []
        try:
            self.reply_to = config.reply_to_email()
        except config.ConfigError:
            pass
        self.copy_to_imap = copy_to_imap

    def set_billing_receipients(self):
        self.recipients = config.billing_recipients()

    def set_billing_bcc(self):
        self.bcc = config.billing_recipients()

    def __call__(self, msg, *args):
        """ Write the data to the body of the message. """
        if args: msg %= args
        self.body.write(msg)
        if self.auto_line_feed:
            self.body.write("\n")
        if self.log_message:
            log.debug("MI: %s", msg)

    def write_dedented(self, msg, *args):
        if args: msg %= args
        return self(textwrap.dedent(msg))

    def write(self, buf):
        """ Implement a file-like interface """
        self(buf)

    def add_attachment(self, fname, payload):
        self._attachments.append((fname, payload))

    def send(self):
        """ Send out the message. """
        outer = MIMEMultipart()
        outer['Subject'] = self.subject
        outer['From'] = self.sender
        outer['To'] = ", ".join(self.recipients)
        if self.reply_to:
            outer['Reply-To'] = self.reply_to
        outer['Date'] = eutils.formatdate()
        outer["Message-ID"] = eutils.make_msgid()
        outer["Mime-version"] = "1.0"
        outer.attach(MIMEText(self.body.getvalue()))

        for fname, payload in self._attachments:
            mt,_ = mimetypes.guess_type(fname)
            if not mt:
                big, little = 'application', 'octet-stream'
            else:
                big, _, little = mt.partition('/')
            part = MIMEBase(big, little)
            part.set_payload(payload)
            encode_base64(part)
            part.add_header('Content-Size', str(len(part)))
            part.add_header('Content-Disposition',
                'attachment; filename="%s"' % fname)
            outer.attach(part)

        smtp = smtplib.SMTP(config.smtp_host())
        smtp.sendmail(self.sender, self.recipients + self.bcc, outer.as_string())
        smtp.close()

        if self.copy_to_imap:
            self._copy_to_imap(outer)

    def _copy_to_imap(self, msg):
        cred = config.imap_copy_credentials()
        if not cred:
            return
        current_date = time.strftime("%Y-%m")
        target_folder = f'{cred.folder}.{current_date}'
        try:
            with imaplib.IMAP4_SSL(cred.server,) as imap_server:
                imap_server.login(cred.user, cred.password)
                # Use '\\Seen' for the message to appear viewed
                imap_server.append(f'"{target_folder}"', '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
                imap_server.logout()
        except Exception as e:
            warnings.warn(f"Error saving to {cred.folder!r} folder: {e}")
            # Consider writing to a log or taking other action as needed

def email_for(lookup):
    """ Lookup """
    cursor = db.dict_cursor()
    cursor.execute("""
        select *
        from site_config
        """)
    f = next(cursor)
    return f.get(lookup, [config.customer_service_email()])

class HTMLMailer(Mailer):

    def __init__(self, subject=None, recipients=None, copy_to_imap=True):
        super(HTMLMailer, self).__init__(subject, recipients, copy_to_imap)
        self._html_buf = io.StringIO()
        self._attachments = []

    def html(self, msg, *args):
        if args: msg %= args
        self._html_buf.write(msg)

    def wrap(self, msg, elem='div'):
        """ Write the message to both text and html, wrapping the html
        in the given element.
        """
        self.write(msg)
        self._html_buf.write("<%s>%s</%s>" % (elem, msg, elem))

    def add_attachment(self, fname, payload):
        self._attachments.append((fname, payload))

    def send(self):
        bouter = MIMEMultipart()
        bouter['Subject'] = self.subject
        bouter['From'] = self.sender
        bouter['To'] = ", ".join(self.recipients)
        bouter['Date'] = eutils.formatdate()
        bouter["Message-ID"] = eutils.make_msgid()

        outer = MIMEMultipart('alternative')
        outer.attach(self._text_mime())
        outer.attach(self._html_mime())
        bouter.attach(outer)

        for fname, payload in self._attachments:
            mt,_ = mimetypes.guess_type(fname)
            if not mt:
                big, little = 'application', 'octet-stream'
            else:
                big, _, little = mt.partition('/')
            part = MIMEBase(big, little)
            part.set_payload(payload)
            encode_base64(part)
            part.add_header('Content-Size', str(len(part)))
            part.add_header('Content-Disposition',
                'attachment; filename="%s"' % fname)
            bouter.attach(part)

        smtp = smtplib.SMTP(config.smtp_host())
        smtp.sendmail(self.sender, self.recipients + self.bcc, 
                      bouter.as_string())
        smtp.close()
        if self.copy_to_imap:
            self._copy_to_imap(bouter)

    def _text_mime(self):
        return MIMEText(self.body.getvalue(), 'plain')

    def _html_mime(self):
        return MIMEText(self._html_buf.getvalue(), 'html')

class MockMailer(object):
    def __init__(self, subject=None, recipients=None):
        self.body = io.StringIO()
        if subject:
            self.subject = subject
        if recipients is not None:
            self.recipients = recipients
        self._attachments = []

    def send(self):
        print("To: %s\n%s" % (self.recipients, self.body.getvalue()))

