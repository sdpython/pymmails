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


def compose_email(fr, to, subject, body_html=None, body_text=None, attachements=None, cc=None, bcc=None):
    """
    Composes an email as a string.

    @param      fr              from
    @param      to              receiver (or list of receivers)
    @param      subject         subject
    @param      body_text       body text
    @param      body_html       body html
    @param      cc              list of ccs
    @param      bcc             list of bccs
    @param      attachements    list of files to attach to the email
    @return                     string

    If the file is a text file, the filename can be replaced by (filename, encoding).
    If *body_html* and *body_text* are filled, only the first one will be used.
    """
    if isinstance(to, str):
        to = [to]
    if isinstance(cc, str):
        cc = [cc]
    if isinstance(bcc, str):
        bcc = [bcc]
    if attachements is None:
        attachements = []

    global COMMASPACE  # pylint: disable=W0602
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(to)
    outer['From'] = fr
    if cc is not None:
        outer["CC"] = COMMASPACE.join(cc)
    if bcc is not None:
        outer["BCC"] = COMMASPACE.join(bcc)

    if body_html is not None:
        part2 = MIMEText(body_html, 'html')
        outer.attach(part2)
    elif body_text is not None:
        part1 = MIMEText(body_text, 'plain')
        outer.attach(part1)
    else:
        # no body
        pass

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
    Creates a SMTP server and log into it.

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


def send_email(server, fr, to, subject, body_html=None, body_text=None,
               attachements=None, delay_sending=False, cc=None, bcc=None):
    """
    Sends an email as a string.

    @param      server          result from function @see fn create_smtp_server
    @param      fr              from
    @param      to              destination (or list of receivers)
    @param      cc              cc
    @param      bcc             bcc
    @param      subject         subject
    @param      body_text       body text
    @param      body_html       body html
    @param      attachements    list of files to attach to the email
    @param      delay_sending   if True, the function returns a function which will send the mail if
                                executed
    @return                     function (if *delay_sending*), return of
                                `sendmail <https://docs.python.org/3.5/library/smtplib.html#smtplib.SMTP.sendmail>`_
                                otherwise

    .. exref::
        :title: Send an email

        ::

            from pymmails import create_smtp_server, send_email
            server = create_smtp_server("gmail", "somebody", "pwd")
            send_email(server, "from.sender@gmail.com",
                       "to.receiver@else.com", "subject",
                       attachements = [ os.path.abspath(__file__) ])
            server.quit()

    .. faqref::
        :title: Gmail does not allow to send or get emails with Python

        By default, a Gmail account does not enable the IMAP access.
        That explains why it is not possible to send or get messages from Gmail.
        The following page
        `Get started with IMAP and POP3 <https://support.google.com/mail/troubleshooter/1668960?hl=en#ts=1665018>`_
        explains how to enable that option.
    """
    astring = compose_email(fr, to, subject, body_html=body_html, cc=cc, bcc=bcc,
                            body_text=body_text, attachements=attachements)
    to = list(to) if isinstance(to, (list, tuple)) else [to]
    if isinstance(cc, str):
        to.append(cc)
    elif isinstance(cc, (list, tuple)):
        to.extend(cc)
    if isinstance(bcc, str):
        to.append(bcc)
    elif isinstance(bcc, (list, tuple)):
        to.extend(bcc)

    if delay_sending:
        def f(fr=fr, to=to, astring=astring):  # pylint: disable=W0102
            "local function"
            try:
                server.sendmail(fr, to, astring)
            except Exception as e:
                raise AssertionError(
                    "Unable to send mail to {0} from '{1}'".format(to, fr)) from e
        return f
    else:
        try:
            return server.sendmail(fr, to, astring)
        except Exception as e:
            raise AssertionError(
                "Unable to send mail to {0} from '{1}'".format(to, fr)) from e
