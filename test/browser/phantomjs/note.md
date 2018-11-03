# note

## phantomjs可以执行html中内联的script，但是不会执行外联script，如何解决？
将外联的js通过page.injectJs()方法注入，就可以执行。  
但是在onResourceRequested事件中注入却不可以（只会返回false）

## script中的异步事件回调不会执行？
确实不会执行，感觉像是phantomjs的bug

##