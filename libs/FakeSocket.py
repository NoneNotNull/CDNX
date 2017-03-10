# /usr/bin/env python
# coding=utf-8

from StringIO import StringIO

class FakeSocket():
    """
    HTTPResponse的参数是socket
    它在构造函数里面会调用socket.makefile
    socket.makefile()函数返回的是文件指针
    其实就是类似于StringIO返回的结果
    """
    def __init__(self, response_str):
        self._file = StringIO(response_str)

    def makefile(self, *args, **kwargs):
        return self._file
