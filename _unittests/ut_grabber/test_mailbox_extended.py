# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import warnings
import datetime

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


from src.pymmails import MailBoxImap
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import is_travis_or_appveyor


class TestMailBox(unittest.TestCase):

    def test_mailbox_extended(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            warnings.warn("requires a password")
            return

        now = datetime.datetime.now()
        now -= datetime.timedelta(1)
        date = now.strftime("%d-%b-%Y")

        if "DOUZE2016" in os.environ.get("COMPUTERNAME", ""):
            # does not work on the remote build server
            return

        import keyring
        user = keyring.get_password(
            "gmail", os.environ["COMPUTERNAME"] + "user")
        code = keyring.get_password(
            "gmail", os.environ["COMPUTERNAME"] + "pwd")

        box = MailBoxImap(user, code,
                          "imap.gmail.com", ssl=True, fLOG=fLOG)
        box.login()

        mails = box.enumerate_mails_in_folder("inbox", date=date)
        li = list(mails)
        self.assertTrue(len(li) > 0)
        box.logout()

        issues = []
        for mail in li:
            name = mail.get_name()
            if "=?" in mail:
                issues.append(name)
            fr = mail.get_from()
            if "=?" in fr[0]:
                issues.append(name)
            if "@" not in fr[1]:
                issues.append(name)
        if len(issues) > 0:
            raise Exception("Issues with\n{0}".format(
                "\n".join(str(_) for _ in issues)))


if __name__ == "__main__":
    unittest.main()
