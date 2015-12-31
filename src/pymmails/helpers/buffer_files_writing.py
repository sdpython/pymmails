"""
@file
@brief Buffer files writing
"""
import io
import os
from pyquickhelper import noLOG
from .helpers_exceptions import FileAlreadyExistingException, FileNotFlushedException


class BufferFilesWriting:
    """
    this class aims at delaying writing files,
    method *open* returns a buffer,
    method *flush* actually writes the file
    """

    def __init__(self, flush_every=20, fLOG=noLOG):
        """
        constructor

        @param      flush_every     flush every 20 created files
        """
        self._nb = 0
        self._buffer = {}
        self._done = set()
        self.fLOG = fLOG
        self._flush_every = flush_every

    def exists(self, name, local=True):
        """
        tells if a file was already written

        @param      name        name
        @param      local       check local existence too
        @return                 boolean
        """
        return name in self._done or \
            name in self._buffer or \
            (local and os.path.exists(name))

    def listfiles(self):
        """
        returns the list of flushed and opened files,
        does not preserved order

        @return     list of files
        """
        return list(self._done) + list(self._buffer.keys())

    def __len__(self):
        """
        return the number of buffered files
        """
        return len(self._buffer)

    def open(self, name, text=True, encoding="utf8"):
        """
        open a file and returns a buffer

        @param      name        filename
        @param      text        text or binary file
        @param      encoding    encoding
        @return                 a buffer
        """
        if len(self._buffer) > self._flush_every:
            self.flush(None)
        if name in self._buffer:
            raise FileAlreadyExistingException(name)
        if text:
            buf = io.StringIO()
        else:
            buf = io.BytesIO()

        self._buffer[name] = (buf, encoding, self._nb)
        self._nb += 1
        return buf

    def flush(self, name, upto=False):
        """
        flush a file (actually write it) and make it disappear from the list of buffered files,
        if the folder does not exists, the method creates it

        @param      name    file name (or None for all)
        @param      upto    flush all files up to this one
        @return             number of written bytes
        """
        if name is None:
            size = 0
            keys = list(self._buffer.keys())
            for name in keys:
                size += self.flush(name)
            return size
        else:
            if name not in self._buffer:
                raise FileNotFoundError(
                    name + "\nEXISTING\n" + "\n".join(self.listfiles()))
            if upto:
                n = self._buffer[name][2]
                names = [name for name, v in self._buffer.items() if v[2] <= n]
                size = 0
                for name in names:
                    size += self.flush(name)
                return size
            else:
                fold = os.path.dirname(name)
                if not os.path.exists(fold):
                    os.makedirs(fold)
                buf = self._buffer[name][0]
                if isinstance(buf, io.StringIO):
                    b = buf.getvalue()
                    with open(name, "w", encoding=self._buffer[name][1]) as f:
                        f.write(b)
                else:
                    b = buf.getvalue()
                    with open(name, "wb") as f:
                        f.write(b)
                self.fLOG("BufferFilesWriting.flush [write {0}]".format(name))
                del self._buffer[name]
                self._done.add(name)
                return len(b)

    def __del__(self):
        """
        destructor, check everything was flushed
        """
        if len(self._buffer) > 0:
            raise FileNotFlushedException(
                "\n".join(sorted(self._buffer.keys())))
