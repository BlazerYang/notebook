# NodeJS产品最佳实践
>译者注：  
This article is translated from "[https://www.joyent.com/node-js/production/design](https://www.joyent.com/node-js/production/design)" by [Joyent](www.joyent.com)(All rights reserved)  
原文链接"[https://www.joyent.com/node-js/production/design](https://www.joyent.com/node-js/production/design)", 作者[Joyent](www.joyent.com)(版权所有)

## 设计
Node.js就是javascript，所以你所了解的JavaScript知识都可以应用到Node.js应用中。你在前端中编写代码的模式在编写服务器端应用逻辑时同样适用。Node.js没有使用JavaScript语法扩展或者任何修改以适应JavaScript服务端的开发。

但是，Node.js中仍然有一些模式能够帮助你设计应用。

## 事件发射器模式
下面讲到第一个模式是事件发射器模式，该模式可以让实现者发射事件，然后让消费者订阅其感兴趣的事件。你可以把其当做传递回调给异步函数并在完成时执行回调模式的一种扩展。通常情况下基于回调的异步方案是不够充分的，因为可能存在不只一个调用者对该事件感兴趣。

比如，一个调用者可能会请求一个远程服务器的“文件列表”。你或许想要在每检测到一个文件时就将结果传递回去，即对每个文件都调用一遍回调函数。事件发射器模式允许你每检测到一个文件就发射一个'file'事件，然后在操作结束后发射'end'事件。

使用事件发射器时，你只需要发射事件及其对应负载即可

```javascript
const EventEmitter = require('events').EventEmitter;

class MyClass extends EventEmitter {
  constructor() {
    super();

    setTimeout(() => {
      this.emit('myEvent', 'hello world', 42);
    }, 1000);
  }
}
```
MyClass的构造器创建了一个1秒后执行的定时器，当定时器触发时会发射一个带有字符串'hello world'和数字42的事件myEvent。你可以使用on()来订阅该事件，on方法会通过继承EventEmitter附加在MyClass上：

```javascript
const myObj = new MyClass();
const start = Date.now();
myObj.on('myEvent', (str, num) => {
  console.log('myEvent triggered', str, num, Date.now() - start);
});
```
你需要注意到，你所订阅的事件是异步事件，但是监听函数是在事件触发时是同步执行的。所以如果myEvent有10个订阅，那么这10个订阅会立即顺序执行，而不会等到下一个事件循环。记住这个同步特性，对事件发射者来说，延迟发射事件就显得非常重要，这样订阅者就可以在同一个事件循环中订阅多个事件，而且不会错过在未来某个时间发射的事件。

如果EventEmitter子类发射了'error'时间，且无人订阅该事件，那么EventEmitter会抛出一个异常，进而导致process对象触发uncaughtException事件

