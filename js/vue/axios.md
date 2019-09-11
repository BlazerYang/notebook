# axios

## axios设置baseUrl时，为什么url结尾必须有斜杠才会生效？
比如axios设置如下
```js
axios.create({
    baseUrl: '/tools'
})
```
那么仅在当前url为`http://hostname:port/tools/`时，请求才会在前方添加`tools`,比如请求`api/login/check`, 最后生成为`http://hostname:port/tools/api/login/check`. 如果当前url为`http://hostname:port/tools`，前面的请求就变成了`http://hostname:port/api/login/check`