import sys


cdef extern from 'dirent.h':
    ctypedef struct DIR
    struct dirent:
        char d_name[0]
    DIR* _opendir 'opendir' (char* name)
    int closedir(DIR* dirp)
    dirent* readdir(DIR* dirp)
    void rewinddir(DIR* dirp)
    void seekdir(DIR* dirp, long int loc)
    long int telldir(DIR* dirp)

cdef extern from 'errno.h':
    int errno

cdef extern from 'string.h':
    char* strerror(int errnum)


cdef class opendir:
    cdef DIR* _dirp
    cdef int _uni

    def __init__(self, path):
        if isinstance(path, unicode):
            path = path.encode(sys.getfilesystemencoding() or
                               sys.getdefaultencoding())
            self._uni = 1
        else:
            self._uni = 0
        self._dirp = _opendir(path)
        if self._dirp is NULL:
            raise OSError(errno, strerror(errno))

    def read(self):
        try:
            return self.__next__()
        except StopIteration:
            return None

    def __iter__(self):
        return self

    def __next__(self):
        cdef dirent* d
        d = readdir(self._dirp)
        if d is NULL:
            raise StopIteration()
        if d.d_name == b'.' or d.d_name == b'..':
            return self.__next__()
        if self._uni:
            try:
                return d.d_name.decode(sys.getfilesystemencoding() or
                                       sys.getdefaultencoding())
            except UnicodeDecodeError:
                pass
        return d.d_name

    def rewind(self):
        rewinddir(self._dirp)

    def tell(self):
        return telldir(self._dirp)

    def seek(self, loc):
        seekdir(self._dirp, loc)

    def close(self):
        if self._dirp is not NULL:
            closedir(self._dirp)
            self._dirp = NULL

    def __dealloc__(self):
        self.close()
