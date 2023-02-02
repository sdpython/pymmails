# -*- coding: utf-8 -*-
import sys
import os
from pyquickhelper.helpgen.default_conf import set_sphinx_variables

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

set_sphinx_variables(__file__, "pymmails", "Xavier Dupré", 2023,
                     "alabaster", None, locals(), add_extensions=None,
                     extlinks=dict(issue=(
                         'https://github.com/sdpython/pymmails/issues/%s',
                         'issue %s')))

blog_root = "http://www.xavierdupre.fr/app/pymmails/helpsphinx/"
html_logo = "_static/project_ico.png"
