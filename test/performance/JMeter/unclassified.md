# unclassified

## 采样器结果中中文乱码如何解决？
JMeter默认编码格式为ISO-8859-1,并不支持中文，有两种解决办法：
1. 对采样器添加后置处理器修改字符编码
    1. 添加->后置处理器->BeanShell后置处理器
    2. 在script中添加prev.setDataEncoding("UTF-8");
2. 修改JMeter默认编码
    1. 打开./bin/jemter.properties
    2. 找到下面的配置，去掉samplresult.default.encoding的注释，并将其修改为UTF-8
        ```
        # The encoding to be used if none is provided (default ISO-8859-1)
        #sampleresult.default.encoding=ISO-8859-1
        ```
    3. 重启JMeter后生效

## BeanShell是什么？里面的script支持什么语法？
基于java的源代码解释器，符合java语法规范，并扩展了自己的语法和方法; 类似于JS的松散类型。  
具体可以参考[BeanShell文档](http://www.beanshell.org/manual/contents.html)

## BeanShell中的prev？
prev是BeanShell的一个内置变量，指的是上一个采样器的结果对象。此外还有一些其他常用变量
* log：写入信息到jmeter.log文件
* ctx: 当前线程上下文对象，使用方法参考[org.apache.jmeter.threads.JMeterContext](http://jmeter.apache.org/api/org/apache/jmeter/threads/JMeterContext.html)
* vars: 当前JMeter线程中的局部变量容器的应用，测试用例与BeanShell交互的桥梁，详见[org.apache.jmeter.threads.JMeterVariables](http://jmeter.apache.org/api/org/apache/jmeter/threads/JMeterVariables.html)
* props: jmeter配置对象的引用，可以获取JMeter属性，用法与vars类似，但只能put进去string而不是对象，对应于java.util.Properties
* sampler: 当前采样器的引用

## 后置处理都支持什么？
* BeanShell，见上
* CSS/JQuery提取器，支持JSOUP和JODD两种解析器，语法差不多。使用的时候在请求上添加，设置好引用名称（JMeter变量），然后再添加debug sampler，运行脚本后，即可再查看结果树中查看变量中抓取到的值

## JSOUP？
基于java的HTML的解析器，可从url、文件和字符串中解析。  
详情参考[jsoup docs](https://jsoup.org/)

## JODD?


## .jtl?
containing result of rest run  
there are two type of JTL file:
* XML
* CSV

## .jmx?
Java Management eXtension, 为java应用程序植入管理功能的框架

## CSV DATA SET CONFIG?
利用该功能可以从文件中读取数据替换采样中的参数化变量

## 如何生成唯一的随机值？
```
${__time(,)}${__threadNum}
```

## 如何使POST body中的数据的换行符为\r 而非 \n\r
先添加一个变量`variable`作为换行符
然后在http下添加一个beanshell前置处理器
```java
vars.put("variable", "\n")
```