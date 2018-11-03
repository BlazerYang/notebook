#unclassified

## js Date对象
* new Date().getTime()返回的是UTC时间 1970-01-01 00:00:00 000 至今的毫秒数。
* new Date(timestamp)和new Date(year[, month[, day]]...)均按照UTC时间初始化，如果提供的数值为本地时间, 则同预期不一致
* console.log(new Date())时，chrome中默认调用Date.prototype.toString(),而node中默认调用Date.prototype.toISOString()，另外还有两种转化方式toUTCString()和toLocaleString()函数差异
* Date中的month是从0开始的，日期是从1开始的
* 示例请参考[该文件](./examples/date/index.js)


扩展阅读: [JavaScript 时间与日期处理实战:你肯定被坑过](https://segmentfault.com/a/1190000007581722)

## ISO 8601中'2017-10-30T08:05:34.980Z'的Z表示？
“Z”表示UTC标准时区，即"00:00"
东八区会用'2017-10-30T08:05:34.980+08:00'表示

## js 中的void(0)?
不返回任何值，这样既可获取到纯正的undefined

## 如何同时遍历数组的序号和值？
可以利用Array.prototype.entries()和解构语法
```js
let names = ['John', 'Bush']
for (let [index, name] of name.entries()) {
  console.log(`index: ${index}, name: ${name}`)
}
// output:
// index: 0, name: John
// index: 1, name: Bush
```