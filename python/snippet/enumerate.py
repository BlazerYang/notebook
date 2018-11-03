# -*- coding: utf-8 -*-
from __future__ import absolute_import

from enum import Enum, unique

@unique
class Gender(Enum):
    Male = 0
    Female = 1

class Student(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


if __name__ == "__main__":
    # 测试:
    bart = Student('Bart', Gender.Male)
    if bart.gender == Gender.Male:
        print(u'测试通过!')
    else:
        print(u'测试失败!')
        