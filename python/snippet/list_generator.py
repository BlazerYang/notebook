# coding: utf-8
# 利用list生成式和dict.get()提取元素的值

a = [{'a':1},{'a':2},{'b':3},{'a':4}]
b = [v.get('a') for v in a]

print a
print b # [1, 2, None, 4]
