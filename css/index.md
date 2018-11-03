# CSS

## 如何在:before或:after中使用其他css中的unicode字符图标？
比如在文件A中已有unicode图标的定义
```css
@font-face {
  font-family: 'fontname',
  url: 'fontfile'
}
.iconfont {
  font-family:"iconfont" !important;
  font-size:16px;
  font-style:normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.icon-yangshengqi:before { content: "\e600"; }
```
文件A已经被引用，那么我们在文件B中可以这样用
```scss
.class {
  font-family: 'iconfont' !important;
  &:before {
    content: '\e600';
  }
}
```