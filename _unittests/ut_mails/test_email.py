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


import src.pymmails as pymmails
from src.pymmails import MailBoxImap
from pyquickhelper import fLOG


class TestEmail (unittest.TestCase):

    def test_load_email(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        data = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        mesf = os.path.join(data, "message.pickle")
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
                            "..",
                            "pymmails",
                            "src")))
                if path not in sys.path:
                    sys.path.append(path)
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
                            "..",
                            "pymmails",
                            "src")))
                if path not in sys.path:
                    sys.path.append(path)
                obj = pickle.load(f)
                del sys.path[-1]

        temp = os.path.join(data, "..", "temp_html")
        if os.path.exists(temp):
            pyquickhelper.remove_folder(temp)
        if not os.path.exists(temp):
            os.mkdir(temp)

        ff = obj.dump_html(temp, fLOG=fLOG)
        fLOG(type(ff), ff)
        assert "d_2014-12-15_p_yyyyy_matthieu-xxxxx_xxx_ii_48bdbc9f9fd180ab917cec5bed8ca529.html" in ff


if __name__ == "__main__":
    unittest.main()
