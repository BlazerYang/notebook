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
* Registry： 注册服

* 如何进入正在运行的容器中
  `nsenter --target ${PID} --mount --uts --ipc --net --pid`
  其中PID指的是容器pid，
  获取方式如下：
  `docker inspect --format "{{ .State.Pid }}" <container id | name>`
  container id可通过`docker ps`指令获取