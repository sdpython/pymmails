# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import pickle

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
    import pyquickhelper
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
    import pyquickhelper


from src.pymmails import MailBoxImap, EmailMessage, MailBoxMock, EmailMessageRenderer, EmailMessageListRenderer
from pyquickhelper import fLOG, get_temp_folder


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

        def tempf(message, location):
            email_render.render(location, message, None,
                                file_css="mail_style.css")
            return ""

        mails = list((m, tempf) for m in mails)
        render = EmailMessageListRenderer(
            title="list of mails", email_renderer=email_render, fLOG=fLOG)
        res = render.render(iter=mails, location=temp)
        fLOG(res[0])
        assert '<a href="">2015/40/01 - Voyages-sncf.com</a>' in res[0]


if __name__ == "__main__":
    unittest.main()
