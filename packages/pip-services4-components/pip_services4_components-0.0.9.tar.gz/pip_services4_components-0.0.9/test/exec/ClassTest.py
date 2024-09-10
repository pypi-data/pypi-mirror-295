# -*- coding: utf-8 -*-

class ClassTest:

    def __init__(self, value1, value2):
        self.value1 = value1
        self._value2 = value2

    @property
    def value2(self):
        return self._value2

    @value2.setter
    def value2(self, value):
        self._value2 = value
