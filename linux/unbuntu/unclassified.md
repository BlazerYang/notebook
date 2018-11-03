# unclassified

## how to connect ubuntu in terminal?
ubuntu需要安装ssh服务
```bash
# 查看是否安装ssh服务
ps -ef | grep ssh
# 如果能看到ssh-agent说明ssh-client已安装、如果能看到sshd说明ssh-server已安
# 否则的话需要用安装对应软件

# ssh-client
sudo apt-get install ssh-client

# ssh-server
sudo apt-get install ssh-server

# 再次查看服务是否已经启动
ps -ef | grep ssh

# modify port
sudo gedit /etc/ssh/sshd_config

# restart ssh service
sudo /etc/init.d/ssh restart
```

## apt-get install cmake failed with "404 not found"?
1. ubuntu升级后软件库可能会迁移导致老版本软件无法更新，此时可以尝试手动更新软件库地址
```bash
sed -i -r 's/([a-z]{2}\.)?archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
sed -i -r 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list

apt-get update
```
那么如何查询ubuntu版本是否过时（EOL, End Of Life）呢
* `lsb_release -a` 查看当前ubuntu版本
* 在[https://wiki.ubuntu.com/Releases](https://wiki.ubuntu.com/Releases)查看当前版本是否已经过时

2. 直接去官网下载软件安装包
    1. wget \<cmake file url\>
    2. tar -zxvf cmake.tar.gz
    3. cd cmake.tar.gz
    4. ./configure --prefix=/usr/local/cmake
    5. make all
    6. make install
    7. cmake --version

## apt-get install failed with "E: Sub-process /usr/bin/dpkg returned an error code (1)"
办法如下：
```
sudo mv /var/lib/dpkg/info /var/lib/dpkg/info.bak //现将info文件夹更名
sudo mkdir /var/lib/dpkg/info //再新建一个新的info文件夹
sudo apt-get update
// 不用解释了吧
apt-get -f install xxx
sudo mv /var/lib/dpkg/info/* /var/lib/dpkg/info.bak
//执行完上一步操作后会在新的info文件夹下生成一些文件，现将这些文件全部移到info.bak文件夹下
sudo rm -rf /var/lib/dpkg/info //把自己新建的info文件夹删掉
sudo mv /var/lib/dpkg/info.bak /var/lib/dpkg/info //把以前的info文件夹重新改回名字
```
参考[ubuntu错误解决E: Sub-process /usr/bin/dpkg returned an error code (1)](http://yanue.net/post-123.html)