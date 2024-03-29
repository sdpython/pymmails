"""
@file
@brief Defines a mailbox using IMAP
"""

import imaplib
import re
import email
import email.message
from pyquickhelper.loghelper import noLOG
from .mail_exception import MailException
from .email_message import EmailMessage


class MailBoxImap:

    """
    Defines a mail box with :epkg:`IMAP` interface.

    .. exref::
        :title: Fetch mails from a gmail account

        ::

            user = "address no domain"
            pwd = "password"
            server = "imap.gmail.com"

            box = MailBoxImap(user, pwd, server, ssl=True)
            box.login()

            # ... fetch emails

            box.logout()
    """

    expFolderName = re.compile('\\"(.*?)\\"')

    def __init__(self, user, pwd, server, ssl=False, fLOG=noLOG):
        """
        @param  user        user
        @param  pwd         password
        @param  server      server something like ``imap.domain.ext``
        @param  ssl         select ``IMPA_SSL`` or ``IMAP``
        @param  fLOG        logging function

        For gmail, it is ``imap.gmail.com`` and ssl must be true.
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
        Returns the list of folder of the mail box.
        """
        folders = self.M.list()
        if folders[0] != "OK":
            raise MailException(
                "unable to retrieve the folder list for " +
                self._user)
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
            self, folder, skip_function=None, date=None, pattern="ALL", body=True):
        """
        Enumerates all mails in folder folder.

        @param      folder          folder name
        @param      skip_function   if not None, use this function on the header/body to avoid loading the entire message (and skip it)
        @param      pattern         search pattern (see below)
        @param      date            add a date to the pattern
        @param      body            add body
        @return                     iterator on (message)

        The search pattern can be used to look for a subset of email.
        It follows these `specifications
        <http://tools.ietf.org/html/rfc3501#page-49>`_.
        If a folder is a subfolder, the syntax should be
        ``folder/subfolder``.

        .. exref::
            :title: Search pattern

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

        If the function generates an error such as::

            imaplib.error: command: SEARCH => got more than 10000 bytes

        The keyword RECENT will be added to the search pattern
        in order to retreive the newest mails.
        """
        if isinstance(folder, list):
            for fold in folder:
                iter = self.enumerate_mails_in_folder(folder=fold,
                                                      skip_function=skip_function, date=date, pattern=pattern, body=body)
                for mail in iter:
                    yield mail
        else:
            qfold = self.M._quote(folder)
            self.M.select(qfold, readonly=True)

            if date is not None:
                pdat = 'SINCE {0}'.format(date)
                if pattern == "ALL":
                    pattern = pdat
                else:
                    pattern += " " + pdat

            try:
                pattern.encode('ascii')
                charset = None
            except UnicodeEncodeError:
                charset = 'UTF8'
                pattern = pattern.encode('utf-8')
                pattern = "".join(chr(b) for b in pattern)

            try:
                try:
                    _, data = self.M.search(charset, pattern)
                except UnicodeEncodeError:
                    charset = None
                    pattern = pattern.encode(
                        'ascii', errors='ignore').decode("ascii")
                    _, data = self.M.search(None, pattern)
            except Exception as e:
                if "SEARCH => got more " in str(e):
                    if pattern == "ALL":
                        pattern = "RECENT"
                    else:
                        pattern += " RECENT"
                    pattern = pattern.strip()
                    self.fLOG("[MailBoxImap.enumerate_mails_in_folder] limit email "
                              "search for folder '{0}' to recent emails with "
                              "pattern '{1}'".format(folder, pattern))
                    data = self.M.search(charset, pattern)[1]
                else:
                    raise MailException(
                        "Unable to search for pattern: '{0}' "
                        "(charset='{1}')\nin subfolder {2}\n"
                        "check the folder you search for is right."
                        .format(pattern, charset, qfold)) from e

            spl = data[0].split()
            self.fLOG("MailBoxImap.enumerate_mails_in_folder [folder={0} nbm={1} body={2} pattern={3}]".format(
                folder, len(spl), body, pattern))

            for num in spl:
                if skip_function is not None:
                    data = self.M.fetch(num, '(BODY[HEADER])')[1]
                    emailBody = data[0][1]
                    mail = email.message_from_bytes(
                        emailBody, _class=EmailMessage)
                    if skip_function(mail):
                        continue
                if body:
                    data = self.M.fetch(num, '(RFC822)')[1]
                    emailBody = data[0][1]
                    mail = email.message_from_bytes(
                        emailBody, _class=EmailMessage)
                elif skip_function is None:
                    data = self.M.fetch(num, '(BODY[HEADER])')[1]
                    emailBody = data[0][1]
                    mail = email.message_from_bytes(
                        emailBody, _class=EmailMessage)
                yield mail

            self.M.close()

    def enumerate_search_person(self, person, folder, skip_function=None,
                                date=None, max_dest=5, body=True):
        """
        Enumerates all mails in folder folder from a user
        or sent to a user.

        @param      person          person to look for or persons to look for
        @param      folder          folder name
        @param      skip_function   if not None, use this function on the header/body to avoid loading the entire message (and skip it)
        @param      pattern         search pattern (see below)
        @param      max_dest        maximum number of receivers
        @param      body            get the body
        @return                     iterator on (message)

        If *person* is a list, the function iterates on the list of
        persons to look for. It returns only unique mails.
        """
        if isinstance(person, list):
            unique_id = set()
            for p in person:
                mail_set = self.enumerate_search_person(p, folder=folder,
                                                        skip_function=skip_function, date=date,
                                                        max_dest=max_dest, body=body)
                for mail in mail_set:
                    uid = mail.UniqueID
                    if uid not in unique_id:
                        unique_id.add(uid)
                        yield mail
        else:
            pat1 = 'FROM "{0}"'.format(person)
            if date is not None:
                pat1 += ' SINCE {0}'.format(date)
            for mail in self.enumerate_mails_in_folder(folder, skip_function=skip_function,
                                                       pattern=pat1, body=body):
                yield mail
            pat2 = 'TO "{0}"'.format(person)
            if date is not None:
                pat2 += ' SINCE {0}'.format(date)
            for mail in self.enumerate_mails_in_folder(
                    folder, skip_function=skip_function, pattern=pat2):
                if max_dest > 0:
                    tos = mail.get_to()
                    if tos:
                        ll = len(tos)
                        if ll <= max_dest:
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
        Enumerates all mails in folder folder with a subject
        verifying a regular expression.

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
