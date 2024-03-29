"""
@brief      test log(time=0s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8, ExtTestCase


class TestCodeStyle(ExtTestCase):

    def test_style_src(self):
        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "src"))
        check_pep8(src_,
                   pylint_ignore=('C0103', 'C1801', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'C0412', 'W0622', 'W0621', 'C0411',
                                  'C0415', 'W0107', 'C0209'),
                   fLOG=fLOG,
                   skip=["email_sender.py:45: W0603",
                         "Redefining built-in ",
                         "Parameters differ from overridden ",
                         "Access to a protected member ",
                         "mailbox_mock.py:22: W0231",
                         "Catching too general exception Exception",
                         "Too many nested blocks",
                         "mailbox_mock.py:21: W0231",
                         ])

    def test_style_test(self):
        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0103', 'C1801', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'C0412', 'W0622', 'W0621', 'C0411',
                                  'C0415', 'C0209'),
                   skip=[])


if __name__ == "__main__":
    unittest.main()
