# MAVEN

## maven compile时提示 “No compiler is provided in this environment. Perhaps you are running on a JRE rather than a JDK?”
在环境变量中添加"JAVA_HOME"指定jdk的目录

## maven错误解决：编码GBK的不可映射字符
修改pom.xml文件，在build/plugin/configuration中增加`<encoding>UTF-8</encoding>`
参考链接：[maven错误解决：编码GBK的不可映射字符](https://blog.csdn.net/EvelynHouseba/article/details/16114353)

## 如何使用阿里的源？
找到maven软件根目录下的 ./conf/settings.xml, 在`<mirrors></mirrors>`章节添加如下语句：
```xml
<mirror>
    <id>aliyunmaven</id>
    <mirrorOf>*</mirrorOf>
    <name>阿里云公共仓库</name>
    <url>https://maven.aliyun.com/repository/public</url>
</mirror>
```

## 如何安装mvn依赖？
```
mvn clean install
```

## “The project was not built since its build path is incomplete. Cannot find the class file for hudson.model.Descriptor. Fix the build path then try building this project”，如何解决？
可能与vscode所用的java插件有关（eclipse团队制作）
1. 设置maven插件的配置文件地址：
`"java.configuration.maven.userSettings": "D:\\Program Files\\apache-maven-3.6.1\\conf\\settings.xml"`
2. 使用eclipse:clean后再安装一遍
`mvn clean eclipse:clean eclipse:eclipse`

## spring tools 提示错误 “missing LineBreak at 'u'”
`swagger.title=\u5947\u6548\u6d41\u6c34\u7ebf`