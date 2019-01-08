# index

## py, pyc, pyo 的区别？
* py是源文件
* pyc是py编译生成后的二进制文件。提高加载速度，隐藏源码
* pyo是优化编译后的文件

## python如何继承？
基类写在派生类声明的()中
```python
class SubClassName (ParentClass1[, ParentClass2, ...]):
   'Optional class documentation string'
   class_suite
```

## singal.pause()
暂停进程直到收到信号，然后调用合适的回调函数。无返回值。window下不可用

## 为何注册SIGINT(2)的回调后，以下代码的异常就没有被catch？
```python
try:
    consumer.start()
    signal.pause()
except KeyboardInterrupt:
    consumer.stop()
```
答：因为python会对一些常见的信号量注册默认的回调，比如SIGINT会被当做KeyboardInterrupt异常。

而python中新注册回调的话会覆盖之前的旧的回调，例如
```python
import signal

def sigintHandler(signum, frame):
    print "signal handler called with signal:", signum, "\n"

def sigintHandler2(signum, frame):
    print "this is sigintHandler2\n"

signal.signal(2, sigintHandler)
signal.signal(2, sigintHandler2)
# ctrl-c will print "this is sigintHandler2"
```

## python中如何取反？
```python
a = True
b = not a
```

## python如何一次读取一行，且不包含换行符？
```python
a = open("text").readLines()
b = a.rstrip(a)
# or
b = a[:-1]
```

## python不支持++
使用`number += 1`替代

## python拼接字符串和数字
python没有隐式类型转换？
```python
a = 222
b = '222'
c = str(a) + b
```

## python如何添加中文注释？
在开头定义编码格式
```python
 # -*- coding: utf-8 -*-
```

## python -v 输出一大堆信息，如何修复？
python看版本是用大写的V
-v: start python in verbose mode
-V, --version: print python version

## 函数调用中出现的赋值操作是什么意思？
```python
def foo(a, b):
    return "My name is " + a + ", I come from" + b

str = foo(b = 'Blazer', a = "Azerath")
```
这种操作可以忽略参数的顺序

## 字符串前面加'r'
告诉python字符串是raw string, 不要对"\"转义

## os has no mknod()
mknod只在unix系统上，window上中会报错  
新建文件可以用
```python
f = open("/file/path","w")
f.close()
```

## python assert如果出错还会继续运行吗？
不会，在python中assert基本等同于
```python
if not in condition
    raise AssertionError()
```
除非使用`except`捕获，否则程序会出错退出

## python 正则多行匹配？
使用re.M,需要注意的是使用re.match()和re.search()时，仅匹配第一个；多个匹配还是使用re.findall(),此时不加re.M也可以多行匹配

### re.search和re.match有什么区别？
* match从开头开始匹配
* search会搜索整个字符串

## python '''三单引号如何插值？
使用如下方式

## python [], (), {}区别
* [] 用于声明列表，list
* () 用于声明元组，tuple。注意，实际上python是依靠","来生成元组，而不是()
* {} 用于声明字典，dict

## *list什么操作？
* 对list或tuple进行解包操作，类似于js中...
* 如果是定义为函数参数`def foo(*list)`，那么意思就是可变参数，内部可以将其作为tuple使用
```python
def foo(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
```
* 如果定义为`def foo(**kw)`那么意思就是将可变参数组装为dict拼装进去
```python
def foo(name, age, **kw):
    print "name is %s, age is %d, other is %s" % (name, age, kw)

# 调用方式1
foo('yang', 27, 'city'="beijing", 'job'='798')

# 调用方式2
kw = {'city':"beijing", 'job':'798'}
foo('yang', 27, **kw)
```
* 命名关键字参数
如果想要规定上例中kw可接受的参数，那么可以采用如下方式定义
```python
# *之后的参数即为命名参数，之前的为位置参数
def foo(name, age, *, city, job)

# 如果已经存在可变参数，那么之后的可变参数无需使用*分隔
def foo(name, age, *args, city, job)
```


## list操作
### list如何新增元素
1. list.append(obj), 添加至列表尾部
2. list.insert(index, obj), 添加元素至指定位置，其余元素后移

### list如何删除元素
1. list.remove(obj), 删除命中的第一个元素
2. del list[index], 删除指定索引的元素
3. list.pop([index]), 删除并返回指定索引的元素，默认最后一个元素

### list如何修改元素
1. list[index] = newValue

### list如何查询元素
1. list.index(obj), 返回第一个命中命中元素的索引

### list合并
1. list.append(listB), 将listB中的元素依次拼接在list尾部，inplace算法，无返回值
2. list + listB，将两个列表合并为一个新的list

### list查询长度

### 其他奇葩操作
#### ["HI"] * 4
return ["HI","HI","HI","HI"]

#### 3 in [1,2,3]
return true  
obj in list操作检查的是元素值而非索引

#### for obj in [1,2,3]
对list的值进行遍历

##tuple操作
同list类似

### tuple的陷阱
```python
# 下面操作是计算了一个1，而不是定义了一个包含一个元素的tuple
a = (1)
# 为了消除歧义，通过添加逗号定义tuple
a = (1,)
```

##dict操作
### dict如何新增元素
1. dict[key] = value, 如果key存在则为修改，如果不存在则为新增

### dict如何删除元素
1. del dict[key], 删除指定key，如果不存在，则抛出KeyError异常
2. del dict, 删除词典
3. dict.clear(), 删除全部元素

