# index

## vuex

### vuex getters 总是undefined？
实例化vuex.store对象时，state中必须声明getter所需的对象，不然该getter就是undefined

## vue-router
### 动态路由的参数在子路由中总是undefined？
path属性在this.$route中而不是在this.$route.params中

### 嵌套路由带参数时，子路由path为什么会覆盖参数值？
/project/bugs/:id
在project/bugs/4页面存在路由 <router-link to="summary"></router-link>时
实际生成的href是/project/bugs/summary而不是/project/bugs/4/summary
可以通过router中的定义，将
/project/bugs/:id
增加一个默认的子路由
```js
children: [
    {
        path: '',
        redirect: 'summary'
    },{
        path: 'summary',
        component: Summary
    }
]
```
问题解决

----更新----
实际上问题依然存在，推测子组件的rout会以其所在的组件的route作为base url来生成，解决办法就是写绝对路径，以绝后患

## vue
### 事件监听时，子组件会在事件中传递参数，同时在父组件中要向回调中传递参数应该怎么做？
可以通过添加`arguments`来传递事件的参数，然后在其他位置添加其他参数，比如
```js
let parent = new Vue({
    template: `<child @click="handler(arguments[0], id)"></child>`,
    data () {
        return {
            id: 1
        }
    },
    methods: {
        handler (payload, id) {
            // payload emit from child
        }
    }
}) 


```
具体请参考该链接
[https://github.com/vuejs/vue/issues/5735](https://github.com/vuejs/vue/issues/5735)

## provice/inject

## vue中css使用新特性被过滤掉了？
`-webkit-box-orient`为实验特性，打包完毕后总是被过滤。不稳定出现，与webpack有关？


## 如何跨多层组件传递slot？
在组件A中引用组件B，在其中加入slot，但是该slot不在B中处理，而是在B的中组件C处理，此时可以用slot-scope。参考阅读：[Vue跨层级传递slot的方法](https://www.codetd.com/article/71541)
注意：
1. 单纯的slot无法跨组件传递，需要添加属性`slot-scope`
```html
<!-- 该slot会被解析至my-alpha模块的this.$scopedSlots -->
<template>
    <my-alpha>
        <div slot="named" slot-scope="props"></div>
    </my-alpha>
</template>
<!-- 该slot会被解析至my-alpha模块的this.$slots -->
<template>
    <my-alpha>
        <div slot="named"></div>
    </my-alpha>
</template>
```
2. 组件传递时，最终传入slot的组件可以通过如下方法设置作用域对象
    1. 使用render
```js
let props = {test: 123} // something you wanna use in context
{
    render: h => {
        return h('div', [this.$scopeSlots.named(props)])
    }
}
```
    2. 使用单文件或者template
```html
<template>
    <slot name="named" :test="123"></slot>
</template>
```

## 使用event.clientX和event.clientY确定邮件菜单位置时，target的hover效果消失？
clientX和clientY各加1，这样就不会挡住dom

## ueditor中点击右键时，如果在iframe之外触发mouseup和mousedown事件，那么ueditor的邮件菜单会直接消失，如何解决？如果不触发的话，列表的右键菜单则不会消失

## vue单文件模式中有函数需要返回VNode怎么办？
this.$createElement 返回vnode