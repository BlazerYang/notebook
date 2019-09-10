# jenkins

## Error 403 No valid crumb was included in the request?
[调用Jenkins API](https://segmentfault.com/a/1190000010738617)

## doDelete提示403
api删除任务是返回结果状态码为403，返回内容如下
```html
<html><head><meta http-equiv=\'refresh\' content=\'1;url=/login?from=%2F\'/><script>window.location.replace(\'/login?from=%2F\');</script></head><body style=\'background-color:white; color:white;\'>


Authentication required
<!--
You are authenticated as: anonymous
Groups that you are in:
  
Permission you need to have (but didn\'t): hudson.model.Hudson.Read
 ... which is implied by: hudson.security.Permission.GenericRead
 ... which is implied by: hudson.model.Hudson.Administer
-->

</body></html>
```
原因是，删除成功之后，api会返回一个302跳转至jenkins页面，但是因为当前session中并没有登陆信息，且匿名用户没有配置项目读权限，所以才提示403

解决方案：
在 jenkins -> 系统管理 -> 全局安全配置 -> 安全矩阵 中授予匿名用户读权限，则jenkins可以正确跳转至首页而不提示403

## html report无法加载css/js
在 系统管理 -> 脚本命令行 中输入并执行如下语句，关闭CSP
```groovy
System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")
```
注意：该设置重启后会失效


## workspace和jobs分别是做什么用的？
workspace是jenkins任务运行的工作目录，一切插件、脚本中的相对目录均以此为根目录
jobs存储的是jenkins任务每次运行的结果