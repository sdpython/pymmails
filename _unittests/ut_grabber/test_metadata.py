# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
from collections import OrderedDict
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


class TestMetaData(unittest.TestCase):

    def test_metadata(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        meta = os.path.join(data, "e.ipynb.metadata")
        d2 = EmailMessage.read_metadata(meta)
        fLOG(d2)
        fLOG(type(d2))
        self.assertIsInstance(d2, OrderedDict)


if __name__ == "__main__":
    unittest.main()
