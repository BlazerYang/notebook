# plugins.md

## publish over ssh 如何配置免密连接？
1. 在应用服务器的~/.ssh/authorized_keys中填写jenkins服务器对用用户的公钥
2. 在jenkins/系统管理/配置管理中，找到publish over ssh,点击新增
3. 在`Path to key`中填写对应用户私钥的路径
4. 在`Hostname`中填写应用服务器的ip，在`Uername`中填写用户名
5. 点击`Test Configuration`显示`success`即为成功

## email extension 如何配置？
说几点需要注意的地方：
1. 如果使用的163邮箱，注意用户密码使用授权码而不是用户密码
2. 用户邮箱需要和jenkins locaiton中的系统管理员邮箱一致

## git

### Failed to connect to repository : Command "git ls-remote -h localhost:/home/git/tzfe HEAD" returned status code 128:？
原因是当前用户的公钥没有添加至git的白名单中，解决办法如下：
1. `sudo -u jenkins -H bash && cd ~`: 切换至jenkins用户，并进入home目录
2. `ssh-keygen -t rsa`: 如果`~/.ssh/`中没有`id_rsa.pub`文件，那么就生成一个
3. 将`id_rsa.pub`中的内容粘贴指git服务器的`authorized_keys`中

## Allure

### post action中选择中allure之后，系统会卡死
推测是运行结果大多，或者不连续导致任务卡死，总之将`%JENKINS_HOME%/workspace/%JOB_NAME%/allure-results/`清空之后任务即可恢复正常

* 续： 清理之后一段时间还是会卡死，检查发现workspace/{JOB_NAME}/allure-results中内容还是过多
* 解决方式：在post action中增加“Delete workspace when build is done”清除历史运行数据和报告。因为处理好的报告是存储在jobs/{JOB_NAME}/{INDEX}/allure中的，所以报告不会清除