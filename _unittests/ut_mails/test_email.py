# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import pickle

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

try:
    import pyquickhelper
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper


from src.pymmails import MailBoxImap, EmailMessage, EmailMessageRenderer
from pyquickhelper import fLOG, get_temp_folder


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
                obj = pickle.load(f)
                del sys.path[-1]

        tos = obj.get_to()
        cc = obj.get_to(True)
        fLOG("cc", cc)
        assert len(cc) == 1
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
        assert len(tos) > 10

        exp = """
            wwww1ww.wwwwwww@xxxxx.xx
            wwww2ww.wwan@xxxxx.xx
            wwwwwww.wwwrrab@xxxxx.xx
            wwwwwwpe.ww@xxxxx.xx
            wwwwwe.wwwwt@xxxxx.xx
            wwww.wwwww@xxxxx.xx
            wwwww.wwwwwL@xxxxx.xx
            wwwwn.wwwwwwwE@xxxxx.xx
            wwwwww.wwwwwwre@xxxxx.xx
            wwwwwww.ww@xxxxx.xx
            wwwwwwne.wwwww.wwwwww@xxxxx.xx
            wwwwwn.wwwwy@xxxxx.xx
            wwwww.wwwwww@xxxxx.xx
            wwwo.wwwwwer@xxxxx.xx
            wwwwwwin.wwwwwt@xxxxx.xx
            wwwww.wwwwwwwI@xxxxx.xx
            wwwweo.wwwwwww@xxxxx.xx
            wwwwwwlt.wwwwwl@xxxxx.xx
            wwwwwww.wwwwwwt@xxxxx.xx
            wwwwas wwwwy <wwwwas.wwwwwer@xxxxx.xx>
            wwwwo.wwwwAYA@xxxxx.xx
            wwww.wwwba@xxxxx.xx
            wwwwwwy.wwwwwwD@xxxxx.xx
            wwwwwn.wwwRI@xxxxx.xx
            wwwwwww.wwwwwiez@xxxxx.xx
            wwww.www.ww@xxxxx.xx
            Xavier zzzzz <xavier.zzzzz@xxxxx.xxx>
            wwwthieu yyyyy <yyyyy.matthieu@xxxxx.xxx>
            wwwwws wwwwout <wwwwwwwwwwwww@xxxxx.xxx>
            """.replace("            ", "").strip("\n\r\t ").split("\n")
        fLOG(len(exp), len(tos))
        end = min(len(exp), len(tos))
        for i, j in zip(exp[:end], tos[:end]):
            if j[1] not in i:
                raise Exception(
                    "issue with {0} and {1} .... {2}".format(
                        i, j[1], [
                            i, j[1]]))

        assert len(exp) == len(tos)

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
                obj = pickle.load(f)
                del sys.path[-1]

        temp = get_temp_folder(__file__, "temp_dump_html")
        render = EmailMessageRenderer()
        ff = obj.dump(render, location=temp, fLOG=fLOG)
        render.flush()
        fLOG(type(ff), ff)
        with open(ff[0], "r", encoding="utf8") as f:
            content = f.read()
        if '<link rel="stylesheet" type="text/css" href="mail_style.css">' not in content:
            raise Exception(content)
        if "d_2014-12-15_p_yyyyy_matthieu-xxxxx_xxx_ii_48bdbc9f9fd180ab917cec5bed8ca529.html" not in ff[0]:
            raise Exception(ff[0])
        if "<h1>2014/30/15 - projet 3A - élément logiciel</h1>" not in content:
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
