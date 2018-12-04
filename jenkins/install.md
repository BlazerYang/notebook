# install

## how to install jenkins in Ubuntu?
```bash
# add key to system
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -

# add following lines in /etc/apt/sources.list
# deb https://pkg.jenkins.io/debian binary/

# update local package index, then install jenkins
sudo apt-get update
sudo apt-get install jenkins

# start jenkins, default listen to 8080, could be modified in /etc/default/jenkins
/etc/init.d/jenkins start

# copy password and visit remoteIp:8080
cat /var/lib/jenkins/secrets/initialAdminPassword
```

## This Jenkins instance appears to be offline
可能是ssl问题，将配置文件中的https修改为http。
/var/lib/jenkins/hudson.model.UpdateCenter.xml
直接执行下面的命令
```bash
sudo sed -ir 's/https/http/g' /var/lib/jenkins/hudson.model.UpdateCenter.xml
```

## 忘记密码怎么办？
1. 如果密码没有修改过，那么直接`cat JENKINS_HOME/secrets/initialAdminPassword`可以看到密码
2. 如果密码已经修改过了，那么把`JENKINS_HOME/config.xml`从`<useSecurity>true</useSecurity>`到`</securityRealm>`之间的内容(含)全部删除
3. 重启jenkins: `service jenkins restart`
4. 此时可以用匿名用户免密进入jenkins，然后在`系统配置`/`全局安全配置`中 `启用安全`，勾选`允许用户注册`
5. 在`授权策略`中选择`安全矩阵`，然后添加对应的用户，并授予所有的权限，然后保存
6. 如果添加的用户是之前不存在的用户，那么在jenkins中需要注册，用户名相同即可


## 如何升级jenkins？
1. 下载最新版jenkins.war
2. 替换war包后启动，请用`ps -ef | grep jenkins`查询原始的启动命令进行启动