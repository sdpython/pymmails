# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest

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
    import pyquickhelper as skip_
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
    import pyquickhelper as skip_

from src.pymmails.helpers import BufferFilesWriting
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder


class TestBufferFilesWriting(unittest.TestCase):

    def test_buffer_files_writing(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        temp = get_temp_folder(__file__, "temp_buffer_files_writing")
        buffer = BufferFilesWriting()

        f1 = os.path.join(temp, "fb.bin")
        assert not os.path.exists(f1)
        op = buffer.open(f1, False)
        op.write(b"456a")
        assert not os.path.exists(f1)

        f2 = os.path.join(temp, "fb.txt")
        assert not os.path.exists(f2)
        op = buffer.open(f2, True, encoding="utf8")
        op.write("456aé")
        assert not os.path.exists(f2)

        buffer.flush(None)
        assert os.path.exists(f1)
        assert os.path.exists(f2)


if __name__ == "__main__":
    unittest.main()
