# -*- coding: utf-8 -*-
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.split(__file__)[0],
            "..",
            "..",
            "..",
            "..",
            "pyquickhelper",
            "src")))

from pyquickhelper.helpgen.default_conf import set_sphinx_variables

set_sphinx_variables(__file__, "pymmails", "Xavier Dupré", 2016,
                     "alabaster", None, locals(), add_extensions=None,
                     extlinks=dict(issue=('https://github.com/sdpython/pymmails/issues/%s', 'issue')))

blog_root = "http://www.xavierdupre.fr/app/pymmails/helpsphinx/"
