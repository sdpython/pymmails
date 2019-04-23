# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""
import os
import unittest
from collections import OrderedDict
from pymmails import EmailMessage


class TestMetaData(unittest.TestCase):

    def test_metadata(self):
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        meta = os.path.join(data, "e.ipynb.metadata")
        d2 = EmailMessage.read_metadata(meta)
        self.assertIsInstance(d2, OrderedDict)


if __name__ == "__main__":
    unittest.main()
