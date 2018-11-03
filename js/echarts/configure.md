# configure

## 一个图中多个饼图，如何在hoverlegend时多个饼图同时触发动效？
legend是通过series.name进行关联，只要设置相同的name即可

## markpoint如何显示自定义文本？
在formatter中指定自定义文本  
```js
data: [{
  label:{
      normal:{
          show: true,
          position: 'inside',
          formatter: '{c}MB'
      }
  },
}]
```