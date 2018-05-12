"""
@brief      test log(time=25s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import ExtTestCase

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


from src.pymmails import create_smtp_server, send_email, compose_email, MailBoxImap


class TestSend(ExtTestCase):

    def test_compose_email(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        st = compose_email("machine@gmail.com", "machinto@gmail.com",
                           "subject", attachements=[os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "run_unittests.py")])
        # fLOG(st)
        self.assertGreater(len(st), 0)
        self.assertIn("main_wrapper_tests(__file__)", st)
        self.assertIn("To: machinto@gmail.com", st)

    def test_send_email(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        st = send_email(None, "machine@gmail.com", "machinto@gmail.com",
                        "subject", cc=["a@a"], bcc=["b@b"], delay_sending=True,
                        attachements=[os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "run_unittests.py")])
        self.assertTrue(st is not None)
        self.assertRaise(lambda: st())

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
        for m in iter:
            m.dump(iter, "destination")
        imap.logout()


if __name__ == "__main__":
    unittest.main()
