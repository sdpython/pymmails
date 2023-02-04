# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""
import os
import unittest
import warnings
import datetime
from pyquickhelper.loghelper import fLOG, get_password
from pyquickhelper.pycode import is_travis_or_appveyor
from pymmails import MailBoxImap


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

        user = get_password("gmail", "pymmails,user")
        code = get_password("gmail", "pymmails,pwd")
        if code is None:
            raise ValueError("code cannot be None.")

        box = MailBoxImap(user, code, "imap.gmail.com", ssl=True, fLOG=fLOG)
        try:
            box.login()
        except Exception as e:  # pylint: disable=W0703
            warnings.warn("Unable to connect due to %r." % e)
            return

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
            frm = [_ for _ in fr if _]
            if "=?" in frm[0]:
                issues.append(name)
            if "@" not in fr[1]:
                issues.append(name)
        if len(issues) > 0:
            raise AssertionError("Issues with\n{0}".format(
                "\n".join(str(_) for _ in issues)))


if __name__ == "__main__":
    unittest.main()
