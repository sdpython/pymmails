# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""
import unittest
import warnings
from pyquickhelper.loghelper import fLOG, get_password
from pyquickhelper.pycode import get_temp_folder, is_travis_or_appveyor
from pymmails import MailBoxImap, EmailMessageRenderer


class TestMailBox(unittest.TestCase):

    def test_mailbox(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            warnings.warn("requires a password")
            return
        code = get_password("sdut", "pymmails")
        box = MailBoxImap("unittest.sdpython", code,
                          "imap.gmail.com", ssl=True, fLOG=fLOG)
        box.login()
        mails = box.enumerate_mails_in_folder("test4", date="1-Jan-2016")
        li = list(mails)
        self.assertEqual(len(li), 3)
        box.logout()

    def test_mailbox_dump(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            warnings.warn("requires a password")
            return
        code = get_password("sdut", "pymmails")
        temp = get_temp_folder(__file__, "temp_dump")
        box = MailBoxImap("unittest.sdpython", code,
                          "imap.gmail.com", ssl=True, fLOG=fLOG)
        render = EmailMessageRenderer()
        box.login()
        mails = box.enumerate_mails_in_folder("test4", date="1-Jan-2016")
        for mail in mails:
            mail.dump(render, location=temp, fLOG=fLOG)
        render.flush()
        box.logout()


if __name__ == "__main__":
    unittest.main()
