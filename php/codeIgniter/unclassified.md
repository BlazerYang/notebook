# unclassified

## how to use nginx as webserver for ci?
modify application/config/config in ci make sure that `$config['uri_protocol'] = REQUEST_URI`  
then enable fastcgi in nginx.  
For detail,[use codeigniter with nginx](https://www.nginx.com/resources/wiki/start/topics/recipes/codeigniter/)

## can not connect to mysql after update from php5 to php7?
```
ERROR - 2017-11-22 14:46:58 --> Severity: Warning  --> mysqli_connect(): (HY000/2002): No such file or directory /var/www/html/rm/system/database/drivers/mysqli/mysqli_driver.php 77
```
if your database configure to connect to 'localhost' , you should replace it with '127.0.0.1'

## ci控制器名称默认会去查找首字母大写的，linux下会区分大小写