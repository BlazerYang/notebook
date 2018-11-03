# Error Handling in Node.js
Error handling is a pain, and it's easy to get by for a long time in Node.js without dealing with errors correctly. However, building robust Node.js applications requires dealing with errors properly, and it's not hard to learn how. If you're really impatient, skip down to the "Summary" section for a tl;dr.

This document will answer several questions that programmers new to Node.js often ask:

* In functions that I write, when should I throw an error, and when should I emit it with a callback, event emitter, or something else?
* What should my functions assume about their arguments? Should I check that they're the correct types? Should I check more specific constraints, like that an argument is non-null, is non-negative, looks like an IP address, or the like?
* How should I deal with arguments that don't match what the function expects? Should I throw an exception or emit an error to the callback?
* How can I programmatically distinguish between different kinds of errors (e.g., a "Bad Request" error vs. a "Service Unavailable" error)?
* How can I provide enough detail with my errors so that callers can know what to do about them?
* How should I handle unexpected errors? Should I use try/catch, domains, or something else?

This document is divided into several parts that build on one another:

* **Background**: what you're expected to know already.
* **Operational errors vs. programmer errors**: introduction to two fundamentally different kinds of errors
* **Patterns for writing functions**: general principles for writing functions that produce useful errors
* **Specific recommendations for writing new functions**: a checklist of specific guidelines for writing robust functions that produce useful errors
* **An example**: example documentation and preamble for a connect function
* **Summary**: a summary of everything up to this point
* **Appendix**: Conventional properties for Error objects: a list of property names to use for providing extra information in a standard way

## Background
This document assumes:
* You're familiar with the idea of exceptions in JavaScript, Java, Python, C++, or any similar language, and that you know what it means to throw and catch them.
* You're familiar with programming in Node.js. You're comfortable with asynchronous operations and with the callback(err, result) pattern of completing an asynchronous operation.
* You should know why this pattern:

```javascript
function myApiFunc(callback) {
  /*
   * This pattern does NOT work!
   */
  try {
    doSomeAsynchronousOperation((err) => {
      if (err) {
        throw (err);
      }
      /* continue as normal */
    });
  } catch (ex) {
    callback(ex);
  }
}
```
does not work to handle errors.

You should also be familiar with the four main ways to deliver an error in Node.js:

* throw the error (making it an exception).
* pass the error to a callback, a function provided specifically for handling errors and the results of asynchronous operations
* pass the error to a reject Promise function
* emit an "error" event on an EventEmitter

We'll discuss when to use each of these patterns below. This document does not assume that you know anything about domains.

Finally, you should know that in JavaScript (and Node.js especially), there's a difference between an error and an exception. An error is any instance of the Error class. Errors may be constructed and then passed directly to another function or thrown. When you throw an error, it becomes an exception.

Here's an example of using an error as an exception:

```javascript
throw new Error('something bad happened');
```
but you can just as well create an Error without throwing it:

```javascript
callback(new Error('something bad happened'));
```
and this is much more common in Node.js because most errors are asynchronous. As we'll see, it's very uncommon to need to catch an error from a synchronous function. This is very different than Java, C++, and other languages that make heavy use of exceptions.

## Operational errors vs. programmer errors
It's helpful to divide all errors into two broad categories:

* **Operational errors** represent run-time problems experienced by correctly-written programs. These are not bugs in the program. In fact, these are usually problems with something else: the system itself (e.g., out of memory or too many open files), the system's configuration (e.g., no route to a remote host), the network (e.g., socket hang-up), or a remote service (e.g., a 500 error, failure to connect, or the like). Examples include:
  * failed to connect to server
  * failed to resolve hostname
  * invalid user input
  * request timeout
  * server returned a 500 response
  * socket hang-up
  * system is out of memory
* **Programmer errors** are bugs in the program. These are things that can always be avoided by changing the code. They can never be handled properly (since by definition the code in question is broken).
  * tried to read property of "undefined"
  * called an asynchronous function without a callback
  * passed a "string" where an object was expected
  * passed an object where an IP address string was expected

People use the term "errors" to talk about both operational and programmer errors, but they're really quite different. Operational errors are error conditions that all correct programs must deal with, and as long as they're dealt with, they don't necessarily indicate a bug or even a serious problem. "File not found" is an operational error, but it doesn't necessarily mean anything's wrong. It might just mean the program has to create the file it's looking for first.

