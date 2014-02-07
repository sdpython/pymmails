# coding: latin-1
"""
@brief      test log(time=1s)
"""

import sys, os, unittest, socket

try :
    import src
except ImportError :
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..")))
    if path not in sys.path : sys.path.append (path)
    import src
    
try :
    import pyquickhelper
except ImportError :
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..", "..","pyquickhelper", "src")))
    if path not in sys.path : sys.path.append (path)
    import pyquickhelper
    

from src.pymmails import MailBoxImap
from pyquickhelper import fLOG

class TestGrab (unittest.TestCase):
    
    def test_exception(self) :
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        try :
            MailBoxImap("nobody","nopwd", server="nowhere")
        except socket.gaierror:
            pass
        


if __name__ == "__main__"  :
    unittest.main ()    
