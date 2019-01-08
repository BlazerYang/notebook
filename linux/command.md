# command

## how to get exists groups?
```bash
# get all groups and its users
cat /etc/group
# get current user(or specific user) and its group
groups [root]
```

## how to adduser?
```bash
adduser username groupname
# initial password is empty, cannot login unless you set password
passwd username
```

## how to add group?
```bash
addgroup GROUPNAME
# or groupadd, they're the same thing
```

## what is nobody user in linux?
系统的最小权限，相当于window的匿名用户，只允许执行一些所有账户都有权限执行的操作

## how to exit from su?
simply type exit in cmd

## how to configure sudo access?
visudo  
For details, pls refer to[⁠2.3. Configuring sudo Access](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/2/html/Getting_Started_Guide/ch02s03.html)

for passwd-free add following sentence in config:
```
jenkins ALL = (ALL) NOPASSWD: ALL
```

## how to exit from sudo?
`exit`

## search and replace in vi?
```bash
# search and replace the next ONE search
:s/search/replacement
# search and replace all search
:%s/search/replacement
```

## how to get encoding of file?
type this in vi
`:set fileencoding`

## what is difference between su and sudo?
* **su**, switch to root only in capacity, but context still stay the same
* **su -**, switch to root both in capacity and context
* **sudo**, only run a single command whit root privileges, don't need to know root's password
* **sudo su**, call su with sudo. Bash is call as interactive non-login shell.   
For defail, refer to ['sudo su -' vs 'sudo -i' vs 'sudo /bin/bash' - when does it matter which is used, or does it matter at all?](https://askubuntu.com/questions/376199/sudo-su-vs-sudo-i-vs-sudo-bin-bash-when-does-it-matter-which-is-used)

##how to add directory into environment variables?
重启后会失效
```bash
export PATH=$PATH:/home/guozhenhua/node/bin
```
如果希望登陆后生效，可将上述语句加入~/.bashrc或者/etc/profile  
如果希望重启后立即生效，可将上述语句加入/etc/rc.local

### /etc/profile ？
为系统的每个用户设置环境信息，当用户第一次登录时，该文件被执行  
登陆linux需要执行的文件为：   
`/etc/profile` -> (`~/.bash_profile` | `~/.bash_login` | `~/.profile`) -> `~/.bashrc` -> `/etc/bashrc` -> `~/.bash_logout`  
其中存在`~/.bash_profile`时，才会尝试执行`~/.bashrc`文件

### /etc/bashrc
为每一个运行bash shell的用户执行此文件.当bash shell被打开时,该文件被读取（即每次新开一个终端，都会执行bashrc）。

### ~/.bash_profile
每个用户都可使用该文件输入专用于自己使用的shell信息,当用户登录时,该文件仅仅执行一次。默认情况下,设置一些环境变量,执行用户的.bashrc文件。

### ~/.bashrc
该文件包含专用于你的bash shell的bash信息,当登录时以及每次打开新的shell时,该该文件被读取。

### ~/.bash_logout
当每次退出系统(退出bash shell)时,执行该文件. 另外,/etc/profile中设定的变量(全局)的可以作用于任何用户,而~/.bashrc等中设定的变量(局部)只能继承 /etc/profile中的变量,他们是"父子"关系。

### ~/.bash_profile
是交互式、login 方式进入 bash 运行的~/.bashrc 是交互式 non-login 方式进入 bash 运行的通常二者设置大致相同，所以通常前者会调用后者。

## source ?
equal to dot command(.), enable initialization file modification without re-login

## sed

## configure?
编译器开始工作之前，需要知道当前的系统环境，比如标准库在哪儿、软件安装位置、需要哪些组件等，因为操作系统的差异，所以需要通过配置(configure)来指定这些参数，使得程序可以编译出各种环境都能运行的代码。
```bash
./configure --prefix=/usr/local/php --with-mysql
```

## make?
make指令在当前目前找到makefile文件，然后按照内容指示编译文件。那么makefile又是什么呢？makefile中存储的是源码文件的编译顺序，因为大型项目中源码文件一般会存在依赖关系，而编译器需要保证各模块按照依赖顺序完成编译。

### 预编译(Precompilation)
对头文件进行编译，确保每个头文件只会被编译一次

### 预处理(Preprocessing)
替换源码中bash的头文件和宏

### 编译(Compilation)
生成机器码

### 连接(Linking)
将外部函数代码（.lib或.a）添加到可执行文件中。**其中通过拷贝外部函数库到可执行文件中的方式叫做静态连接**。在运行时动态引入的方式为动态连接（linux下的.so, window下的.dll, macOS下的.dylib）

## cmake
因为不同的平台的make工具有不同的标准和规范，执行的makefile文件格式也是千差万别。cmake为开发者提供一种编写平台无关的CMakeList.txt文件以定制整个编译流程的工作方式，然后在根据目标用户的凭条进一步生成所需的本地化makefile

## .bz2文件如何解压？
```bash
bzip2 -d rpm.tar.bz2
```

## 查看系统版本号
* cat /proc/version
* cat /etc/issue
* cat /etc/redhat-release //centos7只有这个
* lsb_release -a


## 后台启动程序
```bash
nohup sh your_script.sh param1 param2 > /dev/null 2>&1 &
```

## how to change tabsize in vi
1. in vi at ":" prompt type: `set ts=4` or `set tabstop=4`
2. in ~/.vimrc add
```
set tabstop=4
```

## vi如何临时显示gbk编码文件？
`:e ++enc=gbk`

## 如何配置防火墙

### 如何设置指定本机8361端口只允许特定ip访问
1. 禁止所有ip访问本机8361端口
iptables -I INPUT -p tcp --dport 8361 -j DROP
2. 允许10.18.61.27访问本机8361端口
iptables -I INPUT -s 10.18.61.27/24 -p tcp --dport 8361 -j ACCEPT
3. 允许本机通过外网ip访问本机8361端口
iptables -I INPUT -s 10.173.222.113 -p tcp --dport 8361 -j ACCEPT

* -I Insert, 插入新的规则
* -p protocol, 通过数字或名字指定协议
* -dport destination port, 目的端口
* -s, --source 指定源
* -j jump, 指定要执行的动作，主要有ACCEPT, DROP, REJECT, LOG
* -P, --policy 指定chain target

#### DROP 和 REJECT的区别？
* DROP直接丢弃数据包
* REJECT丢弃之后会返回一个ICMP错误信息包

#### chain是啥？
数据包的传递链条，对于filter表来说，有OUTPUT, INPUT 和 FORWARD三个
* OUTPUT, 从本机发出至其他机器的
* INPUT, 从其他机器发往本机的
* FORWARD, 经由本机转发的

### 如何显示已经设置的规则
1. iptables -S，按照设置来显示规则
2. iptables -L, 按照表格来显示规则

### 如何删除已经设置的规则
使用-D选项加上规则定义
iptables -D INPUT -s 10.18.61.27 -p tcp -dport 8361 -j ACCEPT

## 规则是先写入的在后方


## scp如何实现免密码？
1. 使用sshgen在本地生成rsa密钥对, 生成的`id_rsa`和`id_rsa.pub`保存在`~/.ssh`中
2. 其中`id_rsa.pub`存储的是公钥，将其中内容拷贝至scp所用的用户名对应的`~/.ssh/authorized_keys`中
  1. 注意：如果是新建的`authorized_keys`文件，权限应为600，否则无效
3. 手动scp一次，确认服务器指纹即可

* 当添加无效时，注意需要设置`authorized_keys`权限为600, 父文件夹`.ssh`权限为700

## 如何测试远程端口是否开启？
`ssh -v -p port ip|hostname`
如果回显出现connected，那么端口通着的



## 终端下中文乱码
`export LANG=zh_CN.UTF-8`即可，可将该语句放在`~/.bashrc`中，确保每次登陆后均生效


## free指令
```bash
[cloud@var102 ~]$ free -g
             total       used       free     shared    buffers     cached
Mem:           283        169        114          0          0        159
-/+ buffers/cache:          9        274
Swap:           59          0         59
```
可以参考 [Linux 系统缓存机制](https://blog.csdn.net/yangwenbo214/article/details/74061988)

## 如何删除目录下最老的几个文件？
该命令删掉文件夹在最老的1000个文件
`ll -rt | grep -v total | awk '{print $9}' | head -n 1000 | xargs rm -f`

## grep
### 查找所有子目录
`-r`

### 仅搜索指定后缀文件
`--include="*.conf"`

## 如何查看host配置？
`vi /etc/hosts`

## ulimit？
操作系统提供限制可使用资源量的方式

## linux硬件时间和系统时间不一致怎么办？
先介绍三个指令: `clock`, `hwclock`, `date`
其中前两个指令可以查看硬件时间，后一个可以查看系统时间
系统时间可以任意修改以满足op需求。同步时间指令：
`h**wc**lock --systohc`, 用系统时间来设置硬件时间
`hwclock --hctosys`, 用硬件时间来设置系统时间
一般程序读取的是系统时间

## 如何从日志中查询出满足摸个匹配到后方第一个空行之间的内容？
利用`sed`指令,具体指令如下：
```bash
# 比如要查询 c=task&a=add 到下方第一个空行之间的内容
sed -n '/c=task\&a=add/,/^\r$/p' ./*
```

## 如何查看指令的执行进度
可以用`pv`, 名称来自pipe viewer

## POSTFIX
基于linux的邮件发送服务， [postfix工作原理](https://www.jianshu.com/p/ec59689a1a12)

### 如何启动？
`service postfix start`

### 如何查看postfix日志？
`/var/log/maillog`

#### 如何理解日志内容？
```log
Oct 22 10:15:09 k12336v postfix/smtpd[24058]: connect from localhost[127.0.0.1]
Oct 22 10:15:09 k12336v postfix/smtpd[24058]: D0988339C: client=localhost[127.0.0.1]
Oct 22 10:15:09 k12336v postfix/cleanup[24064]: D0988339C: message-id=<a806ef04cf38577c6af192a4de2dba0d@qixiao.gmail.com>
Oct 22 10:15:09 k12336v postfix/qmgr[2862]: D0988339C: from=<test@alarm.gmail.com>, size=10788, nrcpt=5 (queue active)
Oct 22 10:15:09 k12336v postfix/smtpd[24058]: disconnect from localhost[127.0.0.1]
Oct 22 10:15:10 k12336v postfix/smtp[24066]: D0988339C: to=<john@gmail.com>, relay=tfw.gmail.com[123.123.123.13]:25, delay=0.43, delays=0.07/0.03/0.09/0.23, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as 02EAED6155)
Oct 22 10:15:10 k12336v postfix/smtp[24066]: D0988339C: to=<tom@gmail.com>, relay=tfw.gmail.com[123.123.123.13]:25, delay=0.43, delays=0.07/0.03/0.09/0.23, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as 02EAED6155)
Oct 22 10:15:10 k12336v postfix/smtp[24066]: D0988339C: to=<susan@gmail.com>, relay=tfw.gmail.com[123.123.123.13]:25, delay=0.43, delays=0.07/0.03/0.09/0.23, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as 02EAED6155)
Oct 22 10:15:10 k12336v postfix/smtp[24066]: D0988339C: to=<smith@gmail.com>, relay=tfw.gmail.com[123.123.123.13]:25, delay=0.43, delays=0.07/0.03/0.09/0.23, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as 02EAED6155)
Oct 22 10:15:10 k12336v postfix/smtp[24066]: D0988339C: to=<josh@gmail.com>, relay=tfw.gmail.com[123.123.123.13]:25, delay=0.43, delays=0.07/0.03/0.09/0.23, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as 02EAED6155)
Oct 22 10:15:10 k12336v postfix/qmgr[2862]: D0988339C: removed

```  


1. 其中的delay显示总耗时，delays=a/b/c/d, a指进入队列管理器之前的耗时，b指队列管理器排队的耗时，c指建立连接的耗时，d指邮件发送的耗时
    >Postfix logs additional delay information as "delays=a/b/c/d" where a=time before queue manager, including message transmission; b=time in queue manager; c=connection setup time including DNS, HELO and TLS; d=message transmission time.

### queue manager 是啥？
postfix queue manager, AKA qmgr。该进程由postfix master进程管理器启动，监听邮件投递并负责发送

### DSN是啥？
DSN是delivery status notification

包括四种：fail，delay，success，address verification

[Postfix DSN消息](https://blog.csdn.net/propro1314/article/details/39003843)


### service postfix start 失败，如何查看错误日志？
直接`postfix start`可以看到错误信息

### postfix: fatal: parameter inet_interfaces: no local interface found for ::1 如何处理？
1. open `/etc/postfix/main.cf`
2. comment out `inet_protocol: all`
3. add `inet_protocol: ipv4`

### linux下sendmail、mail和postfix之间什么关系？
* mail是邮件客户端，其将邮件投递给本地MTA，然后MTA（比如sendmail,postfix）负责将邮件投递至收件人
* sendmail和postfix都是邮件服务器，真正收发邮件的就是这些服务
[Difference between mailx and sendmail?](https://stackoverflow.com/questions/51731199/difference-between-mailx-and-sendmail)

#### what is MTA?
short of `Mail Transfer Agent`，邮件转发代理

### 如何查看邮件队列？
mailq

### 如何发送队列中的邮件？
`postqueue -f` or `postqueue flush`

### postqueue: fatal: Cannot flush mail queue - mail system is down?


### why mailq have lot of requests?


### 如何清空mail队列？
postsuper -d ALL

### mail队列中提示450 too much mail怎么办？postfix会重发么？
>said: 450 4.7.1 Error: too much mail from 10.145.28.114 (in reply to MAIL FROM command)

## 如何清理dnscache？
service nscd reload
* windows下：ipconfig /flushdns


## root用户如何查看所有人的cron？
`cut -d: -f1 /etc/passwd|xargs -i sudo crontab -u {} -l`
* `cut -d: -f1`:
  > use `:` instead of TAB for field delimiter
  > select only these fields;  also print any line that contains no delimiter character, unless the -s option is specified
* xargs -i: 
  > This option is a synonym for -Ireplace-str if replace-str is specified, and for -I{} otherwise.  This option is deprecated; use -I instead.
* crontab -u:
  > Append the name of the user whose crontab is to be tweaked.  If this option is not given, crontab examines "your" crontab, i.e., the crontab of the person executing the command.

## 如何统计文件下下所有文件的数量(包括子文件夹)？
`ls -lR| grep "^-" | wc -l`


## locale
[Linux下LC_ALL=C的含义](https://blog.csdn.net/ict2014/article/details/23946471)