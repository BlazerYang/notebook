# coding:utf8
list = []

for i in range(3):
    def func(a):
        return i+a
    list.append(func)

for f in list:
    print(f(1))