### verror
>verror组件是Error的子类，允许你通过使用printf的形式自定义错误信息。你的应用逻辑通常是异步方法的组合，在添加错误处理函数时，你经常会想要将错误信息冒泡至上级。verror组件包含两个类-VError和WError，允许你将调用链上的错误累计起来。可以看到合并的错误信息（VError，unix风格）或者最终的错误信息，但是可以访问上一级的错误信息（WError）  
[joyent/node-verror](https://github.com/joyent/node-verror)

## 流模式
流是另一个在Node.js中广泛应用的基础模式。除了大量实现事件发射器模式的核心模块之外，还有模块很多实现了诸如Readable, Writable或者兼有(Duplex)的接口。

流是一个抽象接口，提供了常用事件比如readable、writable、drain、data、end和close。这些事件本身就具有高互动性，但是流最强大的部分是允许你将不同的流整合到一个管道（pipeline）中。

管道可以帮助你的代码降低复杂性、易于理解并提高可读性。你可以通过使用.pipe()模式启动Node.js通过管道来传递反压（back-pressure）。这个反压意思是你只能读取你可以写的或者你只能写你可以读的东西。因此，在一定时间内，你只能在内存中保持你能够完成的数量的工作。

假设你想要将stdin的数据发送至本地文件和远程服务器

```javascript
const fs = require('fs');
const net = require('net');

const localFile = fs.createWriteStream('localFile.tmp');

const client = net.connect(80, '98.139.183.24', () => {
  process.stdin.pipe(client);
  process.stdin.pipe(localFile);
});
```
client和localFile都会从stdin读取数据，但是读取速度由最慢的消费者决定。

pipe()返回的是目标流，所以如果目标是一个Duplex，或者是一个特殊的Duplex，比如Transform，那么你就可以使用链式调用管道。

继续上一个例子，这次我们只能将内容发送至本地文件，而且在保存前对内容使用gunzip进行压缩

```javascript
const fs = require('fs');
const zlib = require('zlib');
process.stdin.pipe(zlib.createGunzip()).pipe(fs.createWriteStream('localFile.tar'));
```
更多关于流的信息，可以参考最新版Node.js的文档

## 控制流程
因为JavaScript中函数是头等对象和还有闭包的概念，所以很容易在需要的地方定义回调函数。这在对解决方案进行快速原型时会很方便，因为你可以直接在你需要的地方实现你的逻辑。但是，这样的话会导致一堆臃肿的内嵌函数，又称为圣诞树或者毁灭金字塔。

比如你想要顺序读取一系列文件，然后在这些文件内容上做一些通用操作：

```javascript
fs.readFile('firstFile', 'utf8', (err, firstFile) => {
  doSomething(firstFile);
  fs.readFile('secondFile', 'utf8', (err, secondFile) => {
    doSomething(secondFile);
    fs.readFile('thirdFile', 'utf8', (err, thirdFile) => {
      doSomething(thirdFile);
    });
  });
});
```
现在看起来还不算太糟，但是这个模式有一些缺点：

* 如果这些代码的逻辑太复杂的话，那么理解程序流向和操作顺序就会变得非常困难。
* 没有错误处理逻辑，在第三层代码执行时，已经忽略了可能出现的两次错误。
* 第一个文件读取的结果在第三个操作完成之前一直是GC不可回收的状态。闭包内存泄露在JS应用中非常常见，而且多数都很难被诊断和发现。
* 如果你需要在一个输入集上做一系列异步操作的话，最好找一个控制流程函数库来帮助你简化流程。我们使用vasync，因为它还让调试器探查管道变得容易。

### vasync
>vasync是一个控制流程函数库，受异步组件模式的启发而成。然而vasync设计目的是使消费者可以查看指定任务的执行进度。在获取这些任务在错误发生前执行了多久时，这些信息非常重要。

## 代码风格

### 为你的函数命名
>考虑给所有的函数命名，即使是那些你想不到的小闭包。尽管V8使出浑身解数去通过脚本名和错误来源中的函数位置去识别函数，想要一眼区分这些函数还是非常困难。你不会想要在调试的时候浪费时间去修正这个错误的函数。

### 避免使用闭包
>同样地，尽量不要在其他函数内部定义函数。这会将你的思维方式由基于闭包变为基于栈。这个逻辑上小小的改变可以帮助消除许多由于使用闭包无意引入的内存泄露。

### 更多更小的函数
>尽管V8 JIT是一个强大引擎，可以进行许多代码优化，但如果你的函数越小、定义越清晰，那么JIT就越有可能内联缓存这些函数。从好的方面说，如果你的函数都很小（代码不超过100行），那么你的代码可读性和易理解性都有可能得到提升，同时也降低了应用的维护成本。

### 启用代码风格检查
>使用一致的代码风格，安装一个检查工具并启用它。我们使用的是jsstyle，对js来说是一个不常见的风格提示工具，但是至少有一个了。另一个流行的提示工具是eslint。风格检查工具的错误看起来就像是字符错误或者单元测试失败一样：构建失败需要立即修复

### 易于测试
>保证所有的关键函数都是可以在外部执行的。简单地说，就是这些函数可以用export导出或者可以通过class的方法访问。按照这个方式，保证这些函数被测试用例覆盖，通过运行代码覆盖率报告者，比如lab

## 代码提示
代码提示工具可以对代码进行静态分析（无需运行）以识别出潜在的bug或者危险代码，比如使用了未声明的变量或者switch中的case没有写break。好点的代码提示工具应该略微激进一些（比如，有的时候就是需要case中没有break），而你可以通过单行操作来忽略提示。这些操作不应该被用来仅仅是无视提示工具，而是因为代码这样书写比按照提示的书写更加清晰。通过忽略避免了某些让人困惑的代码。

如果你要使用代码提示，那么就请严肃对待这件事。将提示检查作为构筑的一部分，就像单元测试一样，并且拒绝掉没有通过所有见的代码。（记住，你可以按照需要忽略若干单一的提示，但这么做的目的是因为写代码的人已经看到了这个提示并且做出了正确的决定）

代码提示同风格检查不是一个东西。风格检查同样有用（见上），但是代码提示通常是指客观上存在危险的模式，而不是随意的风格选择。（必须承认，这里存在有中间地带，比如有的时候使用"=="而不是"==="是ok的）

有很多不同的代码提示工具。按需取。我们使用javascriptlint因为它有很多好的检查策略、支持基于项目的配置（每个项目可以设置不同的检查策略），同时支持对单个提示点的忽略（以便于编写者手动指定忽略哪些校验点）

同样地，强烈推荐在代码中使用'use strict'开始严格模式，这样可以帮助你的代码在js解析器识别出全局泄露或者其他相似行为时尽快失效。

## 日志
当设计和构建你的应用时，确定未来的计划。特别是考虑到你在调试时需要的工具。一个优秀且明显的措施就是给你的应用添加合适的日志记录。确保你选择了一个日志函数库能够支持你需要的特性。一些常见的考虑：是否支持你关注的需求？是否是你想要的格式？记录日志的API不会同Node.js和你的应用风格差异过大等。

在应用运行时识别出对调试和分析应用有用的信息非常重要。但是要记住，在日志中包含过量的信息会对性能和存储产生不良影响。确认你只在必要的地方包含必要的信息，以免拖慢应用的速度。bunyan有一个很不错的功能是可以按照需要在生产环境读取debug级别的日志，而不需启用也无需重启进程。

### bunyan
>bunyan是一款专为Node.js应用设计的日志函数库。Bunyan的输出是按行分隔的JSON数据，非常易于在unix的命令行函数处理，比如grep和sed，同样在你自己的CLI函数或者json CLI函数也适用。
>
>bunyan内置支持DTrace，其允许你为现有目标保留现有日志级别（e.g. INFO）,但是可以在运行时启用更详细的级别（e.g. Trace），结果会记录至这些日志文件所在的用户空间中，即使文件不存在也会输出至已有的文件中，存在填满硬盘的可能。DTrace用在运行时是绝对安全的，所以如果启用高级别的日志记录会对你的系统造成负面影响时，DTrace会在影响发生之前退出。
>
>也就是说，你已经在你的应用中配置好想要记录的日志等级，但是你的应用运行不正常，而且你想要在不重新启动服务或者增加日志存储量的情况下获取更多信息。依靠bunyan和DTrace即可在运行时从进程中获取你感兴趣的等级的日志。
>
> ```bash
> # bunyan -p *
> [2013-09-27T18:16:19.679Z] DEBUG: test/1076 on sharptooth.local: something went wrong
> ```
>Read more about using bunyan to do runtime log snooping.

## 客户端 服务端
在扩展至分布式系统时，使用这种方式设计你的应用会有很大优势。使用REST比如HTTP上的API或者甚至是TCP上的JSON来描述这一类接口都很自然。这种方式使得一个人可以将Node擅长的异步网络环境和流的使用整合至强大的分布式和弹性系统。

## 具体软件
### bunyan
详情见上

### fast
>fast是一个用于在TCP中高效处理JSON消息的轻量级函数库。基础用法是为了实现基于消息的RPC，即使用指定的指令后将一系列相关的对象被发送至客户端。fast设计时兼顾了可观测性，故其同样支持DTrace，允许你快速获取服务端和客户端的性能数据

### restify
>restify是一个用于创建和消费REST的终端。转为了增加应用的可观性和易调试性而设计，restify对Bunyan支持Bunyan和DTrace。有了Bunyan和DTrace的支持，你就获取了查看日志或运行时路由和请求延迟的能力。

### vasync
详情见上