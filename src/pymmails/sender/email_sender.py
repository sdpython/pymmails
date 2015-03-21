"""
@file
@brief Functions to send emails
"""
import smtplib
import os

import mimetypes
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '


def compose_email(
        fr,
        to,
        subject,
        body=None,
        attachements=None):
    """
    compose an email as a string

    @param      fr              from
    @param      to              destination (or list of receivers)
    @param      subject         subject
    @param      body            body
    @param      attachements    list of files to attach to the email
    @return                     string

    If the file is a text file, the filename can be replaced by (filename, encoding).
    """
    if isinstance(to, str):
        to = [to]
    if body is None:
        body = ""
    if attachements is None:
        attachements = []

    global COMMASPACE
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(to)
    outer['From'] = fr
    outer.preamble = 'prepared by pymmails.\n'

    for filename in attachements:
        if isinstance(filename, tuple):
            path = filename[0]
            encoding = filename[1]
        else:
            path = filename
            encoding = "ascii"

        if not os.path.exists(path):
            raise FileNotFoundError(path)
        if not os.path.isfile(path):
            raise FileNotFoundError(path + " is not a file")

        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            with open(path, "r", encoding=encoding) as fp:
                st = fp.read()
                msg = MIMEText(st, _subtype=subtype)
        elif maintype == 'image':
            with open(path, 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            with open(path, 'rb') as fp:
                msg = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(path, 'rb') as fp:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)

        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        outer.attach(msg)

    composed = outer.as_string()
    return composed


def create_smtp_server(host, username, password):
    """
    creates a SMTP server and log into it.

    @param      host        something like ``smtp.gmail.com:587``
    @param      username    username
    @param      login       login
    @return                 server

    You should call server.quit() when the server is not used anymore.
    """
    if host == "gmail":
        host = 'smtp.gmail.com:587'

    server = smtplib.SMTP(host)
    server.starttls()
    server.login(username, password)
    return server


def send_email(server, fr,
               to,
               subject,
               body=None,
               attachements=None):
    """
    compose an email as a string

    @param      server          result from function @see fn create_smtp_server
    @param      fr              from
    @param      to              destination (or list of receivers)
    @param      subject         subject
    @param      body            body
    @param      attachements    list of files to attach to the email
    @return                     string

    @example(Send an email)
    @code
    server = create_smtp_server("gmail", "somebody", "pwd")
    send_email(server, "somebody@gmail.com", "somebody@else.com",
                    "subject", attachements = [ os.path.abspath(__file__) ])
    server.quit()
    @endcode
    @endexample
    """
    astring = compose_email(
        fr,
        to,
        subject,
        body=body,
        attachements=attachements)
    server.sendmail(fr, to, astring)
