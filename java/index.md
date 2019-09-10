# index

## @override什么作用？
1. 注释
2. 提示编译器此处是否真的覆盖了父类中对应的方法，没有的话会报错

## can not instantiate List<Integer>
List is a interface, so it is can not be instantiated. you can use some kind of List implementaion, such as LinkedList
```java
List<Integer> list = new LinkedList<Integer>();
```