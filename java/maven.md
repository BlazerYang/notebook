# MAVEN

## maven compile时提示 “No compiler is provided in this environment. Perhaps you are running on a JRE rather than a JDK?”
在环境变量中添加"JAVA_HOME"指定jdk的目录

## maven错误解决：编码GBK的不可映射字符
修改pom.xml文件，在build/plugin/configuration中增加`<encoding>UTF-8</encoding>`
参考链接：[maven错误解决：编码GBK的不可映射字符](https://blog.csdn.net/EvelynHouseba/article/details/16114353)