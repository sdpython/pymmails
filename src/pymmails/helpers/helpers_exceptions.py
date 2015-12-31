"""
@file
@brief Exception for subfolders ``helpers``
"""


class FileAlreadyExistingException(Exception):
    """
    file which already existing
    """
    pass


class FileNotFlushedException(Exception):
    """
    raised when the class @see cl BufferFilesWriting still contains
    some files not flushed when deleted
    """
    pass
