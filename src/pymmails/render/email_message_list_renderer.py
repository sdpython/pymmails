# -*- coding: utf-8 -*-
"""
@file
@brief Functions to dump emails
"""
import os
import datetime
import json
from jinja2 import Template
from pyquickhelper.loghelper import noLOG
from ..helpers import iterator_prev_next
from .renderer import Renderer
from .email_message_style import template_email_list_html_iter, template_email_list_html_begin
from .email_message_style import template_email_list_html_end, template_email_css


class EmailMessageListRenderer(Renderer):
    """
    Defines a way to render a list of emails with a template
    template based on `Jinja2 <http://jinja.pocoo.org/docs/dev/>`_.

    .. exref::
        :title: Render a list of emails

        The following example extracts all mails in a folder of a gmail inbox,
        dumps them in a folder and produces a summary which connects to them.

        ::

            from pymmails import EmailMessageRenderer, EmailMessageListRenderer, MailBoxImap
            box = MailBoxImap(user, pwd, server)
            box.login()
            mails = box.enumerate_mails_in_folder("<your_folder)")

            email_render = EmailMessageRenderer()

            render = EmailMessageListRenderer(title="list of mails", email_renderer=email_render)
            render.write(iter=mails, location=temp, filename="summary.html")
            box.logout())
            render.flush()
    """

    def __init__(self, title, email_renderer, tmpl_begin=None, tmpl_iter=None, tmpl_end=None,
                 css=None, style_table="dataframe100l", style_highlight="dataframe100l_hl",
                 buffer_write=None, fLOG=noLOG):
        """
        @param      title               title
        @param      email_renderer      email renderer (see @see cl EmailMessageRenderer)
        @param      tmpl_begin          template which begins the summary
        @param      tmpl_iter           template which adds an element
        @param      tmpl_end            template which ends the summary
        @param      css                 template style
        @param      style_table         style for the table
        @param      style_highlight     style for highlighted cells
        @param      buffer_write        instance of class @see cl BufferFilesWriting
        @param      fLOG                logging function
        """
        if tmpl_begin is None:
            _template_begin = template_email_list_html_begin
        elif len(tmpl_begin) < 5000 and os.path.exists(tmpl_begin):
            with open(tmpl_begin, "r", encoding="utf8") as f:
                _template_begin = f.read()
        else:
            _template_begin = tmpl_begin

        if tmpl_iter is None:
            _template_iter = template_email_list_html_iter
        elif len(tmpl_iter) < 5000 and os.path.exists(tmpl_iter):
            with open(tmpl_iter, "r", encoding="utf8") as f:
                _template_iter = f.read()
        else:
            _template_iter = tmpl_iter

        if tmpl_end is None:
            _template_end = template_email_list_html_end
        elif len(tmpl_end) < 5000 and os.path.exists(tmpl_end):
            with open(tmpl_end, "r", encoding="utf8") as f:
                _template_end = f.read()
        else:
            _template_end = tmpl_end

        if css is None:
            _css = template_email_css
        elif len(css) < 5000 and os.path.exists(css):
            with open(css, "r", encoding="utf8") as f:
                _css = f.read()
        else:
            _css = css

        if buffer_write is None:
            buffer_write = email_renderer.BufferWrite

        Renderer.__init__(self, tmpl=_template_iter, css=_css, style_table=style_table,
                          style_highlight=style_highlight, buffer_write=buffer_write, fLOG=fLOG)

        self._email_renderer = email_renderer
        self._template_begin = Template(_template_begin)
        self._template_end = Template(_template_end)
        self._title = title

    def render(self, location, iter, attachments=None,  # pylint: disable=W0237
               file_css="mail_style.css"):
        """
        Renders a mail.

        @paramp     location        location where this mail should be saved
        @param      iter            iterator on tuple (object, function to call to render the object)
        @param      attachments     used to produce a JSON list
        @param      file_css        css file (where it is supposed to be stored)
        @return                     html, css (content), attachements as JSON

        The method populate fields ``now``, ``message``, ``css``, ``render``, ``location``, ``title``.
        """
        now = datetime.datetime.now()
        file_css = os.path.relpath(file_css, location)
        content = []
        self.fLOG("[EmailMessageListRenderer.render] begin")
        css = self._css.render()
        h = self._template_begin.render(css=file_css, render=self,
                                        location=location, title=self._title, now=now)
        content.append(h)
        self.fLOG("[EmailMessageListRenderer.render] iterate")

        def iter_on_mail():
            "local function"
            for i, mail3 in enumerate(iterator_prev_next(sorted(iter))):
                prev, item, next = mail3
                if i % 10 == 9:
                    self.fLOG(
                        "[EmailMessageListRenderer.render] iterate", i + 1)
                if not isinstance(item, tuple):
                    raise TypeError(
                        "expects a tuple (EmailMessage, function to render) not {0}".format(type(item)))
                prev_mail = prev[0].default_filename() + \
                    ".html" if prev else None
                next_mail = next[0].default_filename() + \
                    ".html" if next else None
                obj, f = item
                f(obj, location, prev_mail, next_mail)
                yield prev[0] if prev else None, item[0], next[0] if next else None

        for _, item, __ in iter_on_mail():
            h = self._template.render(message=item, css=file_css, render=self, location=location,
                                      title=self._title, url=item.default_filename() + ".html", now=now)
            content.append(h)

        self.fLOG("[EmailMessageListRenderer.render] end")
        h = self._template_end.render(css=file_css, render=self,
                                      location=location, title=self._title, now=now)
        json_attachments = []
        if attachments is not None:
            for att in attachments:
                satt = att.replace("\\", "/")
                json_attachments.append(dict(a=satt, name=satt))  # pylint: disable=R1735
        content.append(h)
        return "\n".join(content), css, json_attachments

    def write(self, location, iter, filename, attachments=None,  # pylint: disable=W0221,W0237
              overwrite=False, file_css="mail_style.css",
              file_jsatt="_summaryattachements.json", encoding="utf8",
              attach_folder="attachments"):
        """
        Writes a list of mails in a folder and writes a summary.

        @param      location        location
        @param      mail            instance of @see cl EmailMessage
        @param      attachments     list of attachments (see @see me dump_attachments)
        @param      overwrite       the function does not overwrite
        @param      file_css        css file (where it is supposed to be stored)
        @param      file_jsatt      list of attachments in json format
                                    ``[{'a': 'href', 'name': 'anchor', ...}, ...]``
        @param      encoding        encoding
        @param      attach_folder   attachments folder
        @return                     list of written local files

        The method calls method :meth:`flush
        <pymmails.helpers.buffer_files_writing.BufferFilesWriting.flush>`.
        """
        if not hasattr(iter, '__iter__'):
            raise TypeError("class {0} is not iterable".format(type(iter)))

        full_css = os.path.join(location, file_css)
        full_mail = os.path.join(location, filename)
        full_file_jsatt = os.path.join(location, file_jsatt)
        if self.BufferWrite.exists(full_css, local=not overwrite) and \
                self.BufferWrite.exists(full_mail, local=not overwrite):
            self.fLOG("[EmailMessageListRenderer.write] already exist css='{0}' html='{1}']".format(
                full_css, full_mail))
            return [full_mail, full_css]

        def fwrite(message, location, prev_mail, next_mail):
            "local function"
            res = message.dump(self._email_renderer, location=location,
                               prev_mail=prev_mail, next_mail=next_mail, fLOG=self.fLOG,
                               overwrite=overwrite, attach_folder=attach_folder)
            html, css = res[0]
            atts = res[1]
            return html, css, atts

        def walk_iter():
            "local function"
            for obj in iter:
                yield obj, fwrite

        html, css, json_att = self.render(
            location, walk_iter(), file_css=full_css)
        wrote = []
        if not self.BufferWrite.exists(full_css, local=not overwrite):
            f = self.BufferWrite.open(full_css, text=True, encoding=encoding)
            f.write(css)
            wrote.append(full_css)
        if not self.BufferWrite.exists(full_mail, local=not overwrite):
            f = self.BufferWrite.open(full_mail, text=True, encoding=encoding)
            f.write(html)
            wrote.append(full_mail)
        if json_att and not self.BufferWrite.exists(full_file_jsatt, local=not overwrite):
            f = self.BufferWrite.open(
                full_file_jsatt, text=True, encoding=encoding)
            js = json.dumps(json_att)
            f.write(js)
            wrote.append(full_file_jsatt)
        return wrote
