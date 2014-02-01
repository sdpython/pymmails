# coding: latin-1
"""
@file
@brief Defines a mailbox using IMAP
"""

import sys, os, imaplib, re, email, email.message, datetime, dateutil.parser, mimetypes

from .mail_exception import MailException
from .email_message import EmailMessage

class MailBoxImap :
    """
    defines a mail box with IMAP interface
    """
    
    expFolderName = re.compile('\\"(.*?)\\"')
    
    def __init__ (self, user, pwd, server, ssl = False) :
        """
        constructor
        @param  user        user
        @param  pwd         password
        @param  server      server something like ``imap.domain.ext``
        @param  ssl         select ``IMPA_SSL`` or ``IMAP``
        """
        self.M = imaplib.IMAP4_SSL(server) if ssl else imaplib.IMAP4(server)
        self._user = user
        self._password = pwd
        
        from pyquickhelper import fLOG
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
        if folders[0] != "OK" :
            raise MailException("unable to retrieve the folder list for " + user)
        res = []
        for f in folders[1] :
            s = f.decode("utf8")
            if r"\Noselect" in s : continue
            # s looks like this:  (\HasNoChildren) "/" "INBOX/Something"
            exp = MailBoxImap.expFolderName.findall(s)
            name = exp[-1]
            res.append(name)
        return res
        
    def enumerate_mails_in_folder (self, folder, skip_function = None, pattern = "ALL") :
        """
        enumerates all mails in folder folder
        @param      folder          folder name
        @param      skip_function   if not None, use this function on the header/body to avoid loading the entire message (and skip it)
        @param      pattern         search pattern (see below)
        @return                     iterator on (message)
        
        The search pattern can be used to look for a subset of email.
        It follows these `specifications <http://tools.ietf.org/html/rfc3501#page-49>`_.
        Some examples:
        @code
            pattern='FROM "xavier" SINCE 1-Feb-2013'
            pattern='FROM "xavier" SINCE 1-Feb-2013 BEFORE 5-May-2013'
            pattern='FROM "xavier" SINCE 1-Feb-2013 BEFORE 5-May-2013 (UNANSWERED)'
            pattern='CC "jacques" FROM "xavier" (DELETED)'
            pattern='TEXT "github"'
            pattern='LARGER 10000 SMALLER 1000000'
            pattern='SUBJECT "programmation"'
            pattern='TO "student" (FLAGGED)'
            pattern='(UNSEEN)'
        @endcode
        
        If the function generates an error such as::
        
            imaplib.error: command: SEARCH => got more than 10000 bytes
            
        The keyword RECENT will be added to the search pattern
        in order to retreive the newest mails.
        """
        qfold = self.M._quote(folder)
        self.fLOG("MailBoxImap [folder={0}]".format(qfold))
        self.M.select(qfold, readonly=True) 
        
        try :
            typ, data = self.M.search(None, pattern)
        except Exception as e :
            if "SEARCH => got more " in str(e) :
                if pattern == "ALL" : pattern = "RECENT"
                else : pattern += " RECENT"
                pattern = pattern.strip()
                self.fLOG("limit email search for folder", folder, " to recent emails with pattern", pattern)
                typ, data = self.M.search(None, pattern)
            else :
                raise e
            
        spl = data[0].split()
        self.fLOG("MailBoxImap [folder={0} nbm={1}]".format(folder, len(spl)))
        
        for num in spl:
            if skip_function != None :
                typ, data = self.M.fetch(num, '(BODY[HEADER])')
                emailBody = data[0][1]
                mail = email.message_from_bytes(emailBody, _class=EmailMessage)
                if skip_function(mail) :
                    continue
            
            typ, data = self.M.fetch(num, '(RFC822)')
            emailBody = data[0][1]
            mail = email.message_from_bytes(emailBody, _class=EmailMessage)
            yield mail
            
        self.M.close()
        
    def dump_html(self, pattern="ALL", folder="."):
        """
        Dumps all emails to a folder,
        it creates a subfolder for all inbox folders.
        
        @param      pattern     search pattern, @see me enumerate_mails_in_folder
        @param      folder      folder where to dump
        @return                 list of dumped files
        
        """        
        res = [ ]
        
        def skip_function (mail) :
            if mail.isDumped(subfold, attach) :
                return True
        
        folders = self.folders()
        self.fLOG("MailBoxImap [folders={0}]".format(",".join(folders)))
        for fold in folders :
            if fold == "INBOX/OUTBOX" :
                # we skip that folder, does not seem to be one
                continue
            self.fLOG("MailBoxImap: dumping folder ", fold)
            subfold = os.path.join(folder,fold)
            attach = os.path.join(subfold, "_attachments")

            skip1,skip2 = True,True
            for mail in self.enumerate_mails_in_folder(fold, skip_function = skip_function, pattern = pattern) :
                if skip1 and not os.path.exists (subfold) :
                    os.makedirs(subfold)
                    skip1 = False
                if skip2 and not os.path.exists(attach) :
                    os.makedirs(attach)
                    skip2 = False
                mail.dump_html(subfold, attach, fLOG = self.fLOG)
            
        


