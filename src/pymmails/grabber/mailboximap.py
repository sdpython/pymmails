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
    
    def __init__ (self, user, pwd, server) :
        """
        constructor
        @param  user        user
        @param  pwd         password
        @param  server      server something like ``imap.domain.ext``
        """
        self.M = imaplib.IMAP4(server)
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
            # s looks like this:  (\HasNoChildren) "/" "INBOX/Something"
            exp = MailBoxImap.expFolderName.findall(s)
            name = exp[-1]
            res.append(name)
        return res
        
    def enumerate_mails_in_folder (self, folder, skip_function = None) :
        """
        enumerates all mails in folder folder
        @param      folder          folder name
        @param      skip_function   if not None, use this function on the header/body to avoid loading the entire message (and skip it)
        @return                     iterator on (message)
        """
        qfold = self.M._quote(folder)
        self.fLOG("MailBoxImap [folder={0}]".format(qfold))
        self.M.select(qfold, readonly=True) 
        typ, data = self.M.search(None, 'ALL')
        spl = data[0].split()
        self.fLOG("MailBoxImap [folder={0} nbm={1}]".format(folder, len(spl)))
        
        for num in spl:
            if skip_function != None :
                typ, data = self.M.fetch(num, '(BODY[HEADER])')
                emailBody = data[0][1]
                mail = email.message_from_bytes(emailBody, _class=EmailMessage)
                mail.set_id(num.decode("utf8"))
                if skip_function(mail) :
                    continue
            
            typ, data = self.M.fetch(num, '(RFC822)')
            emailBody = data[0][1]
            mail = email.message_from_bytes(emailBody, _class=EmailMessage)
            mail.set_id(num.decode("utf8"))
            yield mail
            
        self.M.close()
        
    def dump_html(self, pattern="ALL", folder="."):
        """
        dumps all emails to a folder,
        it creates a subfolder for all inbox folder
        
        @param      pattern     ALL (only available option)
        @param      folder      folder where to dump
        @return                 list of dumped files
        """        
        if pattern != "ALL" :
            raise MailException("unavailable")
            
        res = [ ]
        
        def skip_function (mail) :
            if mail.isDumped(subfold, attach) :
                return True
        
        folders = self.folders()
        for fold in folders :
            self.fLOG("MailBoxImap: dumping folder ", fold)
            subfold = os.path.join(folder,fold)
            if not os.path.exists (subfold) :
                os.makedirs(subfold)
            attach = os.path.join(subfold, "_attachments")
            if not os.path.exists(attach) :
                os.makedirs(attach)
                
            for mail in self.enumerate_mails_in_folder(fold, skip_function = skip_function) :
                mail.dump_html(subfold, attach, fLOG = self.fLOG)
            
        


