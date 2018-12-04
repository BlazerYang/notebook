# index.md

## redis windows安装后第一次启动时报错 `[12928] 19 Jun 15:21:56.196 # Creating Server TCP listening socket 127.0.0.1:6379: bind: No error`,什么原因？如何解决？
解决方式：
1. 运行`redis-cli.exe`
2. 分别输入`shutdown`,'exit'
3. 再次启动即可恢复正常 `redis-server.exe redis.windows.conf`
原因: TODO

### cli 中 shutdown指令？
执行如下操作：
1. 停止所有客户端
2. 如果配置了save策略，则执行一个阻塞的save命令
3. 如何开启了AOF，则刷新aof文件
4. 关闭redis-server服务进程

### exit指令？
并非redis-cli指令，而是window退出脚本执行

## redis-cli参数

### -n
指定number，类似mysql的schema，通过不同的数字来连接不同的数据库，默认是`0`, 如果连接的不是0，会在连接后出现提示：
```
X.X.X.X:40000[1]> get 1531208200361
```
## CAS
check and set, watch指令可以检测keys，在一次事务操作期间，如果keys被其他client修改，那么该事务将回滚，不做执行任何动作，以保证事务原子性

## redis和memcached有什么区别？
1. redis不仅支持kv存储，还支持list，set，hash等数据结构
2. 支持主从数据备份
3. 支持数据持久化，内存的数据可以保存在磁盘中，重启的时候可以再次加载


## 如何查看redis版本？
连接之后输入`info`