### dict如何修改元素
见上

### dict如何查找元素
直接通过key引用，dict是通过hashmap实现，理论上查找是O(1),最坏情况下变为O(n)
1. dict[key], 返回key对应的值，如果不存在，会抛出KeyError异常
2. dict.get(key, default=None), 返回Key对应的值，如果不存在，则返回default，default默认为None
    1. dict.setdefault(key, default=None), 将key设为默认值，如果key不存在，则添加并设为默认值

### 如何判断key是否存在
1. key in dict
2. key in dict.keys()
3. dict.has_key(key), 不推荐：2.2以前的遗留api，3.0之后已删除

### 如何判断value是否存在
1. value in dict.values()

### dict合并
1. dict.update(dict2), 将dict2的值更新到dict，相同的key会被dict2中的值覆盖，inplace算法，无返回值

## set操作
同dict类似，都是hash存储。区别是set只能存储key，而没有value
```python
a = set([1,2,3])
b = set([2,3,4])
c = a & b # set([2,3])
```

## r''
表示不对内部字符串转义


## 函数的参数
* 位置参数
* 默认参数
* 可变参数
* 命名关键字参数
* 关键字参数

## import 模块然后使用时报“'Module' has no attribute names XXX”?
python import时会先查找当前目录，然后查找环境变量目录。如果你想要导入环境保量中的包，而恰巧当前目录中存在同名模块，那么就会报这个错误  
解决方法：在头部加上如下语句，意思为使用绝对路径导入，而非相对路径
```python
from __future__ import absolute_import
```

## json.dump()如何正确显示中文？
直接使用json.dump()会打印unicode编码，如果需要输出中文需要如下操作
```python
import codecs
import json

fp = codecs.open('file/path', 'w', encoding='utf-8')
json.dump(json_obj, fp, ensure_ascii=False, indent=2)
fp.close()
```

### 格式化输出报错"UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)"
```python
将
```

## 3*1**3 == 3
** 是幂运算，而且优先级比*要高

## is 和 == 有什么区别
* ==是比较运算符，用来比较两个值是否相等
* is是同一性运算符，用来比较两个对象是否相同

### 以下代码的原理
```python
a = 1
b = 1
a is b # True
a = 300
b = 300
a is b # False
```
因为python为了优化运行速度，使用了小整形对象池，即[-5, 256]之前的数字都已预先建立，所有相同的赋值均指向同一个对象。单字母同理

## 0.1 + 0.2 == 0.3 是False
因为python和javascript一样，采用IEEE754标准存储浮点值，该方式有截尾误差

### IEEE754
对单精度来说（32bit），有1个符号位，8个指数位，23个有效数字位  
对双精度来说（64bit），有1个符号位，11个指数位，52个有效数字位

## python 正则

### ^$和如何匹配行首和行尾
在re.search/match/findall的flag参数中提供re.M(多行模式)

## pip

## install 失败
```
$ pip install jsonschema
Collecting jsonschema
  Could not fetch URL https://pypi.python.org/simple/jsonschema/: There was a problem confirming the ssl certificate: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:661) - skipping
  Could not find a version that satisfies the requirement jsonschema (from versions: )
No matching distribution found for jsonschema
```
解决方式，信任该host
```
pip install jsonschema --trusted-host pypi.python.org
```

## python如何获取当前主机名称？
```python
import socket
hostname = socket.gethostname()
```
## python如何获取当前登录用户名？
```python
import getpass
print getpass.getuser()
```

## python在windows下mkdir报错：WindowsError?
可查询对应错误码，然后具体问题具体解决，比如是不能再不存在的目录下新建目录，比如目录名称不能包含不存在的字符

## python如何使用ssh
使用`paramiko`，必须python 2.7+ or python 3.4+

## UnicodeEncodeError: 'ascii' codec can't encode characters in position 26-29: ordinal not in range(128)
蛋疼的python2在print的unicode类型数据时，会出现这个错误（尽管已经设置`#coding:utf-8`）,原因是数据中包含非ascii字符。此时可以使用`print ret.encode('utf-8')`来强行指定编码


## pip install Error - ReadTimeoutError: HTTPSConnectionPool(host='pypi.python.org', port=443): Read
这是因为python库在境外，网络不好，可以通过国内镜像下载，这样就没事了
比如豆瓣镜像：[https://pypi.doubanio.com/simple/](https://pypi.doubanio.com/simple/)
```bash
python -m pip install --index https://pypi.doubanio.com/simple/ --upgrade pip
```
永久使用国内镜像的方法如下：
[https://www.jianshu.com/p/3621780417be](https://www.jianshu.com/p/3621780417be)

## python 显示文件夹中文件？
```python
from os import listdir
filelist = listdir('/home/cloud')
```

## 如何将dict格式的url参数转化为字符串？
如何该参数使用`urllib.parse_qs()`函数转化而来，那么可以使用`urlib.urlencode()`直接将其转化回去，因为`parse_qs()`函数默认会对参数进行urldecode

## pip安装指定版本？
pip install requests=2.3.6


## how to open and overwrite file?
```python
# no instact mode can be used, so try seek() and truncate
with open('path/to/file', 'r+') as fp:
    data = fp.read()
    new_data = func(data)
    fp.seek(0)
    fp.truncate()
    fp.write(new_data)
```