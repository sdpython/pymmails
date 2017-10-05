#-*- coding: utf-8 -*-
"""
@file
@brief Module *pymmails*.
Functions to automatically grab and send mails.
"""
from .grabber.mail_exception import MailException
from .grabber.email_message import EmailMessage
from .grabber.mailboximap import MailBoxImap
from .grabber.mailbox_mock import MailBoxMock
from .render.email_message_renderer import EmailMessageRenderer
from .render.email_message_list_renderer import EmailMessageListRenderer
from .sender.email_sender import create_smtp_server, send_email, compose_email


__version__ = "0.2"
__author__ = "Xavier Dupré"
__github__ = "https://github.com/sdpython/pymmails"
__url__ = "http://www.xavierdupre.fr/app/pymmails/helpsphinx/index.html"
__license__ = "MIT License"


def _setup_hook():
    """
    does nothing
    """
    pass


def check(log=False):
    """
    Checks the library is working.
    It raises an exception.
    If you want to disable the logs:

    @param      log     if True, display information, otherwise
    @return             0 or exception
    """
    return True
