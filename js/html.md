# html

## input元素中的input和change事件有什么区别？
每次input事件同样会触发change事件
change时间同样会被textarea和select的变化事件触发

## 如何捕获鼠标右键事件？
'contextmenu'

## 点击页面中iframe不会在外部触发mouseup和mousedown事件，如何解决？
在iframe中监听click事件，回调中在外部手动触发mouseup和mousedown事件

### 如何手动触发事件？
```js
let event = new MouseEvent('mouseup', {view: window, bubbles: true, cancelable: true})
document.dispatchEvent(event)
```