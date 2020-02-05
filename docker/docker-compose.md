# docker-compose

## docker redis connection refused
每个容器是分离的，无法直接用localhost访问，但是compose内部会将服务名注册为host，所以直接用 serviceName:port的方式访问即可
[Docker Redis Connection refused](https://stackoverflow.com/questions/42360356/docker-redis-connection-refused)