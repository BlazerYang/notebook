# index

## tomcat如何查询登陆用户名和密码
linux下先使用whereis tomcat查看安装目录，然后在安装目录下的/conf/tomcat-users.xml中的user标签内即可看到可用的用户名和密码

## tomcat如何新建仅部署静态文件的项目
1. 找到tomcat的安装目录
2. ./webapps下新建项目，然后直接把静态文件放在里面
3. 运行./bin/shutdowm.sh和./bin/startup.sh重启tomcat