# coding: latin-1
"""
@file
@brief define an Email grabbed from a server.
"""

import sys, os, imaplib, re, email, email.message, datetime, dateutil.parser, mimetypes

from .email_message_style import html_header_style
from .mail_exception import MailException


class EmailMessage (email.message.Message) :
    """
    overloads the message to class to add some
    functionalities such as a display using HTML
    """
    
    expMail1 = re.compile('(\\"(.*?)\\" )?<(.+?@.+?)>')
    expMail2 = re.compile('((.*?) )?<(.+?@.+?)>')
    expMail3 = re.compile('(\\"(.*?)\\" )?(.+?@.+?)')
    
    subset  = [ "Date", "From", "Subject", "To", "X-bcc" ]
    avoid   = [ "X-me-spamcause", "X-YMail-OSG" ]
    
    html_header = html_header_style
    
    
    @property
    def body(self):
        """
        return the body of the messag
        """
        messages = []
        for part in self.walk():
            if part.get_content_type() == "text/html":
                b =  part.get_payload(decode=1)
                if b != None :
                    messages.append(b.decode("utf8"))
        return "\n------------------------------------------\n\n".join(messages)
        
    def get_all_charsets(self, part = None):
        """
        returns all the charsets
        """
        if part == None :
            charsets = set({})
            for c in self.get_charsets():
                if c is not None:
                    charsets.update([c])
            return charsets        
        else :
            charsets = set({})
            for c in part.get_charsets():
                if c is not None:
                    charsets.update([c])
            return charsets        
    
    @property
    def body_html(self):
        """
        return the body of the messag
        """
        messages = []
        for part in self.walk():
            if part.get_content_type() == "text/html":
                b =  part.get_payload(decode=1)
                if b != None :
                    chs = list(self.get_all_charsets(part))
                    if len(chs) > 0 :
                        ht = b.decode(chs[0])
                    else :
                        ht = b.decode("utf_8")
                    htl = ht.lower()
                    pos = htl.find("<body")
                    pos2 = htl.find("</body>")
                    if pos != -1 and pos2 != -1 :
                        ht = '<div ' + ht[pos+5:pos2] + "</div>"
                    elif pos != -1 :
                        ht = '<div ' + ht[pos+5:] + "</div>"
                    elif pos2 != -1 :
                        ht = '<div>' + ht[:pos2] + "</div>"
                    else :
                        ht = '<div>' + ht + "</div>"
                    messages.append(ht)
        return "<hr />".join(messages)
    
    def set_id(self,num):
        """
        defines an id for the message
        
        @param  num id of the message
        """
        self._myid = num
            
    def enumerate_attachments(self):
        """
        enumerate the attachments as 
        2-uple (filename, content)
        """
        for part in self.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            fileName = part.get_filename()
            fileName = self.decode_header("file",fileName)
            
            if fileName != None and fileName.startswith("=?") and fileName.startswith("?=") :
                fileName = fileName.strip("=?").split("=")[-1]
                
            if fileName == None or "?" in fileName :
                fLOG ("w, ** issue with type", part.get_content_maintype(), " fileName",fileName)
                fileName = "unknown_type"
                cont = part.get_payload(decode=True)
                ext = mimetypes.guess_extension(part.get_content_type())
                if ext != None :
                    fLOG("w, ** mime ", part.get_content_type(), " ** ", ext)
                    fileName += ext
                elif cont != None :
                    if cont.startswith(b"%PDF") :
                        fileName += ".pdf"
                    elif part.get_content_maintype() == "text":
                        if cont.startswith(b"<html>") :
                            fileName + ".html"
                        else :
                            fileName + ".txt"
                    else :
                        raise MailException("unable to guess type: " + part.get_content_maintype() + "\nsubtype: " + str(part.get_content_subtype()) + "\n" + str([cont]))
            else :
                cont = part.get_payload(decode=True)
            yield fileName, cont
            
    def get_from(self):
        """
        returns a tuple (label, email address)
        """
        cp = EmailMessage.expMail1.search(self["from"])
        if not cp :
            cp = EmailMessage.expMail2.search(self["from"])
            if not cp :
                cp = EmailMessage.expMail3.search(self["from"])
                if not cp :
                    raise MailException("unable to interpret: " + self["from"])
        gr = cp.groups()
        return gr[1],gr[2]
        
    def get_date(self):
        """
        return a datetime object
        """
        return dateutil.parser.parse(self["Date"])
            
    def default_filename(self):
        """
        define a default filename (no extension)
        
        @return         str
        """
        a,b = self.get_from()
        if len(b) == 0 :
            raise MailException("from is unknown: " + self["from"])
        b = b.replace("@","-").replace(".","_")
        date = self.get_date()
        d = "%04d-%02d-%02d"%(date.year, date.month, date.day)
        f = "d_{0}_i_{1}_f_{2}".format(d, self._myid, b)
        return f

    def decode_header(self, field, st):
        """
        decode a string encoded in the header
        
        @param      field   field
        @param      st      string
        @return             string
        """
        if st == None :
            return ""
        elif st.startswith("Tr:") and field.lower() == "subject":
            pos = st.find("=?")
            return st[:pos] + self.decode_header(field, st[pos:])
        elif isinstance(st,bytes):
            text, encoding = email.header.decode_header(st)[0]
            return text.decode(encoding) if encoding != None else st
        elif isinstance(st,str):
            text, encoding = email.header.decode_header(st)[0]
            return text.decode(encoding) if encoding != None else st
        else :
            raise MailException("unable to process type " + str(type(st)))

    def isDumped(self, folder=".", attachfolder=".", filename = None):
        """
        checks if the email was already dumped
        
        @param  folder          destination folder 
        @param  attachments     destination folder for the attachments
        @param  filename        filename or a default one if None (see meth default_filename)
        @return                 boolean
        """
        if filename == None :
            filename = self.default_filename() + ".html"
        
        filename = os.path.abspath(os.path.join(folder,filename))
        if os.path.exists(filename) :
            return True
        return False
        
    def produce_table_html(self, toshow, tohighlight, folder, atts = [ ]):
        """
        produces a table with the values of some fields of the message
        
        @param      toshow          list of fields to show, if None, it considers all fields
        @param      tohighlight     list of fields to highlights
        @param      atts            list of files to append at the end of the table
        @param      folder          folder where this page will be saved
        @return                     html string
        """
        rows = []
        rows.append('<div class="dataframe100l">')
        rows.append('<table border="1">')
        rows.append("<thead><tr><th>key</th><th>value</th></tr></thead>")
        for tu in sorted(self.items()) :
            if toshow != None and tu[0] not in toshow : 
                continue
            
            tu = (tu[0], self.decode_header(tu[0], tu[1]))
            
            if tu[0] in tohighlight :
                rows.append('<tr><th style="background-color: yellow;">{0}</th><td style="background-color: yellow;">{1}</td></tr>'.format(
                            tu[0].replace("<","&lt;").replace(">","&gt;"),
                            tu[1].replace("<","&lt;").replace(">","&gt;")))
            else :
                rows.append("<tr><th>{0}</th><td>{1}</td></tr>".format(
                            tu[0].replace("<","&lt;").replace(">","&gt;"),
                            tu[1].replace("<","&lt;").replace(">","&gt;")))
                            
        for i,a in enumerate(atts) :
            rows.append('<tr><td>{0}</td><td><a href="{1}">{2}</a> (size: {3} bytes)</td></tr>'.format(
                        "attachment %d" %i, 
                        os.path.relpath(a, folder), 
                        os.path.split(a)[-1],
                        os.stat(a).st_size))
            
        rows.append("</table>")
        rows.append("</div><br />")
        return "\n".join(rows)
        
    def dump_html(self, folder=".", attachfolder=".", filename = None, fLOG = print):
        """
        Dumps the mail into a folder using HTML format.
        If the destination files already exists, it skips it.
        If an attachments already has the same name, it chooses another one.
        
        @param  folder          destination folder 
        @param  attachments     destination folder for the attachments
        @param  filename        filename or a default one if None (see meth default_filename)
        @param  fLOG            logging function
        @return                 html filename
        """
        if filename == None :
            filename = self.default_filename() + ".html"
        
        filename = os.path.abspath(os.path.join(folder,filename))
        if os.path.exists(filename) :
            fLOG("skip file {0} already exists".format(filename))
            return filename
            
        atts = [ ]
        for att in self.enumerate_attachments():
            if att[1] == None : continue
            to = os.path.join(attachfolder, att[0].replace(":","_"))
            spl = os.path.splitext(to)
            i = 1
            while os.path.exists(to) :
                to = spl[0] + (".%d" % i) + spl[1]
                i += 1
        
            to = os.path.abspath(to)
            if "?" in to :
                raise MailException("issue with " + filename + " \n + "  +to + "\n" + str(att))
            fLOG("dump attachment:", to)
            with open(to, "wb") as f :
                f.write(att[1])
                
            atts.append(to)
        
        subj = self["Subject"]
        if subj == None : subj = self["subject"]
        if subj == None : subj = "none"
        subj = self.decode_header("subject",subj)
            
        rows = [ EmailMessage.html_header.replace("__TITLE__",subj) ]
        
        table1 = self.produce_table_html(EmailMessage.subset, [], folder, atts)
        rows.append(table1)

        rows.append('<div class="bodymail">')
        rows.append(self.body_html)
        
        rows.append ( "</div>")
        
        table2 = self.produce_table_html(None, EmailMessage.subset, folder)
        rows.append(table2)
        
        rows.append ("</body>\n</html>" )
        
        body = "\n".join(rows)
        
        fLOG("dump mail:", filename)
        with open(filename,"w",encoding="utf8") as f :
            f.write(body)
            
        return filename
                


