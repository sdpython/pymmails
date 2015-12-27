# coding: latin-1
"""
@file
@brief Defines a mailbox using IMAP
"""

import os
import email
import email.message

from .email_message import EmailMessage
from .mailboximap import MailBoxImap
from pyquickhelper import noLOG
from pyquickhelper.filehelper.encryption import decrypt_stream


class MailBoxMock(MailBoxImap):

    """
    define a mail box reading from file (kind of mock)
    """

    def __init__(self, folder, pwd, fLOG=noLOG):
        """
        constructor
        @param  folder      folder to look into
        @param  pwd         password, in case mails are encrypted
        @param  fLOG        logging function

        For gmail, it is ``imap.gmail.com`` and ssl must be true
        """
        self._user = None
        self._password = pwd
        self._folder = folder
        self.fLOG = fLOG

    def login(self):
        """
        login (nothing to do here)
        """
        pass

    def logout(self):
        """
        logout (nothing to do here)
        """
        pass

    def folders(self):
        """
        returns the list of folder of the mail box
        """
        res = []
        for root, dirs, files in os.walk(self._folder):
            for name in dirs:
                res.append(name)
        return res

    def read_mail_from_file(self, filename):
        """
        extract a mail from a file

        @param      filename        filename
        @return                     MailMessage
        """
        with open(filename, "rb") as f:
            content = f.read()
        if self._password:
            b = decrypt_stream(self._password, content)
        else:
            b = content
        return email.message_from_bytes(b, _class=EmailMessage)

    def enumerate_mails_in_folder(
            self, folder, skip_function=None, pattern="ALL"):
        """
        enumerate all mails in a folder

        @param      folder              folder
        @param      skip_function       to skip mail or None to keep them all
        @param      pattern             ``'ALL'`` by default, unused otherwise
        @return                         enumerator on mails
        """
        local = os.path.join(self._folder, folder)
        for name in os.listdir(local):
            full = os.path.join(local, name)
            if os.path.isfile(full):
                mail = self.read_mail_from_file(full)
                if skip_function is not None and skip_function(mail):
                    continue
                yield mail

    def enumerate_search_person(self,
                                person,
                                folder,
                                skip_function=None,
                                date=None,
                                max_dest=5):
        """
        enumerates all mails in folder folder from a user or sent to a user

        @param      person          person to look for
        @param      folder          folder name
        @param      skip_function   if not None, use this function on the header/body to avoid loading the entire message (and skip it)
        @param      pattern         search pattern (see below)
        @param      max_dest        maximum number of receivers
        @return                     iterator on (message)
        """
        raise NotImplementedError()

    def enumerate_search_subject(self,
                                 subject,
                                 folder,
                                 skip_function=None,
                                 date=None,
                                 max_dest=5):
        """
        enumerates all mails in folder folder with a subject verifying a regular expression

        @param      subject         subject to look for
        @param      folder          folder name
        @param      skip_function   if not None, use this function on the header/body to avoid loading the entire message (and skip it)
        @param      pattern         search pattern (see below)
        @param      max_dest        maximum number of receivers
        @return                     iterator on (message)
        """
        raise NotImplementedError()
