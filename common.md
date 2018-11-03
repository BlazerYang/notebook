# common

## 编程中的幂等性？
编程中的幂等性指的是一个操作执行多次与执行一次的效果相同

## 动态语言
变量本身类型不固定的语言成为动态语言

## 函数式编程
借用阮一峰的例子简单理解一下([函数式编程初探](http://www.ruanyifeng.com/blog/2012/04/functional_programming.html))
过程式编程:
```js
var a = 1 + 2;
var b = a * 3;
var c = b - 4;
```
函数式编程：
```js
var result = subtract(multiply(add(1,2), 3), 4);
```

特点：
1. 函数是“第一等公民”
2. 使用表达式(expression)，而不是语句(statement)    
3. 没有副作用
4. 不修改状态
5. 引用透明

### curry/compose


## 响应式编程


## 什么是强依赖，什么是弱依赖？
