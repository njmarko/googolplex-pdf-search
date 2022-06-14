"""
Author: Marko Njegomir sw-38-2018
"""


class Stack(object):

    def __init__(self):
        self._data = []

    def is_empty(self):
        return len(self._data) == 0

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if self.is_empty():
            raise Exception
        return self._data.pop()

    def top(self):
        if self.is_empty():
            raise Exception
        return self._data[-1]

    def __len__(self):
        return len(self._data)
