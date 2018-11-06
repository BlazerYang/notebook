# unclassified

## git 库作为若干项目的集合，每次如何只拉取其中一个路径下的文件、更新？
sparse checkout, 但是共用仓库的方式还是不方便，每个项目应该独立仓库

## 如何自建git服务器？
找一台7*24开机的机器作为服务器, 然后执行如下指令：
```bash
# 登陆该服务器，新建git组
addgroup git
# 添加用户git
adduser git git
# 设置密码（否则无法登陆）
passwd git
# 初始化git仓库
git init
# 然后可以尽情克隆了
git clone git@ip_addr:/path/to/repo.git local_path
```
[参考阅读](http://www.runoob.com/git/git-server.html)

## git push如何免密码？
https连接下使用  
git config --global credential.helper store  

ssh连接下将自己的机器的公钥提交给服务器,步骤如下  
1. 查看是否存在~/.ssh/id_rsa、~/.ssh/id_rsa.pub,如果没有，继续步骤2，否则直接步骤3
2. 生成rsa密钥对`ssh-keygen -t rsa -C 'youmail@gmail.com'`
3. 将~/.ssh/id_rsa.pub 加入到git服务器~/.ssh/authorized_keys中
4. 本地在~/.ssh中新建config文件(可以使用别名连接git服务器)，内容如下
```
Host gitserver
HostName 10.18.60.140
User git
Port 22
IdentityFile ~/.ssh/id_rsa
```
5. 之后再进行git push/pull/fetch就不再需要密码了

## 本地库如何推到远程库？
1. 远程新建仓库
2. 克隆至本地
3. 添加文件
4. git add .
5. git commit -m 'comment'
6. git push

## 如何设置git log中显示的用户名和邮箱
1. 通过命令行设置  
>git config global --config user.name 'yourname'  
git config global --config user.email 'youemail@gmail.com'  
2. 直接设置配置文件，法1.中的设置最后也是修改的配置文件  
>~/.gitconfig  
[user]
  name = yourname
  eamil = youemail@gmail.com

## 如何强制使用远程覆盖本地分支
* git pull -f
* 如何提示本地有变更需要提交，那么可以用
```
git fetch --all
git reset --hard origin/master
git pull
```

## 已经添加至版本控的文件如何忽略？
1. 首先添加至.gitignore中
2. 将文件从版本库中删除，git rm --cached \<filename\>

## 如果保存目录结构但是忽略其中的文件？
git默认不会保留空目录，常见方法是在目录中添加一个跟踪的文件(.gitkeep/.keep)，名字随意，内容为空。然后指定忽略特定后缀的文件

## No refs in common and none specified; doing nothing.
Perhaps you should specify a branch such as 'master'
解决方式：
git push origin master

## git remote add <name> <url>发生了什么？
新增了全程仓库地址，name一般叫做origin

## git push -u origin master?
同下方语句相同
git push --set-upstream origin master
作用是将当前分支推送至origin/master分支，同时将本地分支同远程分支关联起来

## 如何撤销在当前工作区的修改？
`git checkout -- filename.txt`

## git忽略权限变更
git config core.filemode false
对于已经提交的由权限变更引起的变动，则无效，此时可用reset恢复

## 由于windows和linux下换行符处理不一致的引发的git ^M如何消除？
提交检出均不转换  
git config core.autocrlf false

## 拉取远程分支到本地？
git checkout remotes/origin/develop -b develop

## git如何避免三方合并冲突？
1. 本地提交要尽快推送到远端
2. 本地开发之前要先把远程代码拉下来

## git 刷新远程分支？
```
git remote update origin --prune
```

## git如何删除远程分支？
`git push origin :feature_v1.3.0`

## git打的tag为什么只在本地有，远程看不到？
因为`git push`并不会推送tag到远程，需要显式推送
1. 推送全部tag： `git push [origin] --tag`
2. 推送单个tag:  `git push [origin] tag_name`

## git 拉代码的时候出现"segmentation fault"后导致代码没有拉取完全？
window和linux对文件命名规则不一样时，有可能出现linux下提交的代码在window下无法通过校验进而导致出现该问题。  
解决方案：
1. linux下删除或重命名该非法命名文件
2. window下进行浅拉取 `git clone --depth=1 repo_name.git foldername`