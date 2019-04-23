# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import pickle
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder
from pymmails import EmailMessage, EmailMessageRenderer


class TestEmail (unittest.TestCase):

    def test_load_email(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        mesf = os.path.join(data, "message.pickle")

        if "anaconda" in sys.executable.lower():
            # issue with Anaconda about import pymmails
            return

        with open(mesf, "rb") as f:
            try:
                import pymmails
                assert pymmails is not None
                obj = pickle.load(f)
            except ImportError:
                path = os.path.normpath(
                    os.path.abspath(
                        os.path.join(
                            os.path.split(__file__)[0],
                            "..",
                            "..",
                            "src")))
                if path not in sys.path:
                    sys.path.append(path)
                import pymmails
                assert pymmails is not None
                obj = pickle.load(f)
                del sys.path[-1]

        tos = obj.get_to()
        tod = obj.get_to(field="Delivered-To")
        cc = obj.get_to(True)
        assert cc is None
        fLOG("tos", len(tos), tos)
        fLOG("tod", len(tod), tod)
        fLOG("cc", cc)
        assert len(tos) > 1
        self.assertEqual(len(tod), 1)
        fro = obj.get_from()
        fLOG(tos)
        fLOG(fro)
        fLOG(obj.get_field("subject"))
        assert len(fro) == 2
        assert fro[0] == "matthieuyyyyy ."
        assert fro[1] == "yyyyy.matthieu@xxxxx.xxx"
        if obj.get_field("subject") != "projet 3A - élément logiciel":
            raise Exception(
                "{0} != {1}".format(
                    obj.get_field("subject"),
                    "projet 3A - élément logiciel"))
        fLOG(obj.Fields)
        assert len(tos) == 8

    def test_tohtml(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        mesf = os.path.join(data, "message.pickle")

        if "anaconda" in sys.executable.lower() or "anaconda" in sys.base_prefix.lower():
            # issue with Anaconda about module pickle
            # pickle has issues when getting a file saved by pickle on another
            # distribution
            return

        with open(mesf, "rb") as f:
            try:
                import pymmails
                assert pymmails is not None
                obj = pickle.load(f)
            except ImportError:
                path = os.path.normpath(
                    os.path.abspath(
                        os.path.join(
                            os.path.split(__file__)[0],
                            "..",
                            "..",
                            "src")))
                if path not in sys.path:
                    sys.path.append(path)
                import pymmails
                assert pymmails is not None
                obj = pickle.load(f)
                del sys.path[-1]

        temp = get_temp_folder(__file__, "temp_dump_html")
        render = EmailMessageRenderer()
        ff = obj.dump(render, location=temp, fLOG=fLOG)
        render.flush()
        fLOG("ff=", type(ff), ff)
        with open(ff[0][0], "r", encoding="utf8") as f:
            content = f.read()
        if '<link rel="stylesheet" type="text/css" href="mail_style.css">' not in content:
            raise Exception(content)
        if "d_2014-12-15_p_yyyyy-matthieu-at-xxxxx-xxx_ii_48bdbc9f9fd180ab917cec5bed8ca529.html" not in ff[0][0]:
            raise Exception(ff[0][0])
        if "<h1>2014/12/15 - projet 3A - élément logiciel</h1>" not in content:
            raise Exception(content)

    def test_decode_header(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        st = '"dupre [MailContact]" <xavier.dupre@gmail.com>,  	=?iso-8859-1?Q?Emmanuel_Gu=E9rin?= <m@emmanuelguerin.fr>'
        res, enc = EmailMessage.call_decode_header(st)
        fLOG("***", enc)
        fLOG("***", res)
        self.assertEqual(enc, "iso-8859-1")
        assert res.startswith('"dupre [MailContact]" <xavier.dupre@gmail.com>')


if __name__ == "__main__":
    unittest.main()