By contrast, programmer errors are bugs. They're cases where you made a mistake, maybe by forgetting to validate user input, mistyping a variable name, or something like that. By definition there's no way to handle those. If there were, you would have just used the error handling code in place of the code that caused the error!

This distinction is very important: operational errors are part of the normal operation of a program. Programmer errors are bugs.

Sometimes, you have both operational and programming errors as part of the same root problem. If an HTTP server tries to use an undefined variable and crashes, that's a programmer error. Any clients with requests in flight at the time of the crash will see an ECONNRESET error, typically reported in Node as a "socket hang-up". For the client, that's a separate operational error. That's because a correct client must handle a server that crashes or a network that flakes out.

Similarly, failure to handle an operational error is itself a programmer error. For example, if a program tries to connect to a server but it gets an ECONNREFUSED error, and it hasn't registered a handler for the socket's 'error' event, then the program will crash, and that's a programmer error. The connection failure is an operational error (since that's something any correct program can experience when the network or other components in the system have failed), but the failure to handle it is a programmer error.

The distinction between operational errors and programmer errors is the foundation for figuring out how to deliver errors and how to handle them. Make sure you understand this before reading on.

## Handling operational errors
Just like performance and security, error handling isn't something that can be bolted onto a program that has no error handling already. Nor can you centralize all error handling in one part of the program, the same way you can't centralize "performance" in one part of the program. Any code that does anything which might possibly fail (opening a file, connecting to a server, forking a child process, and so on) has to consider what happens when that operation fails. That includes knowing how it may fail (the failure mode) and what such a failure would indicate. More on this later, but the key point here is that error handling has to be done in a fine-grained way because the impact and response depend on exactly what failed and why.

You may end up handling the same error at several levels of the stack. This happens when lower levels can't do anything useful except propagate the error to their caller, which propagates the error to its caller, and so on. Often, only the top-level caller knows what the appropriate response is, whether that's to retry the operation, report an error to the user, or something else. But that doesn't mean you should try to report all errors to a single top-level callback, because that callback itself can't know in what context the error occurred, what pieces of an operation have successfully completed, and which ones actually failed.

Let's make this concrete. For any given error, there are a few things you might do:

* **Deal with the failure directly**. Sometimes, it's clear what you have to do to handle an error. If you get an ENOENT error trying to open a log file, maybe this is the first time the program has run on this system and you just need to create the log file first. A more interesting case might be where you're maintaining a persistent connection to a server (e.g., a database), and you get a "socket hang-up" error. This usually means either the remote side or the network flaked out, and it's frequently transient, so you'd usually deal with this by reconnecting. (This isn't the same as retrying, below, since there's not necessarily an operation going on when you get this error.)
* **Propagate the failure to your client**. If you don't know how to deal with the error, the simplest thing to do is to abort whatever operation you're trying to do, clean up whatever you've started, and deliver an error back to your client. (How to deliver that error is another question, and it's discussed below.) This is appropriate when you expect that whatever caused the error is not going to change soon. For example, if the user gave you invalid JSON, it's not going to help to try parsing it again.
* **Retry the operation**. For errors from the network and remote services (e.g., a web service), it's sometimes useful to retry an operation that returns an error. For example, if a remote service gives a 503 (Service Unavailable error), you may want to retry in a few seconds. **If you're going to retry, you should clearly document that you may retry multiple times, how many times you'll try before failing, and how long you'll wait between retries**. Also, **don't assume that you should always retry an operation**. If you're several layers deep in the stack (e.g., you're being called by a client, which was called by another client, which is being driven by a human), it's usually better to fail fast and let the end client deal with retries. If every layer of the stack thinks it needs to retry on errors, the user can end up waiting much longer than they should because because each layer didn't realize that the underlying layer was also retrying.
* **Blow up**. For errors that truly can't happen, or would effectively represent programmer errors if they ever did (e.g., failed to connect to a localhost socket that's supposed to be listening in the same program), it's fine to log an error message and crash. Other errors like running out of memory effectively can't be handled in a dynamic language like JavaScript anyway, so it may be totally reasonable to crash. (That said, you can get ENOMEM from discrete operations like child_process.exec, and those you can reasonably handle, and you should consider doing so.) You can also blow up if there's nothing you can reasonably do about something and an administrator needs to fix things. For example, if you run out of file descriptors or don't have permission to access your configuration file, there's nothing you can do about this, and a user will have to log in and fix things anyway.
* **Log the error — and do nothing else**. Sometimes, there's nothing you can do about something, there's nothing to retry or abort, and there's also no reason to crash the program. An example might be if you're keeping track of a group of remote services using DNS and one of those services falls out of DNS. There's nothing you can do about it except log a message and proceed with the remaining services. But you should at least log something in this case. (There are exceptions to every rule. If this is something that may happen thousands of times per second, and there's nothing you can do about it, it's probably not worth logging it every time it happens. But do log it periodically.)

