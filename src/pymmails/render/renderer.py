# -*- coding: utf-8 -*-
"""
@file
@brief Functions to dump emails
"""
from jinja2 import Template
from pyquickhelper import noLOG


class Renderer:
    """
    defines way to render an email
    """

    def __init__(self, tmpl, css,
                 style_table="dataframe100l",
                 style_highlight="dataframe100l_hl",
                 buffer_write=None, fLOG=noLOG):
        """
        constructor, defines a template based
        on `Jinja2 <http://jinja.pocoo.org/docs/dev/>`_

        @param      tmpl                template (string or file)
        @param      css                 style
        @param      style_table         style for the table
        @param      style_highlight     style for highlighted cells
        @param      buffer_write        instance of class @see cl BufferFilesWriting
        """
        self._template = Template(tmpl)
        self._css = Template(css)
        self._style_table = style_table
        self._style_highlight = style_highlight
        self._session = None
        self._buffer_write = buffer_write
        self.fLOG = fLOG

    def flush(self):
        """
        flushes all files

        @return     number of bytes written
        """
        return self.BufferWrite.flush(None)

    @property
    def BufferWrite(self):
        """
        returns ``self._buffer_write``
        """
        return self._buffer_write

    def render(self, location, obj, attachments=None, file_css="mail_style.css"):
        """
        render a mail

        @paramp     location        location where this mail should be saved
        @param      obj             instance of an object
        @param      file_css        css file (where it is supposed to be stored)
        @param      attachments     attachments
        @return                     html, css (content)

        The mail is stored in object ``message``, ``css`` means the style sheet,
        ``render`` means this object, ``location`` means *location*,
        ``attachments`` is *attachments*::

            {{ message.get_subject() }}

        The value stored in *file_css* will be relative to *location*.

        """
        raise NotImplementedError("this methods needs to be overwritten")

    def write(self, location, mail, filename, attachments=None,
              overwrite=False, file_css="mail_style.css", encoding="utf8"):
        """
        writes a mail, the function assumes the attachments were already dumped

        @param      location        location
        @param      mail            instance of an object or an iterator
        @param      attachments     list of attachments (see @see me dump_attachments)
        @param      overwrite       the function does not overwrite
        @param      file_css        css file (where it is supposed to be stored)
        @param      encoding        encoding
        @return                     list of written local files
        """
        raise NotImplementedError("this methods needs to be overwritten")
