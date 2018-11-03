# nosetests

## 如何执行单个用例？
```bash
# 自动查找当前文件下所有的用例
nosetests
# 指定某个目录执行
nosetests your/tests/path
# 指定文件执行
nosetests your/tests/path/file.py
# 指定文件中的某个类中的方法执行
nosetests your/tests/path/file.py:TestClass.method
```

## nosetests如何编写插件，可以在测试类初始化时传递参数，或者在设置可以在setup()中读取的变量？
1. 定义类继承nose.plugins.Plugin，然后实现对应的接口


## unittest获取docstring时中文乱码
C:\Python27\Lib\unittest\case.py:261, 将return的值加上unicode(), 设置encoding='utf-8'即可
```python
        # return doc and doc.split("\n")[0].strip() or None
        return doc and unicode(doc.split("\n")[0].strip(), encoding='utf-8') or None
```

## nosetests用例failure时如何输出打印信息？
加上选项--nocapture

## nosetests如何获取一次运行运行中所有的错误信息？


## nosetests不支持subclass中的generator成员函数，仅支持generator方法

## generator