"""
@brief      test log(time=25s)
"""
import unittest
import socket
from pyquickhelper.loghelper import fLOG
from pymmails import MailBoxImap


class TestGrab(unittest.TestCase):

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
