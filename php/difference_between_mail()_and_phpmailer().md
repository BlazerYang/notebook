# DIFFERENCE BETWEEN mail() and PHPMailer

1. mail()是最基础的邮件发送服务，其利用本机作为邮件服务器发送邮件，如果需要发送一个复杂的邮件则需要额外处理很多的东西，比如头信息、附件等。
   而如果使用PHPMailer的话，其会将很多繁杂的操作进行封装，降低用户的使用难度
2. mail使用php.ini中sendmail配置指定的程序来发送邮件，而phpmailer配置了SMTP之后直接向SMTP服务器投递邮件

## 为什么test使用mail()可以发送邮件，而prod不可以
prod环境`ps -ef | grep postfix`找不到对应的进程，但是test环境可以

## prod和test环境均为docker环境，使用k8s调度，每个pod中均有frontend和backend镜像
为什么prod中的理应存在于backend的postfix进程却存在于frontend中，导致backend中的php调用mail发送邮件时失败，邮件堆积在邮件队列中
* 排查后发现，因为当前pod中存在两个容器，两个容器的启动命令中均执行了`service postfix start`导致其进程在应该出现的容器中查不到，而php的`mail()``函数是直接调用的postfix进程发送的邮件，所以会出现找不到进程，然后邮件发送失败的情况。而是用PHPMAILER的api的话，走的是SMTP的端口来发送邮件，所以不会有问题