#-*- coding: utf-8 -*-
"""
Documentation for this file.
"""

__version__ = "0.2"
__author__ = "Xavier Dupré"
__github__ = "https://github.com/sdpython/pymmails"
__url__ = "http://www.xavierdupre.fr/app/pymmails/helpsphinx/index.html"
__downloadUrl__ = "http://www.xavierdupre.fr/site2013/index_code.html#pymmails"
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


from .grabber.mail_exception import MailException
from .grabber.email_message import EmailMessage
from .grabber.mailboximap import MailBoxImap
from .sender.email_sender import create_smtp_server, send_email, compose_email
