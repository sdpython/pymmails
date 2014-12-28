# -*- coding: utf-8 -*-
"""
@file
@brief define an Email grabbed from a server.
"""

import sys, os, imaplib, re, email, email.header, email.message, datetime, dateutil.parser, mimetypes, hashlib, warnings

from .email_message_style import html_header_style
from .mail_exception import MailException
from .additional_mime_type import additional_mime_type_ext_type

class EmailMessage (email.message.Message) :
    """
    overloads the message to class to add some
    functionalities such as a display using HTML
    """
    
    expMail1 = re.compile('(\\"([^;,]*?)\\" )?<([^;, ]+?@[^;, ]+)>')
    expMail2 = re.compile('(([^;,]*?) )?<([^;, ]+?@[^;, ]+)>')
    expMail3 = re.compile('(\\"([^;,]*?)\\" )?([^;, ]+?@[^;, ]+)')
    expMailA = re.compile('({0})|({1})|({2})'.format(expMail1.pattern,expMail2.pattern,expMail3.pattern))
    
    subset  = [ "Date", "From", "Subject", "To", "X-bcc" ]
    avoid   = [ "X-me-spamcause", "X-YMail-OSG" ]
    
    html_header = html_header_style
    additionnalMimeType = additional_mime_type_ext_type
    
    
    @property
    def body(self):
        """
        return the body of the message
        """
        messages = []
        for part in self.walk():
            if part.get_content_type() == "text/html":
                b =  part.get_payload(decode=1)
                if b != None :
                    encs = [ part.get_content_charset(), "utf8" ]
                    s = None
                    for enc in encs:
                        try:
                            s = b.decode(enc)
                        except UnicodeDecodeError:
                            continue
                    if s is None:
                        raise UnicodeDecodeError("unable to decode: {0}".format(b))
                    messages.append(s)
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
                        try :
                            ht = b.decode(chs[0])
                        except UnicodeDecodeError as e :
                            try :
                                ht = b.decode("utf-8")
                            except UnicodeDecodeError as e :
                                try :
                                    ht = b.decode("latin-1")
                                except UnicodeDecodeError as e :
                                    raise Exception("unable to decode (" + str(chs[0]) + "):" + str(b))
                    else :
                        try :
                            ht = b.decode("utf-8")
                        except UnicodeDecodeError :
                            ht = b.decode("utf-8", errors='ignore')
                            #raise MailException("unable to decode: " + str(b)) from e
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
        text = "<hr />".join(messages)
        return text
    
    def enumerate_attachments(self):
        """
        enumerate the attachments as 
        3-uple (filename, content, content_id)
        
        @return         iterator on tuple (filename, content, content_id)
        """
        for part in self.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            fileName = part.get_filename()
            fileName = self.decode_header("file",fileName)
            
            if fileName is not None and fileName.startswith("=?") and fileName.startswith("?=") :
                fileName = fileName.strip("=?").split("=")[-1]
                
            if fileName is None or "?" in fileName :
                fileName = "unknown_type"
                cont = part.get_payload(decode=True)
                cont_id = part["Message-ID"]
                ext = EmailMessage.additionnalMimeType.get(part.get_content_subtype(),None)
                if ext == None :
                    ext = mimetypes.guess_extension(part.get_content_type())
                    
                if ext != None :
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
                        raise MailException("unable to guess type: " + part.get_content_maintype() + "\nsubtype: " + str(part.get_content_subtype()) + " ext: " + str(ext) + " def: " + EmailMessage.additionnalMimeType.get(part.get_content_subtype(),"-") +"\n" + str([cont]))
            else :
                cont = part.get_payload(decode=True)
                cont_id = part["Message-ID"]
            yield fileName, cont, cont_id
            
    def __sortkey__(self):
        """
        usual
        """
        return "-".join( [ str(self.get_date()), str(self.get_from()), str(self.get_to()), self.UniqueID, self["subject"] ] )
            
    def __lt__(self, at):
        """
        usual
        """
        return self.__sortkey__() < at.__sortkey__()
            
    @staticmethod
    def call_decode_header(st):
        """
        call `email.header.decode_header <https://docs.python.org/3.4/library/email.header.html#email.header.decode_header>`_
        
        @param      st      string or `email.header.Header <https://docs.python.org/3.4/library/email.header.html#email.header.Header>`_
        @return             text, encoding
        """
        if isinstance(st, email.header.Header):
            text, encoding = email.header.decode_header(st)[0]
            if isinstance(text, bytes):
                if encoding is None:
                    raise ValueError("encoding cannot be None if the returned string is bytes")
                return text.decode(encoding), encoding
            else:
                return text, encoding
        elif isinstance(st, str):
            text, encoding = email.header.decode_header(st)[0]
            if isinstance(text, bytes):
                if encoding is None:
                    warnings.warn ('   File "{0}", line {1}, unable to decode string {2}'.format(__file__, 189, st.replace("\r"," ").replace("\n", " ")))
                    return st, None
                else:
                    return text.decode(encoding), encoding
            else:
                return text, encoding
        else:
            raise TypeError("cannot decode type: {0}".format(type(st)))
        
    def get_from(self):
        """
        returns a tuple (label, email address)
        
        @return     tuple ( label, email address) 
        """
        st = self["from"]
        if isinstance(st, email.header.Header):
            text, encoding = EmailMessage.call_decode_header(st)
            if res is None :
                raise MailException("unable to parse: " + str(res) + "\n" + str(st))
        else : 
            text = st
        
        cp = EmailMessage.expMail1.search(text)
        if not cp :
            cp = EmailMessage.expMail2.search(text)
            if not cp :
                cp = EmailMessage.expMail3.search(text)
                if not cp :
                    if text.startswith('"=?utf-8?'):
                        text = text.strip('"')
                        text, encoding = EmailMessage.call_decode_header(text)
        gr = cp.groups()
        return gr[1],gr[2]
        
    def get_to(self, cc=False):
        """
        return the receivers
        
        @param      cc      get receivers or second receivers
        @return             list of tuple [ ( label, email address) ]
        """
        st = self["to" if not cc else "Delivered-To"]
        text, encoding = EmailMessage.call_decode_header(st)
        if text is None :
            raise MailException("unable to parse: " + str(st))
            
        def find_unnone(ens):
            for c in ens:
                if c is not None:
                    return c
            return None
        
        text = text.replace("\r"," ").replace("\n"," ").replace("\t", " ")
        cp = [ ]
        for st in EmailMessage.expMailA.finditer(text) :
            gr = st.groups()
            if len(gr)!=12:
                raise Exception("unexpected error due to a change in regular expressions")
            values = gr[2],gr[3],gr[6],gr[7],gr[10],gr[11]
            label = find_unnone(values[::2])
            add   = find_unnone(values[1::2])
            if label is not None:
                label = label.strip(" \r\n\t")
                text, encoding = EmailMessage.call_decode_header(label)
                if text.startswith('"=?utf-8?'):
                    text = text.strip('"')
                    text, encoding = EmailMessage.call_decode_header(text)
                cp.append((text,add))
            else:
                cp.append((None,add))
                    
        return cp
        
    def get_date(self):
        """
        return a datetime object for the field Date
        """
        st = self["Date"]
        res, encoding = EmailMessage.call_decode_header(st)
        if res is None :
            raise MailException("unable to parse: " + str(st))
        
        try :
            p = dateutil.parser.parse(res)
        except Exception as e :
            # it can fail because of dates such as: Wed, 7 Oct 2009 11:43:56 +0200 (Paris, Madrid (heure d'\ufffdt\ufffd))
            if "(" in res :
                res = res[:res.find("(")]
                p = dateutil.parser.parse(res)
                return p
            else :
                if "," in res :
                    a,b = res.split(",")
                    try :
                        p = dateutil.parser.parse(b)
                    except Exception as e :
                        raise MailException("unable to parse: " + str(res) + "\n" + str(st)) from e
                else :
                    raise MailException("unable to parse: " + str(res) + "\n" + str(st)) from e
        if p == None :
            raise MailException("unable to parse: " + str(res) + "\n" + str(st))
        return p
            
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
        f = "d_{0}_p_{1}_ii_{2}".format(d, b, self.UniqueID)
        return f.replace("\\","-").replace("\r","").replace("\n","-").replace("%","-").replace("/","-")
        
    @property
    def UniqueID(self):
        """
        builds a unique ID 
        """
        md5 = hashlib.md5()
        t = self["Message-ID"]
        if t != None :
            md5.update(t.encode('utf-8'))
        else :
            for f in ["Subject", "To", "From", "Date"] :
                if self[f] != None : 
                    md5.update(self[f].encode('utf-8'))
        return md5.hexdigest()
        
    def decode_header(self, field, st):
        """
        decode a string encoded in the header
        
        @param      field   field
        @param      st      string
        @return             string (it never return None)
        """
        if st is None :
            return ""
        elif isinstance(st, str) :
            if st.startswith("Tr:") and field.lower() == "subject":
                pos = st.find("=?")
                return st[:pos] + self.decode_header(field, st[pos:])
            else:
                text, encoding = EmailMessage.call_decode_header(st)
                return text if text is not None else ""
        elif isinstance(st,bytes):
            text, encoding = EmailMessage.call_decode_header(st)
            return self.decode_header(field, text) if text is not None else ""
        elif isinstance(st, email.header.Header):
            text, encoding = EmailMessage.call_decode_header(st)
            return self.decode_header(field, text) if text is not None else ""
        else :
            raise MailException("unable to process type " + str(type(st)) + "\n" + str(st))

    def get_field(self, field):
        """
        get a field and cleans it
        
        @param      field       subject or ...
        @return                 text
        """
        subj = self[field]
        if subj == None : subj = self[field]
        if subj is not None:
            subj = self.decode_header(field,subj)
        return subj
        
    @property
    def Fields(self):
        """
        @return  list of available fields
        """
        return list(self.keys())
        
    def is_dumped(self, folder=".", attachfolder=".", filename = None):
        """
        @see me isDumped
        """
        return self.isDumped(folder=folder, attachfolder=attachfolder, filename=filename)
            
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
        
    def produce_table_html(self, toshow, tohighlight, folder, atts = [ ], avoid = []):
        """
        produces a table with the values of some fields of the message
        
        @param      toshow          list of fields to show, if None, it considers all fields
        @param      tohighlight     list of fields to highlights
        @param      atts            list of files to append at the end of the table
        @param      folder          folder where this page will be saved
        @param      avoid           fields to avoid
        @return                     html string
        """
        rows = []
        rows.append('<div class="dataframe100l">')
        rows.append('<table border="1">')
        rows.append("<thead><tr><th>key</th><th>value</th></tr></thead>")
        for tu in sorted(self.items()) :
            if toshow != None and tu[0] not in toshow : 
                continue
            if tu[0] in avoid :
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
        rows.append("<br /></div>")
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
            att_id = att[2]
            to = os.path.split(att[0].replace(":","_"))[-1]
            to = os.path.join(attachfolder, to)
            spl = os.path.splitext(to)
            i = 1
            while os.path.exists(to) :
                to = spl[0] + (".%d" % i) + spl[1]
                i += 1
        
            to = to.replace("\n","_").replace("\r","")
            to = os.path.abspath(to)
            if "?" in to :
                raise MailException("issue with " + filename + " \n + "  +to + "\n" + str(att))
            fLOG("dump attachment:", to)
            with open(to, "wb") as f :
                f.write(att[1])
                
            atts.append(to)
        
        subj = self["subject"]
        if subj == None : subj = self["subject"]
        if subj == None : subj = "none"
        subj = self.decode_header("subject",subj)
            
        rows = [ EmailMessage.html_header.replace("__TITLE__",subj) ]
        
        table1 = self.produce_table_html(EmailMessage.subset, [], folder, 
                                    atts, avoid = EmailMessage.avoid)
        rows.append(table1)

        rows.append('<div class="bodymail">')
        rows.append(self.body_html)
        
        rows.append ( "</div>")
        
        table2 = self.produce_table_html(None, EmailMessage.subset, folder, 
                                    avoid = EmailMessage.avoid)
        rows.append(table2)
        
        rows.append ("</body>\n</html>" )
        
        body = "\n".join(rows)
        
        fLOG("dump mail:", filename, "(", self.default_filename(),")")
        with open(filename,"w",encoding="utf8") as f :
            f.write(body)
            
        return filename
                


