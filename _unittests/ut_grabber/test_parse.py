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


class TestParse(unittest.TestCase):

    def test_decode_header(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        name = "=?iso-8859-1?Q?Dupr=E9_Xavier?= <Xavier.Dupre@ensae.fr>"
        res = EmailMessage.call_decode_header(name)
        self.assertEqual(res[0], "Dupré Xavier")
        res = EmailMessage.call_decode_header(name, is_email=True)
        self.assertEqual(res[0], "Dupré Xavier <Xavier.Dupre@ensae.fr>")


if __name__ == "__main__":
    unittest.main()