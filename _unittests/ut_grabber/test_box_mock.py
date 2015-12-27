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


from src.pymmails import MailBoxImap, EmailMessage, MailBoxMock, EmailMessageRenderer
from pyquickhelper import fLOG


class TestMessageBoxMock(unittest.TestCase):

    def test_box_mock(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))

        box = MailBoxMock(data, b"unittestunittest", fLOG)
        box.login()
        folders = box.folders()
        assert len(folders) == 1
        fLOG(folders)
        mails = list(box.enumerate_mails_in_folder("trav"))
        box.logout()

        fLOG(len(mails))
        assert len(mails) > 0
        mail0 = mails[0]
        # fLOG(mail0)

        bin = mail0.as_bytes()
        ema = EmailMessage.create_from_bytes(bin)
        d0 = mail0.to_dict()
        d1 = ema.to_dict()
        self.assertEqual(d0["Subject"], d1["Subject"])

        render = EmailMessageRenderer()
        html, css = render.render("__LOC__", mail0, "example_css.css", None)
        assert "example_css.css" in html
        # fLOG(css)
        fLOG(html)
        assert "<tr><th>Date</th><td>Sat, 1 Aug 2015 11:40:50 +0200 (CEST)</td></tr>" in html


if __name__ == "__main__":
    unittest.main()
