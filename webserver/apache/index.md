# index.md

## apache2 -k start时报错
>[Wed Jan 03 15:28:39.278441 2018] [core:warn] [pid 21434] AH00111: Config variable ${APACHE_LOCK_DIR} is not defined
[Wed Jan 03 15:28:39.278526 2018] [core:warn] [pid 21434] AH00111: Config variable ${APACHE_PID_FILE} is not defined
[Wed Jan 03 15:28:39.278551 2018] [core:warn] [pid 21434] AH00111: Config variable ${APACHE_RUN_USER} is not defined
[Wed Jan 03 15:28:39.278567 2018] [core:warn] [pid 21434] AH00111: Config variable ${APACHE_RUN_GROUP} is not defined
[Wed Jan 03 15:28:39.278587 2018] [core:warn] [pid 21434] AH00111: Config variable ${APACHE_LOG_DIR} is not defined
AH00526: Syntax error on line 74 of /etc/apache2/apache2.conf:
Invalid Mutex directory in argument file:${APACHE_LOCK_DIR}

缺少环境变量，按照如下步骤操作即可:
```bash
source /etc/apache2/envvars 
apache2 -V
sudo service apache2 start
// 或
sudo apache2 -k start
```

## qixiao rewrite配置
```
<VirtualHost *:80>
	ServerName qixiao.local.com
	DocumentRoot C:\wamp64\www\qixiao
	<Directory  "C:\wamp64\www\qixiao">
		Options +Indexes +Includes +FollowSymLinks +MultiViews
		AllowOverride All
		Require all granted
		
		RewriteEngine on
		RewriteCond %{REQUEST_FILENAME} !-d
		RewriteCond %{REQUEST_FILENAME} !-f
		RewriteRule ^(.*)$ index.php/?$1 [QSA,PT,L]
	</Directory>
</VirtualHost>
```