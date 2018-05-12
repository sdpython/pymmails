# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG

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


from src.pymmails import EmailMessage


class TestDefault(unittest.TestCase):

    def test_default_filename(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        name = "d_2015-08-01_p_noreply-at-voyages-sncf-com_ii_52df24c718fdf138f997e73c383798eb.html"
        res = EmailMessage.interpret_default_filename(name)
        self.assertIsInstance(res, dict)
        self.assertEqual(len(res), 4)
        self.assertEqual(res["date"], "2015-08-01")


if __name__ == "__main__":
    unittest.main()
