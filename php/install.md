# php installation

原版：
```bash
./configure     --prefix=/usr/local/php7     --with-config-file-path=/usr/local/php7/etc     --with-config-file-scan-dir=/usr/local/php7/etc/php.d/     --disable-ipv6      --enable-fpm     --with-fpm-user=nginx      --with-fpm-group=nginx     --enable-inline-optimization     --disable-debug     --disable-rpath     --enable-shared      --enable-soap     --with-libxml-dir     --with-xmlrpc     --with-openssl     --with-mcrypt     --with-mhash     --with-pcre-regex     --with-sqlite3     --with-zlib     --enable-bcmath     --with-iconv     --with-bz2     --enable-calendar     --with-curl     --with-cdb     --enable-dom     --enable-exif     --enable-fileinfo     --enable-filter     --with-pcre-dir     --enable-ftp     --with-gd     --with-openssl-dir     --with-jpeg-dir     --with-png-dir     --with-zlib-dir      --with-freetype-dir     --enable-gd-native-ttf     --enable-gd-jis-conv     --with-gettext     --with-gmp     --with-mhash     --enable-json     --enable-mbstring     --enable-mbregex     --enable-mbregex-backtrack     --with-libmbfl     --with-onig     --enable-pdo     --with-mysqli=mysqlnd     --with-pdo-mysql=mysqlnd     --with-zlib-dir     --with-pdo-sqlite     --with-readline     --enable-session     --enable-shmop     --enable-simplexml     --enable-sockets      --enable-sysvmsg     --enable-sysvsem     --enable-sysvshm     --enable-wddx     --with-libxml-dir     --with-xsl     --enable-zip     --enable-mysqlnd-compression-support     --with-pear     --enable-opcache    --enable-pcntl
```
出现的问题：
1. 出现yum源中某些依赖版本太低，只能手动安装最新依赖
2. 所有依赖的库均需安装对应devel版本才可编译安装
调整后：
```
 ./configure     --prefix=/usr/local/php7     --with-config-file-path=/usr/local/php7/etc     --with-config-file-scan-dir=/usr/local/php7/etc/php.d/     --disable-ipv6      --enable-fpm     --with-fpm-user=root      --with-fpm-group=root     --enable-inline-optimization     --disable-debug     --disable-rpath     --enable-shared      --enable-soap     --with-libxml-dir     --with-xmlrpc     --with-openssl     --with-mcrypt     --with-mhash     --with-pcre-regex     --with-sqlite3     --with-zlib     --enable-bcmath     --with-iconv     --with-bz2     --enable-calendar     --with-curl     --with-cdb     --enable-dom     --enable-exif     --enable-fileinfo     --enable-filter     --with-pcre-dir     --enable-ftp    --with-gd=/usr/local/gd      --with-openssl-dir     --with-jpeg-dir     --with-png-dir     --with-zlib-dir      --with-freetype-dir    --enable-gd-native-ttf     --enable-gd-jis-conv    --with-gettext          --with-mhash     --enable-json     --enable-mbstring     --enable-mbregex     --enable-mbregex-backtrack     --with-libmbfl     --with-onig     --enable-pdo     --with-mysqli=mysqlnd     --with-pdo-mysql=mysqlnd     --with-zlib-dir     --with-pdo-sqlite     --with-readline     --enable-session     --enable-shmop     --enable-simplexml     --enable-sockets      --enable-sysvmsg     --enable-sysvsem     --enable-sysvshm     --enable-wddx     --with-libxml-dir     --with-xsl     --enable-zip     --enable-mysqlnd-compression-support     --with-pear     --enable-opcache  --with-gmp=/usr/local/gmp --with-xpm-dir=/usr/lib64
 ```

## 比起configure之后发现缺少依赖再一个一个去装，可以先提前装好所有的开发包依赖
```
yum groupinstall -y "Development tools" "Server Platform Development"
```

## 如何查找对应的依赖全名
```
yum list all | grep -i NAME
```

## 完成安装之后添加环境变量
```
ln -s /usr/local/php7/bin/php /usr/local/bin/php7
ln -s /usr/local/php7/bin/phpize /usr/local/bin/phpize7
```