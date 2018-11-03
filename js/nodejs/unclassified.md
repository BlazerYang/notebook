# 未分类问题

## node中执行process.exit(0)时，不会等待callback执行完毕
不用手动执行process.exit(0), node在所有工作完成后会自动退出，记得自己关闭connection  
有两种关闭方式
```javascript
// 在所有请求完成后发送COM_QUIT包给mysql，如果在COM_QUIT发送前出现FATAL ERROR，则会将错误信息传送到err中，然后仍会退出
connection.end((err) => {})

// 强制退出，直接执行退出操作。无须参数
connection.destroy()
```

## process.exit(0)时，readline对象会发射end事件吗？
经测试不会发送
### expample: 
[eventEmitAfterProcessExit](./examples/eventEmitAfterProcessExit/index.js)

## fs.appendFile()
如果文件不存在，会创建；如果路径不存在，则不会创建

## node如何升级？
```js
node cache clean -f
node install -g n
n stable // 自动安装到最新的稳定版
```

## 如何使用服务端发送邮件服务？
1. 使用公共邮箱的smtp的方式
```js
npm install --save node-mailer
// 指定smtp服务器、用户名和授权码即可使用
```
2. 使用本地邮件服务器的方式
```js
npm install --save sendmail
// 该组件依赖sendmail服务（linux）下原装，window下有fake版
// 直接指定from、to就可以用了
```

## 如何压缩图片？
可以用node-smushit

## 如何将dataurl保存为图片
删除开头的meta信息后写入文件即可, 注意需要指定编码格式
```js
const fs = require('fs')
let data = dataUrl.replace(/^data:image\/jpeg;base64,/, '')
fs.writeFile(filename, data, 'base64', (err)=>{console.log(err)})
```

## what is JIT?
Just-In-Time compiler， 也就是即时编译编译器，目的是为了提高程序性能
具体工作原理请参考：[JavaScript Just-in-time (JIT) 工作原理](https://zhuanlan.zhihu.com/p/25669120)

## what is socket hang up ?
Node.js中如何你的http的res在返回数据之前就end掉了，那么node.js就会抛出一个socket hang up error

## node中如何使用dom selector？
静态网页需要用解析工具
动态网页需要headless的浏览器

## 打包下载的安装包放在linux中无法直接执行？
将node目录放在环境变量中
```bash
export $PATH=$PATH;/home/username/node/bin/
```