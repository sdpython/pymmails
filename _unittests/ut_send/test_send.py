"""
@brief      test log(time=25s)
"""
import os
import unittest
from pyquickhelper.pycode import ExtTestCase
from pymmails import create_smtp_server, send_email, compose_email, MailBoxImap


class TestSend(ExtTestCase):

    def test_compose_email(self):
        st = compose_email("machine@gmail.com", "machinto@gmail.com",
                           "subject", attachements=[os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_send.py")])
        self.assertGreater(len(st), 0)
        self.assertIn("main_wrapper_tests(__file__)", st)
        self.assertIn("To: machinto@gmail.com", st)

    def test_send_email(self):
        st = send_email(None, "machine@gmail.com", "machinto@gmail.com",
                        "subject", cc=["a@a"], bcc=["b@b"], delay_sending=True,
                        attachements=[os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_send.py")])
        self.assertTrue(st is not None)
        self.assertRaise(lambda: st())

    def should_bemocked_test_server_send(self):
        server = create_smtp_server("gmail", "somebody", "pwd")
        send_email(server, "somebody@gmail.com", "somebody@gmail.com",
                   "subject", attachements=[os.path.abspath(__file__)])
        server.quit()

    def should_bemocked_test_fetch_mail(self):
        imap = MailBoxImap("somebody", "pwd", "imap.gmail.com", True)
        imap.login()
        iter = imap.enumerate_search_subject("subject", "inbox")
        for m in iter:
            m.dump(iter, "destination")
        imap.logout()


if __name__ == "__main__":
    unittest.main()
