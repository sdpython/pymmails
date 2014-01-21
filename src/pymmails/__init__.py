"""
Documentation for this file.
"""

def check( log = False):
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

