# index

## how to restart nginx?
nginx -c /path/to/nginx/conf

## how to reload conf modification ?
`nginx -s reload`
* reload 是平滑重启

## 经nginx代理过的请求的REMOTE_ADDR中如何带上真实的客户端ip？
按照以下两步进行操作即可：  
1. 在代理服务器的配置中加入请求头设置 `proxy_set_header    X-Real-IP    $remote_addr;`
2. 在下游服务器的配置中加入`fastcgi_param REMOTE_ADDR $http_x_real_ip;`将代理服务器的地址替换为真实客户端ip
3. 注意如果直接访问下游服务器的话，`$http_x_real_ip`的值为空，如果该服务器也可能被直接访问，需要在nginx中判断是否为空

## resquest nginx but get 499 http-code, but time only elapsed 1s
原因为生产服务器未加入数据库白名单，php请求数据库链接超时(耗时约1分钟才会抛出异常)，nginx在1s后就会超时返回。
在nginx配置中添加如下字段, 让nginx不要主动断开连接
```nginx
server {
    proxy_ignore_client_abort on;
    fastcgi_ignore_client_abort on;
}
```

## nginx如何在header中增加path_info
1. 重写必须带上index.php
2. 对uri进行正则匹配，fastcgi_split_path_info
3. pathinfo信息会赋予 $fastcgi_path_info
4. 将其赋给fastcig： fastcgi_param PATH_INFO $fastcgi_path_info;
```conf
server
{
    listen 8364;
    server_name X.X.X.X;
    root /var/www/html/pccheck;
    index index.php;
    error_log /data/nginx/logs/pccheck.error.log debug;

    if ($request_filename !~* ^/(.*)\.(js|ico|gif|jpg|png|css|php|xml|txt|html|swf|apk|ipa)$)
    {
        rewrite ^/(.*)$ /index.php/$1 last;
    }

    location / {
        allow 127.0.0.0/24;
        deny all;
        index /index.php;
        try_files $uri $uri/ /index.php;
    }

    location ~* \.php($|/) {
        include fastcgi.conf;
        fastcgi_split_path_info  ^(.+\.php)(.*)$;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_param REMOTE_ADDR $http_x_real_ip;
        fastcgi_pass 127.0.0.1:9000;
    }
}
```

## nginx如何打印调试信息？
```nginx
server {
    error_log /data/nginx/logs/pccheck.error.log debug;
}
```

## nginx如何配置项目前后端分离
1. 配置前端接收所有请求，根据url将后端请求proxy_pass过去
```nginx
server {
  listen 80;
  server_name yourhost;

  gzip              on;
  gzip_buffers      16 8k;
  gzip_comp_level   9;
  gzip_min_length   1024;
  gzip_types        text/plain application/x-javascript application/javascript text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png;
  gzip_vary         on;

  proxy_set_header        X-Real-IP       $remote_addr;

  location / {
    root /home/q/system/tanzhen/dist;
    index index.html;
    try_files $uri $uri/ /index.html;
  }

  location /tanzhen/ {
    proxy_pass http://localhost:8362;
  }

  location /uploads/ {
    proxy_pass http://localhost:8362;
  }

}
```
2. **后端正常配置即可**
```nginx
server
{
    listen 8362;
    server_name X.X.X.X;
    root /var/www/html/tzbe;
    index index.php;

    location / {
        allow 127.0.0.0/24;
        deny all;
        index /index.php;
        try_files $uri $uri/ /index.php;
    }

    location ~* \.php$ {
        include fastcgi.conf;
        fastcgi_param REMOTE_ADDR $http_x_real_ip;
        fastcgi_pass 127.0.0.1:9000;
    }
}
```