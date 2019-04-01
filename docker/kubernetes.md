# kubernetes

## 如何区分是否应该将若干容器放在一个pod之中？
一个pod中放置的容器应该是强耦合的，所谓强耦合可以类比以前必须运行在一个服务器上、互相依赖的进程一样

## 实现基于docker的本地开发环境
1. docker-compose + volumn
    1. 后端代码通过挂载卷的方式加入容器
    2. 前端代码需要npm run dev的方式开发
2. scaffold
3. minikube