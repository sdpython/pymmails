# -*- coding: utf-8 -*-
"""
@file
@brief Functions to dump emails
"""
import os
import re
from jinja2 import Template
from .email_message_style import template_email_html, template_email_css
from .email_message import EmailMessage


class EmailMessageRenderer:
    """
    defines way to render an email
    """

    def __init__(self, tmpl=None, css=None,
                 style_table="dataframe100l",
                 style_highlight="dataframe100l_hl"):
        """
        constructor, defines a template to use based
        on `Jinja2 <http://jinja.pocoo.org/docs/dev/>`_

        @param      tmpl            template (string or file)
        @param      css             style
        @param      style_table     style for the table
        @param      style_highlight style for highlighted cells

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
            <h1>{{ message.get_date().strftime('%Y/%M/%d') }} - {{ message.get_field("subject") }}</h1>
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
            self._template = template_email_html
        elif len(tmpl) < 5000 and os.path.exists(tmpl):
            with open(tmpl, "r", encoding="utf8") as f:
                self._template = f.read()
        else:
            self._template = tmpl

        if css is None:
            self._css = template_email_css
        elif len(css) < 5000 and os.path.exists(css):
            with open(css, "r", encoding="utf8") as f:
                self._css = f.read()
        else:
            self._css = css

        self._template = Template(self._template)
        self._css = Template(self._css)
        self._style_table = style_table
        self._style_highlight = style_highlight

    def render(self, location, mail, attachments, file_css="mail_style.css"):
        """
        render a mail

        @paramp     location        location where this mail should be saved
        @param      mail            instance of @see cl EmailMessage
        @param      file_css        css file (where it is supposed to be stored)
        @param      attachments     attachments
        @return                     html, css (content)

        The mail is stored in object ``message``, ``css`` means the style sheet,
        ``render`` means this object, ``location`` means *store_location*,
        ``EmailMessage`` is the class *EmailMessage*, ``attachments`` is *attachments*::

            {{ message.get_subject() }}

        The value stored in *file_css* will be relative to *location*.

        """
        file_css = os.path.relpath(file_css, location)
        css = self._css.render(mail)
        html = self._template.render(message=mail, css=file_css, render=self,
                                     location=location, EmailMessage=EmailMessage,
                                     attachments=attachments)
        return html, css

    def produce_table_html(self, email, location, toshow, tohighlight=None, atts=None, avoid=None):
        """
        produces a table with the values of some fields of the message

        @param      toshow          list of fields to show, if None, it considers all fields
        @param      tohighlight     list of fields to highlights
        @param      atts            list of files to append at the end of the table,
                                    list of tuple ((filename,message_id,content_id))
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
            filename, mid, cid = a
            rows.append('<tr><td>{0}</td><td><a href="{1}">{2}</a> (size: {3} bytes, cid: {4})</td></tr>'.format(
                        "attachment %d" % i,
                        os.path.relpath(
                            filename, location) if location else filename,
                        os.path.split(filename)[-1],
                        os.stat(filename).st_size,
                        cid))

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
            for filename, mid, cid in atts:
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

    def write(self, location, mail, filename, attachments=None, overwrite=False, file_css="mail_style.css", encoding="utf8"):
        """
        writes a mail, the function assumes the attachments were already dumped

        @param      location        location
        @param      mail            instance of @see cl EmailMessage
        @param      attachments     list of attachments (see @see me dump_attachments)
        @param      overwrite       the function does not overwrite
        @param      file_css        css file (where it is supposed to be stored)
        @param      encoding        encoding
        @return                     list of written local files
        """
        full_css = os.path.join(location, file_css)
        full_mail = os.path.join(location, filename)
        if not overwrite and os.path.exists(full_css) and os.path.exists(full_mail):
            return [full_mail, full_css]
        html, css = self.render(location, mail, attachments, file_css=full_css)
        if overwrite or not os.path.exists(full_css):
            with open(full_css, "w", encoding=encoding) as f:
                f.write(css)
        if overwrite or not os.path.exists(full_mail):
            with open(full_mail, "w", encoding=encoding) as f:
                f.write(html)
        return [full_mail, full_css]
