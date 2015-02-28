"""
@brief      test log(time=25s)
"""

import sys
import os
import unittest
import socket

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


from src.pymmails import create_smtp_server, send_email, compose_email, MailBoxImap
from pyquickhelper import fLOG


class TestSend(unittest.TestCase):

    def test_send_email(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        st = compose_email("machine@gmail.com", "machinto@gmail.com",
                           "subject", attachements=[os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "run_unittests.py")])
        # fLOG(st)
        assert len(st) > 0
        assert "main_wrapper_tests(__file__)" in st
        assert "To: machinto@gmail.com" in st

    def should_bemocked_test_server_send(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        server = create_smtp_server("gmail", "somebody", "pwd")
        send_email(server, "somebody@gmail.com", "somebody@gmail.com",
                   "subject", attachements=[os.path.abspath(__file__)])
        server.quit()

    def should_bemocked_test_fetch_mail(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        imap = MailBoxImap("somebody", "pwd", "imap.gmail.com", True)
        imap.login()
        iter = imap.enumerate_search_subject("subject", "inbox")
        fs = imap.dump_html(iter, "destination")
        imap.logout()


if __name__ == "__main__":
    unittest.main()
