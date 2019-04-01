# unclassified

## @is_dir()前导@的作用？
用在函数前用于忽略报错，但是并未解决报错

## public function &get_instance() 函数前的&？
php的引用，不同的变量名可以访问同一个变量内容；用在函数前意为返回变量的引用

## php上传文件中文名是乱码？
错误发生在copy()或move_uploaded_file()函数中，因为系统默认字体为gb2312，而php设置为UTF-8，因此在新建文件时会出现文件名乱码
解决方案，在写入时，将路径名称使用iconv转换编码格式
```php
copy($file, iconv('UTF-8', 'GB2312', $filePath));
```
参考[iconv用法](http://php.net/manual/zh/book.iconv.php)

## how to restart php-fpm in linux?
`service php-fpm restart`

## 查看CPU位数？
getconf LONG_BIT

## 上传大文件？
修改`upload_max_filesize`  
同时此值同时受限于`post_max_size`, 此值应大于`upload_max_filesize`
可能会受影响的变量`max_input_time`, `max_execution_time`

## 大文件读取，报内存耗尽？
可用内存上限定义在`memory_limit`中

## php 返回500错误，如何查看错误信息？
1. `ps -ef | grep fpm`找到配置文件位置
2. 修改以下配置文件信息
```ini
error_log = /data/php/log/php-fpm.log
log_level = notice
```
3. 重启fpm后即可： `service php-fpm restart`inii

## php如何在ajax返回结果之后执行执行剩余的脚本呢？
参考Stack Overflow的方案：[continue processing php after sending http response
](https://stackoverflow.com/questions/15273570/continue-processing-php-after-sending-http-response)
```php
if (is_callable('fastcgi_finish_request')) {
  // This works in Nginx but the next approach not
  session_write_close();
  fastcgi_finish_request();
  return;
}
ignore_user_abort(true); // 是否在输出流结束后停止脚本执行，设为true就可以继续执行
set_time_limit(0); // 设置允许脚本的超时时间，0为不限制，单位为s，可酌情设置

ob_start(); // 打开输出控制缓冲
// do initial processing here
echo $response; // send the response
header('Connection: close'); // 用于关闭keep-alive的连接
header('Content-Length: '.ob_get_length()); // 缓冲区内容的长度
session_write_close(); // 单进程并发下防止拖慢后续进程
ob_end_flush(); // 冲刷出（送出）输出缓冲区内容并关闭缓冲
ob_flush(); // 冲刷出（送出）输出缓冲区中的内容
flush(); // 刷新输出缓冲
```

### fastcgi_finish_request()
该函数仅在FastCGI模式下可用，对应的就是php-fpm(FastCGI Processes Manager)
[http://php.net/manual/zh/function.fastcgi-finish-request.php](http://php.net/manual/zh/function.fastcgi-finish-request.php)

### session_write_close()
写入session，关闭session，并释放session锁。必须在后续的耗时操作之前调用，不然后续使用到该session的进程会阻塞直到锁释放

### 采用该方案后apache+php的webserver的后续第一个请求会变慢，原因？
因为session锁的原因，第一次脚本执行时session锁没有释放，后续请求在session_start()时会阻塞直到上一次请求的脚本完全执行结束(此时释放session锁)
解决方法就是在ob_end_flush之前调用session_write_close()关闭链接

## 如何查看apache + php采用的并发模型？
目前推测wampserver的apache+php采用单线程单进程处理并发

## php如何获取上传文件？
表单中的文件名为file，则中`$_FILES["file"]['name']`存储的是文件上传的名称，`$_FILES['file']['tmp_name']`中存储的是文件在服务器的临时文件名，
可以用`move_uploaded_file($_FILES['file']['tmp_name'], "/uploads/" . $_FILES["file"]['name'])`移动文件到指定的路径下

## php如何获取客户端ip？
具体参考这里[https://blog.csdn.net/zhezhebie/article/details/74910964](https://blog.csdn.net/zhezhebie/article/details/74910964)
```php
// 1. 没有使用代理
$_SERVER['REMOTE_ADDR'] // client ip
$_SERVER['HTTP_VIA'] // none
$_SERVER['HTTP_X_FORWARDED_FOR'] // none

// 2. 使用透明代理服务器(transparent proxy)
$_SERVER['REMOTE_ADDR'] // most recent proxy ip
$_SERVER['HTTP_VIA'] // passed proxy ip
$_SERVER['HTTP_X_FORWARDED_FOR'] // client ip + passed proxy ip

// 3. 使用匿名代理服务器(anonymous proxy)
$_SERVER['REMOTE_ADDR'] // most recent proxy ip
$_SERVER['HTTP_VIA'] // passed proxy ip
$_SERVER['HTTP_X_FORWARDED_FOR'] // passed proxy ip

// 4. 使用欺骗性代理服务器(distorting  proxy)
$_SERVER['REMOTE_ADDR'] // most recent proxy ip
$_SERVER['HTTP_VIA'] // passed proxy ip
$_SERVER['HTTP_X_FORWARDED_FOR'] // random fake ip + passed proxy ip

// 5. 使用高匿名代理服务器(high anonymity proxy)
$_SERVER['REMOTE_ADDR'] // most recent proxy ip
$_SERVER['HTTP_VIA'] // none
$_SERVER['HTTP_X_FORWARDED_FOR'] // none
```

### HTTP_X_FORWARDED_FOR
如果请求经过代理，那么这里记录的是客户端的真实IP，如果经过两个及以上的代理服务器，那么后续会依次跟上经过的代理ip 
如果从客户端到服务器依次为： 10.18.173.161(client) => 10.18.12.14(proxy 1) => 10.173.180.142(proxy 2) => 10.18.173.161(server)
```
// 这里是头信息，与PHP内置名相比少了HTTP-前缀
X_FORWARDED_FOR: 10.18.173.161, 10.18.12.14, 10.173.180.142
```

### HTTP_VIA
其中会依次记录经过的代理服务器名称(或者ip[:port])。具体参考MDN的说明文档
[https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Via](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Via)
如果从客户端到服务器依次为： 10.18.173.161(client) => 10.18.12.14(proxy 1) => 10.173.180.142(proxy 2) => 10.18.173.161(server)
```
VIA: 10.18.12.14, 10.173.180.142
```

### 为什么PSR中函数的命名推荐使用小写字母和下划线的方式？

### 什么是语言变量？


## fpm平滑重启
`kill -USR2 $(ps -aux | grep php-fpm|awk '{print $1}")`
其中：
* `USR2` 平滑重载所有worker进程并重新载入配置和二进制模块
* 平滑重启： 旧进程在处理完当前请求后依次退出，并生成新的进程开始处理请求，对于无状态的服务来说，用户是无感知的


## 为什么有时候从数据库里取出来的数据使用basename后结果不符合预期？
```php
$path = 'attachment/2018/12/20/20/27/05/商业化会议纪要汇总_5c1b6ef468525.zip';
$filename = basename($path);

// 预期: 商业化会议纪要汇总_5c1b6ef468525.zip
// 实际: _5c1b6ef468525.zip
var_dump($filename);
```

## 中文json_encode时被转为unicode码
使用json_encode('中文',JSON_UNESCAPED_UNICODE)