# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""
import unittest
from pymmails import EmailMessage


class TestParse(unittest.TestCase):

    def test_decode_header(self):
        name = "=?iso-8859-1?Q?Dupr=E9_Xavier?= <Xavier.Dupre@ensae.fr>"
        res = EmailMessage.call_decode_header(name)
        self.assertEqual(res[0], "Dupré Xavier")
        res = EmailMessage.call_decode_header(name, is_email=True)
        self.assertEqual(res[0], "Dupré Xavier <Xavier.Dupre@ensae.fr>")


if __name__ == "__main__":
    unittest.main()
