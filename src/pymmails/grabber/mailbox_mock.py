"""
@file
@brief Defines a mailbox using IMAP
"""

import os
import email
import email.message
from pyquickhelper.loghelper import noLOG
from pyquickhelper.filehelper.encryption import decrypt_stream
from .email_message import EmailMessage
from .mailboximap import MailBoxImap


class MailBoxMock(MailBoxImap):

    """
    Define a mail box reading from file (kind of mock).
    """

    def __init__(self, folder, pwd, fLOG=noLOG):
        """
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
        for __, dirs, _ in os.walk(self._folder):
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

    def enumerate_mails_in_folder(  # pylint: disable=W0221
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
                                max_dest=5,
                                body=True):
        """
        enumerates all mails in folder folder from a user or sent to a user

        @param      person          person to look for
        @param      folder          folder name
        @param      skip_function   if not None, use this function on the header/body to avoid loading the entire message (and skip it)
        @param      pattern         search pattern (see below)
        @param      max_dest        maximum number of receivers
        @param      body            also extract the body
        @return                     iterator on (message)
        """
        return self.enumerate_mails_in_folder(folder=folder, skip_function=skip_function)

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
