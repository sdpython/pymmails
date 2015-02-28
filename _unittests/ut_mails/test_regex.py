"""
@brief      test log(time=25s)
"""

import sys
import os
import unittest
import socket

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


from src.pymmails import EmailMessage
from pyquickhelper import fLOG


class TestRegEx (unittest.TestCase):

    def test_regular_expression(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        fold = os.path.abspath(os.path.dirname(__file__))

        body = """
                    </div>
                    <div><img name="14a318e16161c62a_14a31789f7a34aae_null" title="pastedImage.png" src="cid:f8b05bd4-1c83-47bc-af9d-0032ba9c018e"><br>
                    </div>
                    <div>4. Vous m&#39;avez demande d&#39;afficher l&#39;arbre de decision pour mon random forest, mais apparemment &quot;.tree_&quot; n&#39;existe que pour les decision trees . J&#39;ai donc essaye de le faire avec un DT apres avoir telecharge le logiciel pour tracer l&#39;arbre mais ca ne marche
                     pas<br>
                    </div>
                    <div><br>
                    </div>
                    <div><img name="14a318e16161c62a_14a31789f7a34aae_null" title="pastedImage.png" src="cid:1146aa0a-244a-440e-8ea5-7b272c94f89a" height="153.02644466209597" width="560"><br>
                    </div>
                    <div><br>
                    ?<sp
                    """.replace("                    ", "")

        atts = [
            (os.path.join(
                fold,
                "attachements",
                "image.png"),
                None,
                "1146aa0a-244a-440e-8ea5-7b272c94f89a")]
        em = EmailMessage.process_body_html(fold, body, atts)
        fLOG(em)
        assert "1146aa0a-244a-440e-8ea5-7b272c94f89a" not in em
        assert 'src="attachements\\image.png"' in em


if __name__ == "__main__":
    unittest.main()
