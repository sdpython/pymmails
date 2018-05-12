"""
@brief      test log(time=25s)
"""

import sys
import os
import unittest
import socket
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


from src.pymmails import MailBoxImap


class TestGrab (unittest.TestCase):

    def test_exception(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        try:
            MailBoxImap("nobody", "nopwd", server="nowhere")
        except TimeoutError:
            fLOG("TimeoutError")
        except socket.gaierror:
            fLOG("gaierror")
        except ConnectionRefusedError:
            fLOG("ConnectionRefusedError")


if __name__ == "__main__":
    unittest.main()
