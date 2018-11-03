# index.md

## 主Activity是什么？
Activity是Android应用程序提供交互界面的一个重要组件。main Activity也就是程序的入口

## android instrumented test?
类似于一种单元测试，但与android unit test只运行在JVM不同的是，其可以运行在真机或模拟器中。  
会增加额外的开销，但也减少了编写模拟环境代码。  
适合AIT的情况是：
1. 测试时需要Android api的支持
2. 测试时需要Android中的组件
3. 测试时需要访问Android中的特定环境元素
其他情况请使用Unit Test，它更快、消耗更少

## java注解？

## @RunWith()
使用RunWith注解改变JUnit的默认执行类，并实现自已的Listener在平时的单元测试，如果不使用RunWith注解，那么JUnit将会采用默认的执行类Suite执行

## AndroidJUnit4
AndroidJUnitRunner的别名，可让你在Android设备上运行JUnit3和JUnit4样式测试类，包括使用Espresso和UI Automator测试框架的设备。其是JUnit的子类

### JUnit中使用的注解
@Before： 初始化方法：对于每一个测试方法都要执行一次（注意与BeforeClass区别，后者是对于所有方法执行一次）
@After：释放资源，对于每一个测试方法都要执行一次（注意与AfterClass区别，后者是对于所有方法执行一次）
@Test：测试方法，在这里可以测试期望异常和超时时间 

### 一个JUnit4的单元测试用例执行顺序为:
@BeforeClass -> @Before -> @Test -> @After -> @AfterClass; 

### 每一个测试方法的调用顺序为:
@Before -> @Test -> @After;

## instrumentation？
用于实现应用instrumentation功能的基类。当程序运行切instrumentation打开时，该类会在你的应用代码之前实例化，允许你监控系统与应用间的所有交互。

## context？
一个获取应用环境全局信息的接口。这是一个有Android系统实现的抽象类。它允许访问应用相关资源和类，也可以进行应用层操作调用，比如加载activities或者广播和接收intent对象。

### intent对象
intent是一个消息床底对象，可以使用它从其他应用组件请求操作。

## UiDevice？
UiDevice提供了获取设备状态信息的方法。你同样可以使用该类来模拟用户在设备上的动作，如按压十字键或摁Home键和Menu键

### getInstance(Instrumentation instrumentation)?
获取UiDevice的单例

## PackageManager？
用于检索当前设备上安装应用包相关信息的类，可以通过getPackageManager()获取

## 如何遍历listView的子元素，不包括孙子元素？
* 尝试0：
```java
mUiDevice.findObject(new UiSelector().className("android.widget.LinearLayout").index(nIndex));
```
结果：遍历时，第0个会选中两次，第1个没有选中，然后开始第3个。  
查阅文档得知index()方法不稳当，只推荐作为最后的方法。
* 尝试1：
```java
mUiDevice.findObject(new UiSelector().className("android.widget.LinearLayout").instance(nIndex));
```
结果：只会找到list中的第一个子元素。为什么会这样？
* 尝试2：
```java
listScrollable.getChildByInstance(new UiSelector().className("android.widget.LinearLayout"), nIndex);
```
结果：同上。猜测原因同上
* 尝试3：
```java
listScrollable.getChild(new UiSelector().instance(nIndex));
```
结果：同上。猜测原因同上
* 尝试4：
```java
listScrollable.getChild(new UiSelector().clickable(true).instance(nIndex));
```
结果：这个方法可以按照预期选择。此时如果将尝试1至3中的UiSelector加上.clickable(true)时，也可以正常运行

### 使用UiSelector选择list的子元素时，为什么加上clickable(true)才能正确遍历，否则只是选中第0个？

## native指的是什么？

## 什么是native crach？什么是java crash？两者有什么区别？
