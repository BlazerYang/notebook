# index

## 推荐阅读：
1. 《Docker技术入门与实战 第2版》

### 《Docker技术入门与实战 第2版》 笔记

* 为什么用Docker?
    1. 更高效的系统资源利用
    2. 更快的启动时间
    3. 一致的运行环境
    4. CI/CD
    5. 易于迁移
    6. 易于维护和扩展

* 分层存储是什么？
一个docker镜像并不会包含一个单独的文件系统，而是由多层文件系统联合组成。镜像的构建是一层一层进行的，前一层是后一层的基础。每一层构建完成就不会再发生改变，后一层的任何改变只发生在自己这一层。

* 容器存储层
容器存储层的生命周期同容器一致，所以写在其中的数据会随着容器的删除而消失。所有需要写入文件的操作都应该是用数据卷(Volume)或者绑定宿主目录，这样数据写入就可以跳过容器存储层，直接对宿主目录(或网络存储)发生读写

* 如何查看已经下载的镜像？
    ```
    docker images
    ```

* `docker pull`获取的镜像存储在哪里？  
`/var/lib/docker/containers`，每个hash值都是一个镜像

* 虚悬镜像(dangling image)  
因为官方镜像维护发布新版本之后，已有的 名称:标签 被占用，原镜像的名称或标签会出现为`none`的情况，这种镜像称为虚悬镜像

* 查看当前正在运行的容器  
  `docker ps`
  `docker ps -a`, 可查看所有启动的容器(不仅是运行中的)

* 查看当前运行容器的资源占用情况  
  `docker stats`

* 查看指定容器内部进程情况
  `docker top [NAME]`

* 使用save加load发送镜像（不推荐）  
`docker save <镜像名> | bzip2 | pv | ssh <用户名>@<机器名> 'cat | do
cker load'`  
推荐使用regsitry来传递镜像

* Repository: 仓库
* Registry： 注册服务器

* 如何进入正在运行的容器中
  `nsenter --target ${PID} --mount --uts --ipc --net --pid`
  其中PID指的是容器pid，
  获取方式如下：
  `docker inspect --format "{{ .State.Pid }}" <container id | name>`
  container id可通过`docker ps`指令获取


## 
docker run -itd --entrypoint=/bin/bash r.bingo.soft.798.cn/qixiao/qixiao-socket:qixiao.socket-hotfix-docker-20181113104911-499404f
docker exec -it a748c2c5dadb /bin/bash env | grep HOME

## 如何退出容器不关闭？
1. `docker attach 容器id`, 进入容器需要按如下方法退出，不然容器会关闭
`ctrl+p+q`
2. `docker exec -it 容器id /bin/bash`, 这种方法进入再退出不会关闭容器

## 如何查询可用的镜像列表？
`docker search mysql`

### 查询可用列表之后，如何获取其对应的tag信息？
`curl -s -S 'https://registry.hub.docker.com/v2/repositories/library/mysql/tags/' | jq '."results"[]["name"]' |sort`

### 如何拉取tag对应的镜像
`docker pull mysql:5.6`

### 如何启动mysql镜像？
`docker run --name some-mysql -v /home/yangxuefei/var/lib/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql:5.6`

* `-e`：用于设置容器中的环境变量，`MYSQL_ROOT_PASSWORD`用于设置用户密码， 如果不想使用密码可以使用配置免密`MYSQL_ALLOW_EMPTY_PASSWORD`

### 如何连接上mysql镜像？
`docker run -it --link some-mysql:mysql --rm mysql:5.6 sh -c 'exec mysql -h172.17.0.2 -P3306 -uroot -proot'`

其中`-h`为容器的ip

### 如何查看container的ip？
`docker inspect --format '{{ .NetworkSettings.IPAddress }}' dockerid`

### 如何从容器保存为镜像？
1. `docker ps -a`获取容器的id
2. `docker commit {container id} /{namespace}/{name}:{tag}`


## docker 在Dockerfile中修改/etc/hosts/为何不生效？
/etc/hosts文件并不是保存在容器的fs中，而是挂载在宿主机保存容器的目录里，而每次启动均会生成一个新的容器，所以中间层中对/etc/hosts的修改并不会生效。
如要在容器启动命令中修改才可以