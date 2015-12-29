"""
@file
@brief Defines a mailbox using IMAP
"""

import imaplib
import re
import email
import email.message

from .mail_exception import MailException
from .email_message import EmailMessage
from pyquickhelper import noLOG


class MailBoxImap:

    """
    defines a mail box with IMAP interface
    """

    expFolderName = re.compile('\\"(.*?)\\"')

    def __init__(self, user, pwd, server, ssl=False, fLOG=noLOG):
        """
        constructor
        @param  user        user
        @param  pwd         password
        @param  server      server something like ``imap.domain.ext``
        @param  ssl         select ``IMPA_SSL`` or ``IMAP``
        @param  fLOG        logging function

        For gmail, it is ``imap.gmail.com`` and ssl must be true
        """
        self.M = imaplib.IMAP4_SSL(server) if ssl else imaplib.IMAP4(server)
        self._user = user
        self._password = pwd
        self.fLOG = fLOG

    def login(self):
        """
        login
        """
        self.M.login(self._user, self._password)

    def logout(self):
        """
        logout
        """
        self.M.logout()

    def folders(self):
        """
        returns the list of folder of the mail box
        """
        folders = self.M.list()
        if folders[0] != "OK":
            raise MailException(
                "unable to retrieve the folder list for " +
                self.user)
        res = []
        for f in folders[1]:
            s = f.decode("utf8")
            if r"\Noselect" in s:
                continue
            # s looks like this:  (\HasNoChildren) "/" "INBOX/Something"
            exp = MailBoxImap.expFolderName.findall(s)
            name = exp[-1]
            res.append(name)
        return res

    def enumerate_mails_in_folder(
            self, folder, skip_function=None, pattern="ALL"):
        """
        enumerates all mails in folder folder
        @param      folder          folder name
        @param      skip_function   if not None, use this function on the header/body to avoid loading the entire message (and skip it)
        @param      pattern         search pattern (see below)
        @return                     iterator on (message)

        The search pattern can be used to look for a subset of email.
        It follows these `specifications <http://tools.ietf.org/html/rfc3501#page-49>`_.

        @example(Search pattern)

        ::

            pattern='FROM "xavier" SINCE 1-Feb-2013'
            pattern='FROM "xavier" SINCE 1-Feb-2013 BEFORE 5-May-2013'
            pattern='FROM "xavier" SINCE 1-Feb-2013 BEFORE 5-May-2013 (UNANSWERED)'
            pattern='CC "jacques" FROM "xavier" (DELETED)'
            pattern='TEXT "github"'
            pattern='LARGER 10000 SMALLER 1000000'
            pattern='SUBJECT "programmation"'
            pattern='TO "student" (FLAGGED)'
            pattern='(UNSEEN)'

        @endexample

        If the function generates an error such as::

            imaplib.error: command: SEARCH => got more than 10000 bytes

        The keyword RECENT will be added to the search pattern
        in order to retreive the newest mails.
        """
        qfold = self.M._quote(folder)
        self.fLOG("MailBoxImap [folder={0}]".format(qfold))
        self.M.select(qfold, readonly=True)

        try:
            typ, data = self.M.search(None, pattern)
        except Exception as e:
            if "SEARCH => got more " in str(e):
                if pattern == "ALL":
                    pattern = "RECENT"
                else:
                    pattern += " RECENT"
                pattern = pattern.strip()
                self.fLOG(
                    "limit email search for folder",
                    folder,
                    " to recent emails with pattern",
                    pattern)
                typ, data = self.M.search(None, pattern)
            else:
                raise Exception(
                    "unable to search for pattern: {0}\nin subfolder {1}\ncheck the folder you search for is right"
                    .format(pattern, qfold)) from e

        spl = data[0].split()
        self.fLOG("MailBoxImap [folder={0} nbm={1}]".format(folder, len(spl)))

        for num in spl:
            if skip_function is not None:
                typ, data = self.M.fetch(num, '(BODY[HEADER])')
                emailBody = data[0][1]
                mail = email.message_from_bytes(emailBody, _class=EmailMessage)
                if skip_function(mail):
                    continue

            typ, data = self.M.fetch(num, '(RFC822)')
            emailBody = data[0][1]
            mail = email.message_from_bytes(emailBody, _class=EmailMessage)
            yield mail

        self.M.close()

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
        pat1 = 'FROM "{0}"'.format(person)
        if date is not None:
            pat1 += ' SINCE {0}'.format(date)
        for mail in self.enumerate_mails_in_folder(
                folder, skip_function=skip_function, pattern=pat1):
            yield mail
        pat2 = 'TO "{0}"'.format(person)
        if date is not None:
            pat2 += ' SINCE {0}'.format(date)
        for mail in self.enumerate_mails_in_folder(
                folder, skip_function=skip_function, pattern=pat2):
            if max_dest > 0:
                tos = mail.get_to()
                l = len(tos)
                if l <= max_dest:
                    yield mail
            else:
                yield mail

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
        pat1 = 'SUBJECT "{0}"'.format(subject)
        for mail in self.enumerate_mails_in_folder(
                folder, skip_function=skip_function, pattern=pat1):
            yield mail