## (Not) handling programmer errors
There's nothing you can do to handle a programmer error. By definition, the code that was supposed to do something was broken (e.g., had a mistyped variable name), so you can't fix the problem with more code. If you could, you'd just use the error handling code in place of the broken code.

Some people advocate attempting to recover from programmer errors — that is, allow the current operation to fail, but keep handling requests. This is not recommended. Consider that a programmer error is a case that you didn't think about when you wrote the original code. How can you be sure that the problem won't affect other requests? If other requests share any common state (a server, a socket, a pool of database connections, etc.), it's very possible that the other requests will do the wrong thing.

A typical example is a REST server (e.g., using restify) where one of the request handlers throws a ReferenceError (e.g., used a mistyped variable name). There are a lot of ways this that continuing on can lead to serious bugs that are extremely difficult to track down. For a few examples:

1. Some piece of state shared by requests may be left null, undefined, or otherwise invalid, so that when the next request tries to use it, it blows up too.
2. A database (or other) connection may be leaked, reducing the number of future requests you can handle in parallel. This can get so bad that you're left with just a few connections, and you end up handling requests in series instead of concurrently.
2. Worse, a postgres connection may be left inside an open transaction. This causes postgres to "hang on" to old versions of rows in the table because they may be visible to that transaction. This can stay open for weeks, resulting in a table whose effective size grows without bound — causing subsequent queries to slow down by orders of magnitude — from a few milliseconds to a minute. While this problem is obviously postgres-specific, it's an example of how horribly broken a program's state can be after even a simple programmer error.
2. A connection may be left in an authenticated state and used for a subsequent connection. You may end up running a request for the wrong user.
2. A socket may be left open. Node normally uses a 2-minute timeout on idle sockets, but this can be overridden, resulting in a leaked file descriptor. If this happens enough, you can run out of file descriptors and crash. Even if you don't override this timeout, the client may hang for two minutes and then see an unexpected "hang-up" error. The two-minute delay makes the problem annoying to deal with and debug.
2. Memory references may be left around. This results in leakage, which results in running out of memory, or (worse) increasing time spent in GC, causing performance to tank horribly. This is particularly hard to debug, and it would be especially tricky to associate it with the programmer errors that triggered the leakage.

**The best way to recover from programmer errors is to crash immediately**. You should run your programs using a restarter that will automatically restart the program in the event of a crash. With a restarter in place, crashing is the fastest way to restore reliable service in the face of a transient programmer error.

The only downside to crashing on programmer errors is that connected clients may be temporarily disrupted, but remember:

* By definition, these errors are always bugs. We're not talking about legitimate system or network failures, but actual bugs in the program. They should be rare in production, and the top priority has to be to debug and fix them.
* For all the cases described above (and many more), the requests in flight are not necessarily going to complete successfully anyway. They may complete successfully, they may crash the server again, they may complete incorrectly in obvious ways, or they may complete wrongly in very subtle ways that are very hard to debug.
* In a reliable distributed system, clients must be able to deal with server failure by reconnecting and retrying requests. Network and system failure are a reality, whether or not the Node.js program itself is allowed to crash.
* If your production program is crashing so often that these disconnections are a problem, then the real problem is that the server is so buggy, not that it crashes in the case of a bug.

