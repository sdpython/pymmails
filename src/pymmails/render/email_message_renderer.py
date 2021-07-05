# -*- coding: utf-8 -*-
"""
@file
@brief Functions to dump emails
"""
import os
import re
import pprint
from jinja2.exceptions import UndefinedError
from pyquickhelper.loghelper import noLOG
from ..grabber.email_message import EmailMessage
from ..helpers.buffer_files_writing import BufferFilesWriting
from .email_message_style import template_email_html, template_email_css
from .renderer import Renderer


class EmailMessageRenderer(Renderer):
    """
    defines way to render an email
    """

    def __init__(self, tmpl=None, css=None,
                 style_table="dataframe100l",
                 style_highlight="dataframe100l_hl",
                 buffer_write=None,
                 fLOG=noLOG):
        """
        Defines a template based
        on `Jinja2 <http://jinja.pocoo.org/docs/dev/>`_.

        @param      tmpl                template (string or file)
        @param      css                 style
        @param      style_table         style for the table
        @param      style_highlight     style for highlighted cells
        @param      buffer_write        instance of class @see cl BufferFilesWriting
        @param      fLOG                logging function

        @example(Template to render an email)

        See file :mod:`email_message_style <pymmails.grabber.email_message_style>`

        HTML template::

            <?xml version="1.0" encoding="utf-8"?>
            <body>
            <html>
            <head>
            <title>{{ message.get_field("subject") }}</title>
            <link rel="stylesheet" type="text/css" href="{{ css }}">
            </head>
            <body>
            {{ '<a href="{0}">&lt;--</a>'.format(prev_mail) if prev_mail else '' }}
            {{ '<a href="{0}">--&gt;</a>'.format(next_mail) if next_mail else '' }}
            <h1>{{ message.get_date().strftime('%Y/%m/%d') }} - {{ message.get_field("subject") }}</h1>
            <h2>attributes</h2>
            {{ render.produce_table_html(message, toshow=EmailMessage.subset, location=location, avoid=EmailMessage.avoid) }}
            <h2>message</h2>
            {{ render.process_body_html(location, message.body_html, attachments) }}
            <h2>full list of attributes</h2>
            {{ render.produce_table_html(message, toshow=message.Fields, location=location, tohighlight=EmailMessage.subset) }}
            </body>
            </html>

        CSS style::

            .dataframe100l {
                padding: 0;
                width=75%
                font-family: Calibri;
                font-size: 100%;
                cursor: pointer;
            }

            .dataframe100l table {
                border-collapse: collapse;
                text-align: left;
                font-size: 11px;
            }

            .dataframe100l table td, .dataframe100l table th {
                padding: 3px 6px;
            }

            .dataframe100l table thead th {
                background-color:#AAAAAA;
                color:#ffffff;
                font-size: 11px;
                font-weight: bold;
                border-left: 1px solid #0070A8;
            }

            .dataframe100l table tbody td {
                color: #00496B;
                border-left: 1px solid #E1EEF4;
                font-size: 11px;
                font-weight: normal;
            }

            .dataframe100l table tbody .alt td {
                background: #E1EEF4;
                color: #00496B;
                }

            .dataframe100l_hl td {
                background: #FFFF00;
                }

            .dataframe100l_hl th {
                background: #FFFF00;
                }

            .dataframe100l_hl tr {
                background: #FFFF00;
                }

            .dataframe100l table tbody td:first-child {
                border-left: none;
            }

            .dataframe100l table tbody tr:last-child td {
                border-bottom: none;
            }

            .dataframe100l table tfoot td div {
                border-top: 1px solid #006699;
                background: #E1EEF4;
            }

            .dataframe100l table tfoot td {
                padding: 0;
                font-size: 11px
            }

            .dataframe100l table tfoot td div{ padding: 2px; }
            .dataframe100l table tfoot td ul {
                margin: 0;
                padding:0;
                list-style: none;
                text-align: right;
            }

            .dataframe100l table tfoot  li { display: inline; }
            .dataframe100l table tfoot li a {
                text-decoration: none;
                display: inline-block;
                padding: 2px 8px;
                margin: 1px;
                color: #FFFFFF;
                border: 1px solid #006699;
                border-radius: 3px;
                background-color:#006699;
            }

            .dataframe100l table tfoot ul.active, .dataframe100l table tfoot ul a:hover {
                text-decoration: none;
                border-color: #006699;
                color: #FFFFFF;
                background: none;
                background-color:#00557F;
            }

        @endexample

        """
        if tmpl is None:
            _template = template_email_html
        elif len(tmpl) < 5000 and os.path.exists(tmpl):
            with open(tmpl, "r", encoding="utf8") as f:
                _template = f.read()
        else:
            _template = tmpl

        if css is None:
            _css = template_email_css
        elif len(css) < 5000 and os.path.exists(css):
            with open(css, "r", encoding="utf8") as f:
                _css = f.read()
        else:
            _css = css

        if buffer_write is None:
            buffer_write = BufferFilesWriting(fLOG=fLOG)
        Renderer.__init__(self, tmpl=_template, css=_css, style_table=style_table,
                          style_highlight=style_highlight, buffer_write=buffer_write, fLOG=fLOG)

    def render(self, location, mail, attachments,  # pylint: disable=W0221
               file_css="mail_style.css", prev_mail=None, next_mail=None, **addition):
        """
        Renders a mail.

        @paramp     location        location where this mail should be saved
        @param      mail            instance of @see cl EmailMessage
        @param      file_css        css file (where it is supposed to be stored)
        @param      attachments     attachments
        @param      prev_mail       previous mail (or None if there is none)
        @param      next_mail       next mail (or None if there is none)
        @param      addition        sent to *Jinja*
        @return                     html, css (content), attachments

        The mail is stored in object ``message``, ``css`` means the style sheet,
        ``render`` means this object, ``location`` means *location*,
        ``EmailMessage`` is the class *EmailMessage*, ``attachments`` is *attachments*::

            {{ message.get_subject() }}

        The value stored in *file_css* will be relative to *location*.

        """
        file_css = os.path.relpath(file_css, location)
        css = self._css.render(message=mail)
        try:
            html = self._template.render(message=mail, css=file_css, render=self,
                                         location=location, EmailMessage=EmailMessage,
                                         attachments=attachments, prev_mail=prev_mail,
                                         next_mail=next_mail, **addition)
        except UndefinedError as e:
            empty = []
            if 'groups' in addition:
                for gr in addition['groups']:
                    if 'emails' in gr and len(gr['emails']) == 0:
                        empty.append(gr)
            tmpl = self._raw_template
            disp1 = pprint.pformat(empty)
            mes = "This usually happens when the project was sent with a mail not retained in a the final list."
            raise RuntimeError("Unable to apply pattern\n----\n{0}\n----\n{1}\n----\n{2}".format(
                               mes, tmpl, disp1)) from e
        return html, css, attachments

    def write(self, location, mail, filename, attachments=None,  # pylint: disable=W0221
              overwrite=False, file_css="mail_style.css", encoding="utf8",
              prev_mail=None, next_mail=None, **addition):
        """
        Writes a mail, the function assumes the attachments were already dumped.

        @param      location        location
        @param      mail            instance of @see cl EmailMessage
        @param      attachments     list of attachments (see @see me dump_attachments)
        @param      overwrite       the function does not overwrite
        @param      file_css        css file (where it is supposed to be stored)
        @param      encoding        encoding
        @param      addition        additional parameter sent to Jinja2
        @param      prev_mail       previous mail (or None if there is none)
        @param      next_mail       next mail (or None if there is none)
        @return                     list of written local files, attachements
        """
        full_css = os.path.join(location, file_css)
        full_mail = os.path.join(location, filename)
        if not overwrite and self.BufferWrite.exists(full_css) and \
                self.BufferWrite.exists(full_mail):
            return [full_mail, full_css], attachments
        html, css, attachments = self.render(
            location, mail, attachments, file_css=full_css,
            prev_mail=prev_mail, next_mail=next_mail, **addition)
        if not self.BufferWrite.exists(full_css, local=not overwrite):
            f = self.BufferWrite.open(full_css, text=True, encoding=encoding)
            f.write(css)
        if not self.BufferWrite.exists(full_mail, local=not overwrite):
            f = self.BufferWrite.open(full_mail, text=True, encoding=encoding)
            f.write(html)
        return [full_mail, full_css], attachments

    def produce_table_html(self, email, location, toshow, tohighlight=None, atts=None, avoid=None):
        """
        produces a table with the values of some fields of the message

        @param      toshow          list of fields to show, if None, it considers all fields
        @param      tohighlight     list of fields to highlights
        @param      atts            list of files to append at the end of the table,
                                    list of tuple *((filename,message_id,content_id))*
        @param      location        folder where this page will be saved (for attachment)
        @param      avoid           fields to avoid
        @return                     html string
        """
        if atts is None:
            atts = []
        if avoid is None:
            avoid = []
        rows = []
        rows.append('<div class="{0}">'.format(self._style_table))
        rows.append('<table border="1">')
        rows.append("<thead><tr><th>key</th><th>value</th></tr></thead>")
        for tu in sorted(email.items()):
            if toshow is not None and tu[0] not in toshow:
                continue
            if tu[0] in avoid:
                continue

            tu = (tu[0], email.decode_header(tu[0], tu[1]))

            if tohighlight and tu[0] in tohighlight:
                format = '<tr class="%s"><th>{0}</th><td>{1}</td></tr>' % self._style_highlight
            else:
                format = "<tr><th>{0}</th><td>{1}</td></tr>"
            rows.append(format.format(
                        tu[0].replace("<", "&lt;").replace(">", "&gt;"),
                        tu[1].replace("<", "&lt;").replace(">", "&gt;")))

        for i, a in enumerate(atts):
            filename, _, cid = a
            rows.append('<tr><td>{0}</td><td><a href="{1}">{2}</a>{3}</td></tr>'.format(
                        "attachment %d" % (i + 1),
                        os.path.relpath(
                            filename, location) if location else filename,
                        os.path.split(filename)[-1],
                        "id={0}".format(cid) if cid else ""))

        rows.append("</table>")
        rows.append("<br /></div>")
        return "\n".join(rows)

    def process_body_html(self, location, body, atts):
        """
        replaces link to images included in the mail body::

            <img name="14a318e16161c62a_14a31789f7a34aae_null"
                 title="pastedImage.png"
                 src="cid:1146aa0a-244a-440e-8ea5-7b272c94f89a"
                 height="153.02644466209597"
                 width="560">

        @param      location    location where the HTML body will be saved
        @param      body        html body
        @param      atts        attachements (filename, message id, content id)
        @return                 modified body html
        """
        if atts:
            for filename, _, cid in atts:
                if cid is None:
                    continue
                pattern = 'src="cid:{0}"'.format(cid.strip("<>"))
                exp = re.compile('({0})'.format(pattern))
                fall = exp.findall(body)
                if len(fall) > 0:
                    relf = os.path.relpath(filename, location)
                    link = 'src="{0}"'.format(relf)
                    body = body.replace(pattern, link)
        return body
