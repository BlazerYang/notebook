# errno

## what is HTTP connection refused[111] mean? And what is the reason for?
报connection refused的原因很多的，以下列举常见的3个  
1. 没有进程监听所请求的ip:port
2. 挂起连接数已经打满，新来的请求会被refuse掉
3. 对该ip:port的请求被防火墙拦截
