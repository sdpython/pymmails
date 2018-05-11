# -*- coding: utf-8 -*-
"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest

try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_


from src.pymmails import MailBoxMock, EmailMessageRenderer, EmailMessageListRenderer
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder


class TestMessageBoxMock(unittest.TestCase):

    def test_box_mock_render(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))

        temp = get_temp_folder(__file__, "temp_render_mock_list_mail")
        box = MailBoxMock(data, b"unittestunittest", fLOG)
        box.login()
        folders = box.folders()
        assert len(folders) == 1
        fLOG(folders)
        mails = list(box.enumerate_mails_in_folder("trav"))
        box.logout()

        email_render = EmailMessageRenderer()

        def tempf(message, location, prev_mail, next_mail):
            email_render.render(location, message, None,
                                file_css="mail_style.css",
                                prev_mail=prev_mail, next_mail=next_mail)
            return ""

        mails = list((m, tempf) for m in mails)
        render = EmailMessageListRenderer(
            title="list of mails", email_renderer=email_render, fLOG=fLOG)
        res = render.render(iter=mails, location=temp)
        render.flush()
        # fLOG(res[0])
        exp = ('<a href="d_2015-08-01_p_noreply-at-voyages-sncf-com_ii_8de6a63addb7c03407bc6f0caabd967e.html">' +
               '2015/08/01 -\n Voyages-sncf.com</a>')
        if exp not in res[0]:
            raise Exception(res[0])

    def test_box_mock_write(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))

        temp = get_temp_folder(__file__, "temp_write_mock_list_mail")
        box = MailBoxMock(data, b"unittestunittest", fLOG)
        box.login()
        folders = box.folders()
        assert len(folders) == 1
        fLOG(folders)
        mails = list(box.enumerate_mails_in_folder("trav"))
        box.logout()

        email_render = EmailMessageRenderer()
        render = EmailMessageListRenderer(
            title="list of mails", email_renderer=email_render, fLOG=fLOG)
        res = render.write(iter=mails, location=temp, filename="essai.html")
        render.flush()

        with open(res[0], "r", encoding="utf8") as f:
            content = f.read()
        exp = ('<a href="d_2015-12-20_p_noreply-at-voyages-sncf-com_ii_1bb6fa70421145bed927e00c5e292277.html">' +
               '2015/12/20 -\n Voyages-sncf.com</a>')
        if exp not in content:
            raise Exception(content)
        if 'list of mails</h1>' not in content:
            raise Exception(content)
        allfiles = render.BufferWrite.listfiles()
        assert len(allfiles) > 0

        allfiles.sort()
        with open(allfiles[0], "r", encoding="utf8") as f:
            content = f.read()
        if '<a href="d_2015-08-01_p_noreply-at-voyages-sncf-com_ii_8de6a63addb7c03407bc6f0caabd967e.html">&lt;--</a>' not in content:
            raise Exception(content)


if __name__ == "__main__":
    unittest.main()