If disconnecting clients is a frequently problem because a server crashes so often, you should focus on the bugs that cause the service to crash — and make those exceptional — rather than trying to avoid crashing in cases where the code is obviously wrong. [The best way to debug these problems is to configure Node to dump core on an uncaught exception](https://www.joyent.com/node-js/production/debug#postmortem). On both GNU/Linux and illumos-based systems, you can use these core files to see not only the stack trace where the program crashed, but the arguments to each of these functions and most other JavaScript objects as well, even those only referenced in closures. Even without core dumps configured, you can use the stack information and logs to make a start at the problem.

Finally, remember that a programmer error on a server just becomes an operational error on a client. Clients have to deal with servers crashing and network blips. That's not just theoretical — both really do happen in production systems.

## Patterns for writing functions
We've talked about how to handle errors, but when you're writing a new function, how do you deliver errors to the code that called your function?

The single most important thing to do is **document** what your function does, including what arguments it takes (including their types and any other constraints), what it returns, what errors can happen, and what those errors mean. **If you don't know what errors can happen or don't know what they mean, then your program cannot be correct except by accident.** So if you're writing a new function, you have to tell your callers what errors can happen and what they mean.

## Throw, Callback, Reject, or EventEmitter?
There are three basic patterns for a function to deliver errors.

* throw delivers an error synchronously — that is, in the same context where the function was called. If the caller (or the caller's caller, ...) used try/catch, then they can catch the error. If none of the callers did, the program usually crashes. (The error can also be handled by domains or the process-wide "uncaughtException" event, which are discussed below.)
* Callbacks are the most basic way of delivering an error asynchronously. The user passes you a function (the callback), and you invoke it sometime later when the asynchronous operation completes. The usual pattern is that the callback is invoked as callback(err, result), where only one of err and result is non-null, depending on whether the operation succeeded or failed.
* Promise rejections are a common way to deliver an error asynchrously. This method is growing in popularity since the release of Node.js version 8 that includes support for async/await. This allows asynchrounous code to be written to look like synchronous code and to catch errors using try/catch.
* For more complicated cases, instead of using a callback, the function itself can return an EventEmitter object, and the caller would be expected to listen for error events on the emitter. This is useful in two particular cases:
  * When you're doing a complicated operation that may produce multiple errors or multiple results. For example, think about a request that fetches rows from a database and then streams the rows back as they arrive, rather than waiting for them all to arrive first. In this case, instead of taking a callback, your function would return an EventEmitter and emit row events for each result, an end event when all results have been reported, and an error event if any error is encountered.
  * For objects that represent complex state machines, where a lot of different asynchronous things can happen. For example, a socket is an event emitter that may emit "connect", "end", "timeout", "drain", and "close". It's natural to make "error" just another type of event that the socket can emit. When using this approach, it's important to be clear about when "error" is emitted, whether any other events may be emitted, what other events may be seen at the same time (e.g., "close"), what order they happen in, and whether the socket is closed at the end of it.

For the most part, we'll lump callbacks and event emitters in the same bucket of "asynchronous error delivery". If you want to deliver an error asynchronously, You generally want to use one or the other of these (callback or event emitter), but not both.

So, when do you use throw, and when do you use callbacks or event emitters? It depends on two things:

* Is the error an operational error or a programmer error?
* Is the function itself synchronous or asynchronous?

By far, the most common case is an operational error in an asynchronous function. For the majority of these, you'll want to have your function take a callback as an argument, and you'll just pass the error to the callback. This works very well, and is widely used. See the Node fs module for examples. If you've got a more complicated case like the ones described above, you may want to use an event emitter instead, but you'll still deliver the error asynchronously.

The next most common case is an operational error in a synchronous function like JSON.parse. For these functions, if you encounter an operational error (like invalid user input), you have to deliver the error synchronously. You can either throw it (much more common) or return it.

For a given function, if any operational error can be delivered asynchronously, then all operational errors should be delivered asynchronously. There may be cases when you know immediately that the request will fail, but not because of a programmer error. Maybe the function caches the results of recent requests and there's a cache entry with an error that you'll return to the caller. Even though you know right away that the request will fail, you should deliver that error asynchronously.

The general rule is that **a function may deliver operational errors synchronously (e.g., by throwing) or asynchronously (by passing them to a callback or emitting error on an EventEmitter), but it should not do both.** This way, a user can handle errors by either handling them in the callback or using try/catch, but they never need to do both. Which one they use depends on what how the function delivers its errors, and that should be specified with its documentation.

We've left out programmer errors. Recall that these are always bugs. They can also usually be identified immediately by checking the types (and other constraints) on arguments at the start of the function. A degenerate case is where someone calls an asynchronous function but doesn't pass a callback. You should throw these errors immediately, since the program is broken and the best chance of debugging it involves getting at least a stack trace and ideally a core file at the point of the error. To do this, we recommend validating the types of all arguments at the start of the function.

Since programmer errors should never be handled, this recommendation doesn't change our conclusion above that a caller can use try/catch or a callback (or event emitter) to handle errors but never needs to use both. For more, see "(Not) handling programmer errors" above.

Here's a summary of these recommendations with some example functions in Node's core libraries, in rough order of the frequency that each kind of problem comes up:

| Example func |	Kind of func |	Example error |	Kind of error |	How to deliver |	Caller uses |
|--------------|---------------|----------------|---------------|----------------|--------------|
|fs.stat       |	asynchronous |	file not found|	operational   |callback |handle callback error|
|JSON.parse    |	synchronous  |	bad user input|	operational   |	throw	         |try/catch     |
|fs.stat       |	asynchronous |null for filename|	programmer  |	throw	         |none (crash)  |
Operational errors in an asynchronous function (row 1) are by far the most common case. Use of synchronous functions that report operational errors (row 2) is very rare in Node.js except for user input validation. However, with the release of Node.js version 8 people are starting to promisify these asynchronous functions and using await inside of a try/catch. Programmer errors (row 3) should never happen except in development.

## Bad input: programmer error or operational error?
How do you know what's a programmer error vs. an operational error? Quite simply: it's up to you to define and document what types your function will allow and how you'll try to interpret them. If you get something other than what you've documented to accept, that's a programmer error. If the input is something you've documented to accept but you can't process right now, that's an operational error.

You have to use your judgment to decide how strict you want to be, but we can make some suggestions. To get specific, imagine a function called "connect" that takes an IP address and a callback and invokes the callback asynchronously after either succeeding or failing. Suppose the user passes something that's obviously not a valid IP address, like 'bob'. In this case, you have a few options:

* Document that the function only accepts strings representing valid IPv4 addresses, and throw an exception immediately if the user passes 'bob'. This is strongly recommended.
* Document that the function accepts any string. If the user passes 'bob', emit an asynchronous error indicating that you couldn't connect to IP address 'bob'.

Both of these are consistent with the guidelines about operational errors and programmer errors. You're really deciding whether to consider such input to be a programmer error or an operational error. In general, user input validation functions are very loose. Date.parse, for example, accepts a variety of inputs — that's basically the point. But for most other functions, we strongly recommend biasing towards being stricter rather than looser. The more your function tries to guess what the caller meant (using implied coercions, either as part of JavaScript or doing it explicitly in your function), the more likely it'll guess wrong. Instead of saving developers the effort required to be more explicit, you may well do something that wastes hours of the developer's time to debug. Besides, you can always make the function less strict in future versions if you decide that's a good idea, but if you discover that your attempt to guess what people meant leads to really nasty bugs, you can't fix it without breaking compatibility.

So if a value cannot possibly be valid (e.g., undefined for a required string, or a string that's supposed to be an IP address but obviously isn't), you should document that it isn't allowed and throw an error immediately if you see it. As long as you document it, then these are programmer errors, not operational errors. By throwing immediately, you minimize the damage caused by the bug and preserve the information the developer would want to debug the problem (e.g., the call stack, and if you're using core dumps, the arguments and all of memory as well).

## What about domains and process.on('uncaughtException')?
Operational errors can always be handled through an explicit mechanism: catching an exception, processing the error in a callback, handling an "error" event on a EventEmitter, and so on. Domains and the process-wide 'uncaughtException' event are primarily useful to attempt to handle or recover from unanticipated programmer errors. For all the reasons described above, this is strongly discouraged.

### Specific recommendations for writing new functions
We've talked about a lot of guiding principles, so now let's get specific.

>#### 1. Be clear about what your function does.
>This is the single most important thing to do. The documentation for every interface function should be very clear about:
>
>* what arguments it expects
>* the types of each of those arguments
>* any additional constraints on those arguments (e.g., must be a valid IP address)
>
>If any of these are wrong or missing, that's a programmer error, and you should throw immediately.
>
>You'll also want to document:
>
>* what operational errors callers should expect (including their names)
>* how to handle operational errors (e.g., will they be thrown, passed to the callback, emitted on an event emitter, etc.)
>* the return value

>#### 2. Use Error objects (or subclasses) for all errors, and implement the Error contract.
>All of your errors should either use the Error class or a subclass of it. You should provide name and message properties, and stack should work too (and be accurate).

>#### 3. Use the Error's name property to distinguish errors programmatically.
>When you need to figure out what kind of error this is, use the name property. Built-in JavaScript names you may want to reuse include "RangeError" (an argument is outside of its valid range) and "TypeError" (an argument has the wrong type). For HTTP errors, it's common to use the RFC-given status text to name the error, like "BadRequestError" or "ServiceUnavailableError".
>
>Don't feel the need to create new names for everything. You don't need separate InvalidHostnameError, InvalidIpAddressError, InvalidDnsServerError, and so on, when you could just have a single InvalidArgumentError and augment it with properties that say what's wrong (see below).

>#### 4. Augment the Error object with properties that explain details
>For example, if an argument was invalid, set propertyName to the name of the property that was invalid and propertyValue to the value that was passed. If you failed to connect to a server, use remoteIp to say which IP you tried to connect to. If you got a system error, include the syscall property to say which syscall failed, and the errno property to say which system errno you got back. See the appendix for example property names to use.
>
>At the very least, you want:
>
>* name: used to programmaticaly distinguish between broad types of errors (e.g., illegal argument vs. connection failed)
>* message: a human-readable error message. This should be complete enough for whomever you expect to read it to understand it. If you're passing an error from a lower level of the stack, you should add something to the message that explains what you were doing. See the next item for more on wrapping errors.
>* stack: generally, don't mess with this. Don't even augment it. V8 only computes it if someone actually reads the property, which improves performance dramatically for handlable errors. If you read the property just to augment it, you'll end up paying the cost even if your caller doesn't need the stack.
>
>You should also include enough information in the error message for the caller to construct their own error message without having to parse yours. They may want to localize the error message, or aggregate a large number of errors together, or display the error message differently (e.g., in a table on a web site, or by highlighting a bad user-input form field).

>#### 5. If you pass a lower-level error to your caller, consider wrapping it instead.
>Often you'll find that your asynchronous function funcA calls some other asynchronous function funcB, and that if funcB emits an Error, you'll want funcA to emit the same Error. (Note that the second part doesn't always follow from the first. Sometimes funcA will retry instead. Or sometimes you'll have funcA ignore the error because it may just mean there's nothing to do. But we're just considering the simple case where funcA wants to directly return funcB's error here.)
>
>In this case, consider wrapping the Error instead of returning it directly. By wrapping, we mean propagating a new Error that includes all of the information from the lower level, plus additional helpful context based on the current level. The verror module provides an easy way to do this.
>
>For example, suppose you have a function called fetchConfig, which fetches a server's configuration from a remote database. Maybe you call this function when your server starts up. The whole path at startup looks like this:
>
> 1. Load configuration
>     1. Connect to the database server. This in turn will:
>         1. Resolve the DNS hostname of the database server
>         1. Make a TCP connection to the database server.
>         1. Authenticate to the database server
>     1. Make the DB request
>     1. Decode the response
>     1. Load the configuration
> 1. Start handling requests
>Suppose at runtime there's a problem connecting to the database server. If the connection step at 1.1.2 fails because there's no route to the host, and each level propagates the error to the caller (as it should), but doesn't wrap the error first, then you might get an error message like this:
>
>```
>myserver: Error: connect ECONNREFUSED
>```
>This is obviously not very helpful.
>
>On the other hand, if each level wraps the Error returned from the lower level, you can get a much more informative message:
>```
>myserver: failed to start up: failed to load configuration: failed to connect to database server: failed to connect to 127.0.0.1 port 1234: connect ECONNREFUSED
>```
>You may want to skip wrapping in some levels and get a less pedantic message:
>```
>myserver: failed to load configuration: connection refused from database at 127.0.0.1 port 1234.
>```
>On the other hand, it's better to err on the side of including more information rather than less.
>
>If you decide to wrap an Error, there are a few things to consider:
>
> * Leave the original error intact and unchanged, and make sure the underlying Error is still available to the caller in case it wants to get some information from it directly.
> * Either use the same "name" for your error, or else explicitly choose one that makes more sense. For example, the bottom level might be a plain Error from Node, but the error from step 1 might be a InitializationError. (But don't feel obligated to create new names for errors if they can be programmaticaly distinguished by looking at the other properties.)
> * Preserve all of the properties of the original error. Augment the message property as appropriate (but don't change it on the original error). Shallow-copy all other properties like syscall, errno, and the like. You're best off copying all properties except for name, message, and stack, rather than hardcoding a list of properties to explicitly copy. Don't do anything with stack, since even reading it can be relatively expensive. If the caller wants to produce a combined stack, it should iterate the causes and print each one's stack instead.
>At Joyent, we use the verror module to wrap errors since it's syntactically concise. As of this writing, it doesn't quite do all of this yet, but it will be extended to do so.

### An example
Consider a function that asynchronously connects to a TCP port at an IPv4 address. Here's an example of how we might document it:
```js
/*
 * Make a TCP connection to the given IPv4 address.  Arguments:
 *
 *    ip4addr        a string representing a valid IPv4 address
 *
 *    tcpPort        a positive integer representing a valid TCP port
 *
 *    timeout        a positive integer denoting the number of milliseconds
 *                   to wait for a response from the remote server before
 *                   considering the connection to have failed.
 *
 *    callback       invoked when the connection succeeds or fails.  Upon
 *                   success, callback is invoked as callback(null, socket),
 *                   where `socket` is a Node net.Socket object.  Upon failure,
 *                   callback is invoked as callback(err) instead.
 *
 * This function may fail for several reasons:
 *
 *    SystemError    For "connection refused" and "host unreachable" and other
 *                   errors returned by the connect(2) system call.  For these
 *                   errors, err.errno will be set to the actual errno symbolic
 *                   name.
 *
 *    TimeoutError   Emitted if "timeout" milliseconds elapse without
 *                   successfully completing the connection.
 *
 * All errors will have the conventional "remoteIp" and "remotePort" properties.
 * After any error, any socket that was created will be closed.
 */
function connect(ip4addr, tcpPort, timeout, callback) {
  assert.equal(typeof (ip4addr), 'string',
      "argument 'ip4addr' must be a string");
  assert.ok(net.isIPv4(ip4addr),
      "argument 'ip4addr' must be a valid IPv4 address");
  assert.equal(typeof (tcpPort), 'number',
      "argument 'tcpPort' must be a number");
  assert.ok(!isNaN(tcpPort) && tcpPort > 0 && tcpPort < 65536,
      "argument 'tcpPort' must be a positive integer between 1 and 65535");
  assert.equal(typeof (timeout), 'number',
      "argument 'timeout' must be a number");
  assert.ok(!isNaN(timeout) && timeout > 0,
      "argument 'timeout' must be a positive integer");
  assert.equal(typeof (callback), 'function');

  /* do work */
}
```
This example is conceptually simple, but demonstrates a bunch of the suggestions we talked about:

* The arguments, their types, and other constraints on their values are clearly documented.
* The function is strict in what arguments it accepts and it throws errors (programmer errors) when it gets invalid input.
* The set of possible operational errors is documented. The different "name" values are used to distinguish logically different errors, and "errno" is used to get detailed information for system errors.
* The way errors are delivered is documented (callback is invoked upon failure.)
* The returned errors have "remoteIp" and "remotePort" fields so that a user could define a custom error message (for example, when the port number is implied, as it would be with an HTTP client).
* Although it should be obvious, the state after a failed connections clearly documented: any sockets that were opened will have been closed already.

This may seem like more work than people usually put into writing what should be a well-understood function, but most functions aren't so universally well-understood. All advice should be shrink-to-fit, and you should use your judgment if something truly is simple, but remember: ten minutes documenting expectations now may save hours for you or someone else later.

### Summary
* Learn to distinguish between operational errors, which are anticipatable, unavoidable errors, even in correct programs (e.g., failing to connect to a server), and programmer errors, which are bugs in the program.
* Operational errors can and should be handled. Programmer errors cannot be handled or reliably recovered from (nor should they be), and attempting to do so makes them harder to debug.
* A given function should deliver operational errors either synchronously (with throw) or asynchronously (with a callback or event emitter), but not both. A user should be able to use try/catch or handle errors in the callback, but should never need both. In general, using throw and expecting a caller to use try/catch is pretty rare, since it's not common in Node.js for synchronous functions to have operational errors. (The main exception are user input validation functions like JSON.parse.)
* When writing a new function, document clearly the arguments that your function expects, their types, any other constraints (e.g., "must be a valid IP address"), the operational errors that can legitimately happen (e.g., failure to resolve a hostname, failure to connect to a server, any server-side error), and how those errors are delivered to the caller (synchronously, using throw, or asynchronously, using a callback or event emitter).
* Missing or invalid arguments are programmer errors, and you should always throw when that happens. There may be gray area around what parameters the author decides are acceptable, but if you pass a function something other than what it's documented to accept, that's always a programmer error.
* When delivering errors, use the standard Error class and its standard properties. Add as much additional information as may be useful in separate properties. Where possible, use conventional property names (see below).

## Appendix: Conventional properties for Error objects.
It's strongly recommended that you use these names to stay consistent with the Errors delivered by Node core and Node add-ons. Most of these won't apply to any given error, but when in doubt, you should include any information that seems useful, both programmatically and for a custom error message.

|Property name|	Intended use|
|-------------|-------------|
|localHostname|	the local DNS hostname (e.g., that you're accepting connections at)|
|localIp|	the local IP address (e.g., that you're accepting connections at)|
|localPort|	the local TCP port (e.g., that you're accepting connections at)|
|remoteHostname|	the DNS hostname of some other service (e.g., that you tried to connect to)|
|remoteIp|	the IP address of some other service (e.g., that you tried to connect to)|
|remotePort|	the port of some other service (e.g., that you tried to connect to)|
|path|	the name of a file, directory, or Unix Domain Socket (e.g., that you tried to open)|
|srcpath|	the name of a path used as a source (e.g., for a rename or copy)|
|dstpath|	the name of a path used as a destination (e.g., for a rename or copy)|
|hostname|	a DNS hostname (e.g., that you tried to resolve)|
|ip|	an IP address (e.g., that you tried to reverse-resolve)|
|propertyName	|an object property name, or an argument name (e.g., for a validation error)|
|propertyValue|	an object property value (e.g., for a validation error)|
|syscall|	the name of a system call that failed|
|errno|	the symbolic value of errno (e.g., "ENOENT").Do not use this for errors that don't actually set the C value of errno. Use "name" to distinguish between types of errors.|

## Footnotes
```js
const func = () => {
  return new Promise((resolve, reject) => {
    setImmediate(() => {
      throw new Error('foo');
    });
  });
};

const main = async () => {
  try {
    await func();
  } catch (ex) {
    console.log('will not execute');
  }
};

main();
```
1. People sometimes write code like this when they want to handle the asynchronous error by invoking the callback function and passing the error as an argument. But they make the mistake of thinking that if they throw it from their own callback (the function passed to doSomeAsynchronousOperation), then it can be caught in the catch block. That's not how try/catch work with asynchronous functions. Recall that the whole point of an asynchronous function is that it's invoked some time later, after myApiFunc returns. That means the try block has been exited. The callback is invoked directly by Node, with no try block around it. So if you use this anti-pattern, you'll end up crashing the program when you throw the error. Event in the case of an explicit async function that uses an await in the try block, an error thrown asynchronously won't be caught. Below is an example of an error that won't be caught. 

1. In JavaScript, you can technically throw things that are not Errors, but this should be avoided. The result does not include the potential for getting a call stack, nor a "name" property for programmatic inspection, nor any useful properties describing what went wrong. 

1. The concepts of an operational error and a programmer error long predate Node.js. In Java, this loosely tracks the use of checked and unchecked exceptions, though operational errors that are known to be unhandleable, like OutOfMemoryError, are grouped with unchecked exceptions. In C, it's analogous to normal error handling vs. using an assertion, and the Wikipedia article on assertions has a similar explanation of when to use assertions vs. normal error handling. 

1. If that sounds oddly specific, it's because we've seen this in production. And it was terrible. 
