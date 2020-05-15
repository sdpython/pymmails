# -*- coding: utf-8 -*-
"""
@file
@brief define an Email grabbed from a server.
"""

import os
import re
import json
import datetime
import email
from email.generator import BytesGenerator, Generator
import email.header
import email.message
from io import BytesIO, StringIO
import mimetypes
import hashlib
import warnings
from collections import OrderedDict
import dateutil.parser
from pyquickhelper.loghelper import noLOG

from .mail_exception import MailException
from .additional_mime_type import additional_mime_type_ext_type


class EmailMessage(email.message.Message):

    """
    overloads the message to class to add some
    functionalities such as a display using HTML
    """

    expMail1 = re.compile('(\\"([^;,]*?)\\" )?<([^;, ]+?@[^;, ]+)>')
    expMail2 = re.compile('(([^;,]*?) )?<([^;, ]+?@[^;, ]+)>')
    expMail3 = re.compile('(\\"([^;,]*?)\\" )?([^;, ]+?@[^;, ]+)')
    expMail4 = re.compile('((=[?]([^;,]+?)[?]=)? ?<([^;, ]+?@[^;, ]+)>)')
    expMailA = re.compile(
        '({0})|({1})|({2})'.format(
            expMail1.pattern,
            expMail2.pattern,
            expMail3.pattern))

    subset = ["Date", "From", "Subject", "To", "X-bcc"]
    avoid = ["X-me-spamcause", "X-YMail-OSG"]

    additionnalMimeType = additional_mime_type_ext_type
    _date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    def as_bytes(self):
        """
        converts the mail into a binary string

        @return     bytes

        See `Message.as_bytes <https://docs.python.org/3/library/email.message.html#email.message.Message.as_bytes>`_
        """
        fp = BytesIO()
        g = BytesGenerator(fp, mangle_from_=True, maxheaderlen=60)
        g.flatten(self)
        return fp.getvalue()

    def as_string(self, unixfrom=False, maxheaderlen=None, policy=None):
        """
        Converts the mail into a string.

        @return     string

        See `Message.as_string <https://docs.python.org/3/library/email.message.html#email.message.Message.as_string>`_
        """
        fp = StringIO()
        g = Generator(fp, mangle_from_=True, maxheaderlen=60)
        g.flatten(self)
        return fp.getvalue()

    @staticmethod
    def create_from_bytes(b):
        """
        Creates an instance of @see cl EmailMessage
        from a binary string (bytes) (see @see me as_bytes).

        @param      b       binary string
        @return             instance of @see cl EmailMessage
        """
        return email.message_from_bytes(b, _class=EmailMessage)

    @property
    def body(self):
        """
        return the body of the message
        """
        messages = []
        for part in self.walk():
            if part.get_content_type() == "text/html":
                b = part.get_payload(decode=1)
                if b is not None:
                    encs = [part.get_content_charset(), "utf8"]
                    s = None
                    for enc in encs:
                        try:
                            s = b.decode(enc)
                        except UnicodeDecodeError:
                            continue
                    if s is None:
                        raise UnicodeDecodeError(
                            "unable to decode: {0}".format(b))
                    messages.append(s)
        return "\n------------------------------------------\n\n".join(
            messages)

    def get_all_charsets(self, part=None):
        """
        returns all the charsets
        """
        if part is None:
            charsets = set({})
            for c in self.get_charsets():
                if c is not None:
                    charsets.update([c])
            return charsets
        else:
            charsets = set({})
            for c in part.get_charsets():
                if c is not None:
                    charsets.update([c])
            return charsets

    def get_nb_attachements(self):
        """
        return the number of attachments

        @return     int
        """
        r = 0
        for part in self.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            r += 1
        return r

    @property
    def body_html(self):
        """
        return the body of the messag
        """
        messages = []
        for part in self.walk():
            if part.get_content_type() == "text/html":
                b = part.get_payload(decode=1)
                if b is not None:
                    chs = list(self.get_all_charsets(part))
                    if len(chs) > 0:
                        try:
                            ht = b.decode(chs[0])
                        except UnicodeDecodeError:
                            try:
                                ht = b.decode("utf-8")
                            except UnicodeDecodeError:
                                try:
                                    ht = b.decode("latin-1")
                                except UnicodeDecodeError:
                                    raise Exception(
                                        "unable to decode (" + str(chs[0]) + "):" + str(b))
                    else:
                        try:
                            ht = b.decode("utf-8")
                        except UnicodeDecodeError:
                            ht = b.decode("utf-8", errors='ignore')
                            #raise MailException("unable to decode: " + str(b)) from e
                    htl = ht.lower()
                    pos = htl.find("<body")
                    pos2 = htl.find("</body>")
                    if pos != -1 and pos2 != -1:
                        ht = '<div ' + ht[pos + 5:pos2] + "</div>"
                    elif pos != -1:
                        ht = '<div ' + ht[pos + 5:] + "</div>"
                    elif pos2 != -1:
                        ht = '<div>' + ht[:pos2] + "</div>"
                    else:
                        ht = '<div>' + ht + "</div>"
                    messages.append(ht)
        text = "<hr />".join(messages)
        return text

    def enumerate_attachments(self):
        """
        enumerate the attachments as
        4-uple (filename, content, message_id, content_id)

        @return         iterator on tuple (filename, content, message_id, content_id)
        """
        for part in self.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            fileName = part.get_filename()
            fileName = self.decode_header("file", fileName)

            if fileName is not None and fileName.startswith(
                    "=?") and fileName.startswith("?="):
                fileName = fileName.strip("=?").split("=")[-1]

            if fileName is None or "?" in fileName:
                fileName = "unknown_type"
                cont = part.get_payload(decode=True)
                cont_id = part["Message-ID"]
                cont_id2 = part["Content-ID"]
                ext = EmailMessage.additionnalMimeType.get(
                    part.get_content_subtype(),
                    None)
                if ext is None:
                    ext = mimetypes.guess_extension(part.get_content_type())

                if ext is not None:
                    fileName += ext
                elif cont is not None:
                    if cont.startswith(b"%PDF"):
                        fileName += ".pdf"
                    elif part.get_content_maintype() == "text":
                        if cont.startswith(b"<html>"):
                            fileName += ".html"
                        else:
                            fileName += ".txt"
                    else:
                        raise MailException("unable to guess type: " +
                                            part.get_content_maintype() +
                                            "\nsubtype: " +
                                            str(part.get_content_subtype()) +
                                            " ext: " +
                                            str(ext) +
                                            " def: " +
                                            EmailMessage.additionnalMimeType.get(part.get_content_subtype(), "-") +
                                            "\n" +
                                            str([cont]))
            else:
                cont = part.get_payload(decode=True)
                cont_id = part[
                    "Message-ID"].strip("<>") if part["Message-ID"] else None
                cont_id2 = part[
                    "Content-ID"].strip("<>") if part["Content-ID"] else None

            yield fileName, cont, cont_id, cont_id2

    def __sortkey__(self):
        """
        usual
        """
        key = [self.get_date(), self.get_from(), self.get_to(),
               self.UniqueID, self["subject"]]
        for i, k in enumerate(key):
            if isinstance(k, tuple):
                if None in k:
                    key[i] = tuple("" if _ is None else _ for _ in k)
                elif k is None:
                    key[i] = ""
        return tuple(key)

    def __lt__(self, at):
        """
        usual
        """
        try:
            return self.__sortkey__() < at.__sortkey__()
        except TypeError as e:
            raise Exception("issue with\n{0}\n{1}".format(
                self.__sortkey__(), at.__sortkey__())) from e

    #: use for method @see me call_decode_header
    _search_encodings = ["iso-8859-1", "windows-1252", "UTF-8", "utf-8"]

    @staticmethod
    def call_decode_header(st, is_email=False):
        """
        call `email.header.decode_header <https://docs.python.org/3.4/library/email.header.html#email.header.decode_header>`_

        @param      st          string or `email.header.Header <https://docs.python.org/3.4/library/email.header.html#email.header.Header>`_
        @param      is_email    does something specific for emails
        @return                 text, encoding
        """
        if isinstance(st, email.header.Header):
            text, encoding = email.header.decode_header(st)[0]
            if isinstance(text, bytes):
                if encoding is None:
                    raise ValueError(
                        "encoding cannot be None if the returned string is bytes")
                if encoding == "unknown-8bit":
                    try:
                        res = text.decode("utf8")
                    except UnicodeDecodeError:
                        res = text.decode("ascii", errors="ignore")
                        # raise ValueError("encoding {0} is unexpected in\n{1}".format(encoding, st)) from e
                    return res, "ascii"
                else:
                    return text.decode(encoding), encoding
            else:
                return text, encoding
        elif isinstance(st, str):
            if is_email:
                zall = EmailMessage.expMail4.findall(st)
                if zall:
                    res = []
                    for add in zall:
                        head, enc = EmailMessage.call_decode_header(
                            add[0], is_email=False)
                        fin = "{0} <{1}>".format(head, add[-1])
                        res.append(fin)
                    return "; ".join(res), enc
                else:
                    return EmailMessage.call_decode_header(st, is_email=False)
            else:
                text, encoding = email.header.decode_header(st)[0]
                if isinstance(text, bytes):
                    position = None
                    if encoding is None:
                        # maybe the string contrains several encoding
                        for enc in EmailMessage._search_encodings:
                            look = "=?%s?" % enc
                            if look in st:
                                position = st.find(look)

                        if position == 0:
                            # otherwise we face an infinite loop
                            position = None

                        if position is not None:
                            first = st[:position]
                            second = st[position:]
                            dec1, enc1 = EmailMessage.call_decode_header(first)
                            dec2, enc2 = EmailMessage.call_decode_header(
                                second)

                            if isinstance(dec1, str) and isinstance(dec2, str):
                                enc = enc2 if enc1 is None else enc1
                                return dec1 + dec2, enc
                            else:
                                mes = ('decoding issue\n   File "{0}", line {1},\nunable to decode ' +
                                       'string:\n{2}\neven split into:\n1: {3}\n2: {4}')
                                warnings.warn(mes.format(__file__, 250, st.replace("\r", " ").replace("\n", " "),
                                                         first.replace("\r", " ").replace(
                                                             "\n", " "),
                                                         second.replace("\r", " ").replace("\n", " ")))
                                return st, None
                        else:
                            warnings.warn(
                                'decoding issue\n   File "{0}", line {1},\nunable to decode string:\n{2}'.format(
                                    __file__,
                                    260,
                                    st.replace(
                                        "\r",
                                        " ").replace(
                                        "\n",
                                        " ")))
                            return st, None
                    else:
                        return text.decode(encoding), encoding
                else:
                    return text, encoding
        else:
            raise TypeError("cannot decode type: {0}".format(type(st)))

    def get_from_str(self):
        """
        return a string for the receivers

        @return     string
        """
        l, a = self.get_from()
        res = []
        if l:
            res.append(l)
        else:
            res.append(a)
        return ";".join(res)

    def get_from(self):
        """
        returns a tuple (label, email address) or a list of groups
        from the regular expression

        @return     tuple       ( label, email address)
        """
        st = self["from"]
        if isinstance(st, email.header.Header):
            text, _ = EmailMessage.call_decode_header(st, is_email=True)
            if text is None:
                raise MailException(
                    "unable to parse: " +
                    str(text) +
                    "\n" +
                    str(st))
        else:
            text = st

        cp = EmailMessage.expMail1.search(text)
        if not cp:
            cp = EmailMessage.expMail2.search(text)
            if not cp:
                cp = EmailMessage.expMail3.search(text)
                if not cp:
                    if text.startswith('"=?utf-8?'):
                        text = text.strip('"')
                        text, _ = EmailMessage.call_decode_header(
                            text, is_email=True)
        gr = cp.groups()
        name, mail = gr[1], gr[2]
        if name is None:
            name = self.get_name(_fallback_get_from=False)
        elif name.startswith("=?"):
            name = EmailMessage.call_decode_header(name)[0]
            if name is None:
                name = gr[1]
        return name, mail

    def get_name(self, _fallback_get_from=True):
        """
        return the sender name of an email (if available)

        @param      _fallback_get_from      internal parameter, avoir recursion
        @return                             name (or None if not found)
        """
        st = self["from"]
        if isinstance(st, email.header.Header):
            text, _ = EmailMessage.call_decode_header(st, is_email=True)
            if text is None:
                raise MailException(
                    "unable to parse: " +
                    str(text) +
                    "\n" +
                    str(st))
        elif st.startswith("=?"):
            text, _ = EmailMessage.call_decode_header(st)
        else:
            text = st

        if "<" in text:
            r = text.split("<")[0].strip()
            return r if r else None
        elif text is None and _fallback_get_from:
            return self.get_from()[0]
        else:
            return text

    def get_to_str(self, cc=False, field="to"):
        """
        return a string for the receivers

        @param      cc      get receivers or second receivers
        @param      field   field to use, ``to`` or ``Delivered-To``
                            (the second one is used as a backup anyway)
        @return             string
        """
        to = self.get_to(cc=cc, field=field)
        res = []
        for li, a in to:
            if li:
                res.append(li)
            else:
                res.append(a)
        return ";".join(res)

    def get_to(self, cc=False, field="to"):
        """
        return the receivers

        @param      cc      get receivers or second receivers
        @param      field   field to use, ``to`` or ``Delivered-To``
                            (the second one is used as a backup anyway)
        @return             list of tuple [ ( label, email address) ]
        """
        st = self[field if not cc else "cc"]
        if st is None and not cc:
            st = self["Delivered-To"]
        if st is None:
            return None
        text, _ = EmailMessage.call_decode_header(st, is_email=True)
        if text is None:
            raise MailException("unable to parse: " + str(st))

        def find_unnone(ens):
            "local function"
            for c in ens:
                if c is not None:
                    return c
            return None

        text = text.replace("\r", " ").replace("\n", " ").replace("\t", " ")
        cp = []
        for st in EmailMessage.expMailA.finditer(text):
            gr = st.groups()
            if len(gr) != 12:
                raise MailException(
                    "unexpected error due to a change in regular expressions")
            values = gr[2], gr[3], gr[6], gr[7], gr[10], gr[11]
            label = find_unnone(values[::2])
            add = find_unnone(values[1::2])
            if label is not None:
                label = label.strip(" \r\n\t")
                text, _ = EmailMessage.call_decode_header(
                    label, is_email=True)
                if text.startswith('"=?utf-8?'):
                    text = text.strip('"')
                    text = EmailMessage.call_decode_header(
                        text, is_email=True)[0]
                cp.append((text, add))
            else:
                cp.append((None, add))

        return cp if cp else None

    def get_date(self):
        """
        return a datetime object for the field Date
        """
        st = self["Date"]
        res, _ = EmailMessage.call_decode_header(st)
        if res is None:
            raise MailException("unable to parse: " + str(st))

        try:
            p = dateutil.parser.parse(res)
        except Exception as e:
            # it can fail because of dates such as: Wed, 7 Oct 2009 11:43:56
            # +0200 (Paris, Madrid (heure d'\ufffdt\ufffd))
            if "(" in res:
                res = res[:res.find("(")]
                p = dateutil.parser.parse(res)
                return p
            else:
                if "," in res:
                    b = res.split(",")[1]
                    try:
                        p = dateutil.parser.parse(b)
                    except Exception as e:
                        raise MailException(
                            "unable to parse: " +
                            str(res) +
                            "\n" +
                            str(st)) from e
                else:
                    raise MailException(
                        "unable to parse: " +
                        str(res) +
                        "\n" +
                        str(st)) from e
        if p is None:
            raise MailException(
                "unable to parse: " +
                str(res) +
                "\n" +
                str(st))
        return p

    def get_date_str(self):
        """
        return the date into a string

        @return     date as a string (iso format)
        """
        return self.get_date().strftime(EmailMessage._date_format)

    def default_filename(self):
        """
        define a default filename (no extension)

        @return         str
        """
        b = self.get_from()[1]
        if len(b) == 0:
            raise MailException("from is unknown: " + self["from"])
        b = b.replace("@", "-at-").replace(".", "-")
        date = self.get_date()
        d = "%04d-%02d-%02d" % (date.year, date.month, date.day)
        f = "d_{0}_p_{1}_ii_{2}".format(d, b, self.UniqueID)
        return f.replace(
            "\\", "-").replace("\r", "").replace("\n", "-").replace("%", "-").replace("/", "-")

    @staticmethod
    def interpret_default_filename(name):
        """
        reverse engineer method @see me default_filename

        @param      name        filename
        @return                 dictionary

        The function creates a dictionary with keys date, from, uid, name.
        """
        pieces = name.split("_")
        res = {}
        for i, p in enumerate(pieces):
            if p == "d" and "date" not in res:
                res["date"] = pieces[i + 1]
            elif p == "p" and "from" not in res:
                res["from"] = pieces[i + 1]
            elif p == "ii" and "uid" not in res:
                res["uid"] = pieces[i + 1].split(".")[0]
        res["name"] = name
        return res

    @property
    def UniqueID(self):
        """
        builds a unique ID
        """
        md5 = hashlib.md5()
        t = self["Message-ID"]
        if t is not None:
            md5.update(t.encode('utf-8'))
        else:
            for f in ["Subject", "To", "From", "Date"]:
                if self[f] is not None:
                    md5.update(self[f].encode('utf-8'))
        return md5.hexdigest()

    def decode_header(self, field, st):
        """
        decode a string encoded in the header

        @param      field   field
        @param      st      string
        @return             string (it never return None)
        """
        if st is None:
            return ""
        elif isinstance(st, str):
            if st.startswith("Tr:") and field.lower() == "subject":
                pos = st.find("=?")
                return st[:pos] + self.decode_header(field, st[pos:])
            else:
                text, _ = EmailMessage.call_decode_header(st)
                return text if text is not None else ""
        elif isinstance(st, bytes):
            text, _ = EmailMessage.call_decode_header(st)
            return self.decode_header(field, text) if text is not None else ""
        elif isinstance(st, email.header.Header):
            text = EmailMessage.call_decode_header(st)[0]
            return self.decode_header(field, text) if text is not None else ""
        else:
            raise MailException(
                "unable to process type " + str(type(st)) + "\n" + str(st))

    def get_field(self, field):
        """
        get a field and cleans it

        @param      field       subject or ...
        @return                 text
        """
        subj = self[field]
        if subj is None:
            subj = self[field]
        if subj is not None:
            subj = self.decode_header(field, subj)
        return subj

    @property
    def Fields(self):
        """
        @return  list of available fields
        """
        return list(sorted(self.keys()))

    def to_dict(self):
        """
        Returns all fields for an emails as a dictionary
        @return     dictionary { key : value }
        """
        res = OrderedDict((k, self.get_field(k)) for k in self.Fields)
        res["attached"] = self.get_nb_attachements()
        return res

    def dump_attachments(self, attach_folder=".", buffer_write=None, metadata=True, fLOG=noLOG):
        """
        Dumps the mail into a folder using HTML format.
        If the destination files already exists, it skips it.
        If an attachments already has the same name, it chooses another one if
        the attachment is different (otherwise it keeps it as it is).

        @param      attach_folder   destination folder
        @param      buffer_write    None or instance of @see cl BufferFilesWriting
        @param      metadata        if True, also dump metadata about attachments
        @param      fLOG            logging function
        @return                     list of attachments

        The results is a list of 3-uple:

        * full name of the attachments
        * message id
        * content id

        The metadata contains information about the mail it comes from.
        The data is stored in a json format (except for date).
        It is stored in a file with extension ``.metadata``.
        """
        def local_exists(name):
            "local function"
            if buffer_write:
                return buffer_write.exists(name)
            else:
                return os.path.exists(name)

        def local_different(to, content):
            "local function"
            if buffer_write:
                c2 = buffer_write.read_binary_content(to)
            else:
                with open(to, "rb") as f:
                    c2 = f.read()
            return c2 != content

        atts = []
        for ai, att in enumerate(self.enumerate_attachments()):
            if att[1] is None:
                continue
            att_id = att[2]
            cont_id = att[3]
            to = os.path.split(att[0].replace(":", "_"))[-1]
            to = os.path.join(attach_folder, to)

            to = to.replace("\n", "_").replace("\r", "")
            to = os.path.abspath(to)
            spl = os.path.splitext(to)

            if "?" in to:
                raise MailException(
                    "issue with attachments (mail to {0})\n{1}".format(to, att))

            if local_exists(to):
                already = True
                # must be different otherwise we don't do anything
                different = local_different(to, att[1])
                if different:
                    i = 1
                    while local_exists(to):
                        to = spl[0] + (".(%d)" % i) + spl[1]
                        i += 1
            else:
                already = False
                different = True

            fLOG("[dump_attachments] attachment:", to,
                 "different={0} notnew={1}".format(different, already))

            if different:
                if metadata:
                    d2 = dict(index=ai, filename=os.path.split(to)[-1],
                              mail=self.default_filename() + ".html",
                              from_=self.get_from(), to=self.get_to(),
                              date=self.get_date_str(), uid=self.UniqueID)
                    d2 = OrderedDict(sorted(d2.items()))
                    st = StringIO()
                    json.dump(d2, st)
                    meta_text = st.getvalue()
                    meta_name = to + ".metadata"

                if buffer_write is None:
                    with open(to, "wb") as f:
                        f.write(att[1])
                    if metadata:
                        with open(meta_name, "r", encoding="utf8") as f:
                            f.write(meta_text)
                else:
                    f = buffer_write.open(to, text=False)
                    f.write(att[1])
                    if metadata:
                        f = buffer_write.open(meta_name, text=True)
                        f.write(meta_text)

            atts.append((to, att_id, cont_id))
        return atts

    def dump(self, render, location, attach_folder="attachments", fLOG=noLOG, **params):
        """
        Dumps a message using a call such as @see cl EmailMessageRenderer.

        @param      render          instance of class @see cl EmailMessageRenderer
        @param      location        location of the file to store
        @param      attach_folder   folder for the attachments, it will be created if it does not exist
        @param      buffer_write    None or instance of @see cl BufferFilesWriting
        @param      fLOG            logging function
        @param      params          others parameters, see
                                    :meth:`EmailMessageRenderer.write <pymmails.grabber.email_message_renderer.EmailMessageRenderer.write>`
        @return                     list of stored files
        """
        full_fold = os.path.join(location, attach_folder)
        atts = self.dump_attachments(full_fold,
                                     buffer_write=render.BufferWrite,
                                     fLOG=fLOG)
        return render.write(location=location, mail=self,
                            filename=params.get(
                                "filename", self.default_filename() + ".html"),
                            attachments=atts,
                            overwrite=params.get("overwrite", False),
                            file_css=params.get("file_css", "mail_style.css"),
                            encoding=params.get("encoding", "utf8"),
                            prev_mail=params.get("prev_mail", None),
                            next_mail=params.get("next_mail", None))

    @staticmethod
    def read_metadata(metafile):
        """
        read metadata assuming metafile contaings a json string

        @param      metafile        json string
        @return                     dictionary
        """
        if isinstance(metafile, str):
            if len(metafile) < 5000 and os.path.exists(metafile):
                with open(metafile, "r", encoding="utf8") as f:
                    d2 = json.load(f)
            else:
                f = StringIO(metafile)
                d2 = json.load(f)
        else:
            d2 = json.load(metafile)
        d2["date"] = datetime.datetime.strptime(
            d2["date"], EmailMessage._date_format)
        d2 = OrderedDict(sorted(d2.items()))
        return d2
