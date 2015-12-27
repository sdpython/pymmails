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

    def __init__(self, tmpl=None, css=None):
        """
        constructor, defines a template to use based
        on `Jinja2 <http://jinja.pocoo.org/docs/dev/>`_

        @param      tmpl        template (string or file)
        @param      css         style
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

    def render(self, location, mail, file_css, attachments):
        """
        render a mail

        @paramp     location        location where this mail should be saved
        @param      mail            instance of @see cl EmailMessage
        @param      file_css        css file
        @param      attachments     attachments
        @return                     html, css (content)

        The mail is stored in object ``message``, ``css`` means the style sheet,
        ``render`` means this object, ``location`` means *store_location*,
        ``EmailMessage`` is the class *EmailMessage*, ``attachments`` is *attachments*::

            {{ message.get_subject() }}


        """
        css = self._css.render(mail)
        html = self._template.render(message=mail, css=file_css, render=self,
                                     location=location, EmailMessage=EmailMessage,
                                     attachments=attachments)
        return html, css

    def produce_table_html(self, email, location, toshow, tohighlight=None, atts=None, avoid=None,
                           style_table="dataframe100l", style_highlight="dataframe100l_hl"):
        """
        produces a table with the values of some fields of the message

        @param      toshow          list of fields to show, if None, it considers all fields
        @param      tohighlight     list of fields to highlights
        @param      atts            list of files to append at the end of the table,
                                    list of tuple ((filename,message_id,content_id))
        @param      location        folder where this page will be saved (for attachment)
        @param      avoid           fields to avoid
        @param      style_table     style for the table
        @param      style_highlight style for highlighted cells
        @return                     html string
        """
        if atts is None:
            atts = []
        if avoid is None:
            avoid = []
        rows = []
        rows.append('<div class="{0}">'.format(style_table))
        rows.append('<table border="1">')
        rows.append("<thead><tr><th>key</th><th>value</th></tr></thead>")
        for tu in sorted(email.items()):
            if toshow is not None and tu[0] not in toshow:
                continue
            if tu[0] in avoid:
                continue

            tu = (tu[0], email.decode_header(tu[0], tu[1]))

            if tohighlight and tu[0] in tohighlight:
                format = '<tr class="{0}"><th>{0}</th><td>{1}</td></tr>'.format(
                    style_highlight)
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
