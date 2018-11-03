# Design
[原文链接](https://www.joyent.com/node-js/production/design#EventEmitter)
## Design
Node.js is JavaScript, so everything you already know about JavaScript applies to your Node.js application as well. The patterns you use to write your front-end client code work when writing your server-side application logic. Node.js does not use any JavaScript language extensions or modifications to accomplish its goal of server-side JavaScript.

There are, however, patterns used throughout Node.js that are helpful to know and can be useful while designing your application.

## EventEmitter
The first pattern to be aware of is the EventEmitter pattern, which allows implementors to emit an event and consumers to subscribe to the events they are interested in. You can think of this as an extension to the pattern of passing a callback to an asynchronous function that the function invokes upon completion. EventEmitters are useful when one callback isn't enough, usually, because there's more than one event that might be interesting to the caller.

For example, a caller might make a request to "list files" on a remote server. You may want to stream results back as they come, invoking a callback for each one. The EventEmitter pattern lets you emit "file" on each one and "end" when the whole operation is done.

When implementing an EventEmitter, you simply need to emit the event and the arguments associated with that event.

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
The constructor for MyClass creates a timer that will fire in 1 second, when that timer fires it emits the event myEvent with the string 'hello world' and the number 42. To consume that event you need to use the on() method which was added to the prototype of your class when you inherited it from EventEmitter:

```javascript
const myObj = new MyClass();
const start = Date.now();
myObj.on('myEvent', (str, num) => {
  console.log('myEvent triggered', str, num, Date.now() - start);
});
```
It's important to note that you subscribe EventEmitter events to be notified of asynchronous events, but the execution of the listeners themselves is synchronous when that event happens. So if the myEvent event has 10 listeners subscribed, all 10 listeners will be called sequentially without deferring to the event loop. With that synchronicity in mind, it's important for event emitters to defer emission of events so that consumers can subscribe to multiple events in the same turn of the event loop and have confidence that the callback will be fired sometime in the future.

If a descendant of EventEmitter has cause to emit('error') and there are no listeners subscribed to that event, the EventEmitter base class will throw an exception, which will lead to the uncaughtException event firing on the process object.

### verror
>verror extends the base Error class, and allows you to define your messages using printf string formatting. The logic for your application is often a composition of asynchronous methods, and when adding error handling you may want to bubble that information up through your system. verror has VError and WError which allow you to accumulate multiple levels of errors through a chain, and either see the combination of errors in the message (as in VError) or have a final message in WError but programmatically be able to access the previous errors in the chain.

## Streams
Streams are another base pattern used extensively throughout Node.js. Along with most core pieces implementing the EventEmitter pattern, many will implement the Readable, Writable, or both (Duplex) interfaces.

Streams are an abstract interface that provides common events like readable, writable, drain, data, end, and close. These events in and of themselves are powerful to interact with, but the most powerful part of the streams interface is your ability to compose a series of streams into a pipeline.

A pipeline is helpful to simplify the complexity, understandability, and readability of your code. By using the .pipe() pattern you allow Node.js to communicate back-pressure through the pipeline. This back-pressure means that you're only attempting to read what you're able to write or write what you're able to read. Therefore, you're only keeping the amount of work you can accomplish in memory at a given time.

Consider if you want to send data coming in from stdin to both a local file and to a remote server.

```javascript
const fs = require('fs');
const net = require('net');

const localFile = fs.createWriteStream('localFile.tmp');

const client = net.connect(80, '98.139.183.24', () => {
  process.stdin.pipe(client);
  process.stdin.pipe(localFile);
});
```
Both client and localFile will read from stdin but the data will only write as fast as the slowest reader can consume.

pipe() always returns the destination stream. So if the destination is a Duplex, or if it is a special case of Duplex known as a Transform you can chain the pipeline together.

Consider the previous example, but this time we only want to send to a local file and want to gunzip the stream before it's written to disk.

```javascript
const fs = require('fs');
const zlib = require('zlib');
process.stdin.pipe(zlib.createGunzip()).pipe(fs.createWriteStream('localFile.tar'));
```
You can learn more about streams in the latest versions of Node.js in this talk.

## Control Flow
Since JavaScript has the concept of functions as first class objects and closures, it's easy to define the callback right where it is needed. This is convenient when prototyping your solution, as it allows you to consolidate the logic right where it's needed. However, it can quickly lead to unwieldy sets of embedded functions, sometimes referred to as the Christmas tree or pyramid of doom.

Consider that you want to read a series of files in succession, and perform a common task on the results of those tasks:

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
This doesn't appear to be too bad, but there are several downsides to the pattern:

If the logic around any of these pieces gets too complex, it can be difficult to understand the flow and order of operations.  
There's no error handling being done here, and by the time we're on the third level we've shadowed the first operation's error twice.
The result from reading the first file will stay active in the eyes of the GC until the third operation completes. Closure memory leaks are very common in JavaScript applications, and often the most difficult to diagnose and detect.
If you need to do a series of asynchronous operations on a set of input, it's good to find a control flow library that simplifies the process for you. We use vasync because it also makes it easy to inspect a pipeline from a debugger.

### vasync
>vasync is a control flow library, inspired by the patterns found in the async module. However vasync is designed specifically to enable a consumer to have visibility and observability into their progress for a given task. Such information is crucial when trying to determine how far along a task was before an error occurred.

## Coding Style
Coding style is notoriously contentious because much of it is arbitrary. It's important to follow a style that is comfortable for you and your team. That being said, there are some conventions that can be used to make your life developing with Node.js easier.

### Name your functions
>Consider naming all functions, even small closures you wouldn't think to, merit a name. While V8 will try its best to identify by script name and function location the source of an error, it can be difficult to differentiate functions at a glance that way. The last thing you want to do when debugging is to waste time fixing the wrong function.

### Avoid closures
>Similarly, consider moving function definitions outside of other functions. This changes your thinking from closure-based to stack-based. This small switch in logic can help eliminate many unintended memory leaks that closures can bring with them.

### More and smaller functions
>The V8 JIT is a powerful engine and can optimize a lot of patterns, but the smaller and more concise you are with your functions the more likely the JIT will be able to inline those functions. On the upside, if your function is small (no more than a 100 or so lines of code for instance) it's likely to increase the readability and understandability of your codebase, which should decrease the amount of effort spent trying to maintain your application.

### Check style programmatically
>Use a consistent style, and have a checking tool that enforces it. We use jsstyle, which is a somewhat unusual style for JavaScript, but at least the tool enforces it. Another popular linting tool is eslint. Errors from the style checker are just like syntax errors or unit test failures: the build is considered broken and must be fixed immediately.

### Design for testability
>Make sure that any critical functions are available to be externally executed. Simply put, this usually means that they are exported or are accessible on a class that is exported. Along these lines, ensure that these functions are covered by tests by running a code coverage reporter like lab.

## Linting
Lint tools analyze your code statically (without running it) to identify potential bugs or dangerous patterns, like the use of undeclared variables or "case" statements inside a switch without a "break" statement. Good linters can be a little aggressive (e.g., sometimes it's desirable to have a "case" statement without a "break"), but you can override them on a per-line basis. Such overrides should not be used just to silence the linter, but rather because the code as written is much clearer than rewriting it to avoid the warning. The override also clarifies the potentially confusing code for readers.

If you lint your code, be serious about it. Run lint checks as part of the build, alongside unit tests, and reject code that doesn't pass all checks. (Remember, you can override individual checks as needed, but the point is that doing so makes it clear that the programmer has seen that check and decided the code is correct.)

Lint is not the same thing as style checking. Style checking is useful too (see above), but linting generally refers to objectively dangerous patterns, rather than arbitrary style choices. (Admittedly, there's a gray area between these, as when considering whether it's okay to use "==" instead of "===" in some cases.)

There are many different linters. Find one that fits your needs. We use javascriptlint because it has a good number of checks and it's configurable both on a by-project basis (each project can specify which checks it wants to enforce) as well as on a by-line basis (so that a programmer can indicate when a check is being explicitly bypassed).

Also, strongly consider enabling strict mode on your codebase with 'use strict';, as this can help your code fail fast if the JavaScript parser can identify a leaked global or similar bad behavior.

## Logging
While designing and building your application, be sure to plan for the future. Especially consider the tools you will need when it comes to debugging. An excellent and obvious first step is to add appropriate amounts of logging to your application. Make sure you pick a logging library that supports the feature sets you need. Some considerations are: does it support the destinations you care about, the output format you prefer, and is the API what you expect from logging while at the same time not feeling foreign to Node.js and your codebase.

It's important to identify the information that will be critical for debugging and analyzing your application while it's running. But be mindful, including excess information in your logs may have a detrimental effect on performance or storage. Be sure you include the useful information, and in the appropriate places, while not also slowing your application down for unnecessary information. One nice feature of bunyan is that you can read debug-level logs on-demand in production, without actually enabling them there and without restarting the process.

### bunyan
>Bunyan is a straightforward logging library for Node.js applications. Bunyan's output is line delimited JSON, which makes it easy to consume with your normal unix command line utilities like grep and sed, and also with its own CLI utility, or with the json cli utility.
>
>Bunyan also comes with built-in support for DTrace, which allows you to keep your existing log level for your existing destinations (e.g. INFO) but enable at runtime a more verbose level (e.g. TRACE) and be notified in user space of those log entries, without them also going to your existing destinations and potentially filling the disks. DTrace is completely safe to use at runtime, so if enabling higher levels of logging would result in detrimental effect your system DTrace will exit before doing your system harm.
>
>That is, you've already defined in your configuration the level at which you want your application to log, but your process is currently misbheaving and you're looking to find out more information without potentially restarting the service or increasing the amount of storage where your logs are stored. With bunyan and DTrace you can enable your process to send to you the log level you're interested in at runtime.
>
> ```bash
> # bunyan -p *
> [2013-09-27T18:16:19.679Z] DEBUG: test/1076 on sharptooth.local: something went wrong
> ```
>Read more about using bunyan to do runtime log snooping.

## Client Server
It can be advantageous to design your application in such a way that allows you to build distributed systems. It's quite natural to describe this sort of interface with a REST like API over HTTP, or even with raw JSON over TCP. This allows one to combine Node's expertise in asynchronous network environments, and the use of streams into a powerful distributed and scalable system.

## Specific Software
### bunyan
>Bunyan is a straightforward logging library for Node.js applications. Bunyan's output is line delimited JSON, which makes it easy to consume with your normal unix command line utilities like grep and sed, and also with its own CLI utility, or with the json cli utility.
>
>Bunyan also comes with built-in support for DTrace, which allows you to keep your existing log level for your existing destinations (e.g. INFO) but enable at runtime a more verbose level (e.g. TRACE) and be notified in user space of those log entries, without them also going to your existing destinations and potentially filling the disks. DTrace is completely safe to use at runtime, so if enabling higher levels of logging would result in detrimental effect your system DTrace will exit before doing your system harm.
>
>That is, you've already defined in your configuration the level at which you want your application to log, but your process is currently misbheaving and you're looking to find out more information without potentially restarting the service or increasing the amount of storage where your logs are stored. With bunyan and DTrace you can enable your process to send to you the log level you're interested in at runtime.
>
>```bash
># bunyan -p *
>[2013-09-27T18:16:19.679Z] DEBUG: test/1076 on sharptooth.local: something went wrong
>```
>Read more about using bunyan to do runtime log snooping.

### fast
>Fast is a lightweight library for efficiently handling JSON messaging across a TCP channel. At its base it was created to enable message-based RPC, where the result for a given command may induce a series of related objects being streamed to the client. Designed with observability in mind, fast also comes with DTrace support, allowing you to quickly identify the performance characteristics of your server and clients.

### restify
>Restify is a module for creating and consuming REST endpoints. Designed specifically to increase the observability and debugability of your application, Restify comes with first class Bunyan support as well support for DTrace. With Bunyan and DTrace support, you're gaining the ability to see via the logs or at runtime routes and their latencies over requests.

### vasync
>vasync is a control flow library, inspired by the patterns found in the async module. However vasync is designed specifically to enable a consumer to have visibility and observability into their progress for a given task. Such information is crucial when trying to determine how far along a task was before an error occurred.