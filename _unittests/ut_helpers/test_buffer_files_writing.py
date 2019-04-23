# -*- coding: utf-8 -*-
"""
@brief      test log(time=1s)
"""
import os
import unittest
from pyquickhelper.pycode import get_temp_folder
from pymmails.helpers import BufferFilesWriting


class TestBufferFilesWriting(unittest.TestCase):

    def test_buffer_files_writing(self):
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
