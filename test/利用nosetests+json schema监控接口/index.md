# 利用nosetests+json schema监控接口

## nosetests
nosetests是基于pyUnit(即unittest)的一个单元测试框架，设计思想是通过扩展unittest使得测试更优雅且简单

那么，相比于unittest，nosetests做了什么改进呢？
1. 自动发现  
    nosetests会自动搜索并加载当前执行路径下的所有模块和包中以test开头的文件、方法或TestCase的子类作为测试用例执行，并在屏幕上显示测试执行结果。
    ```bash
    $ nosetests -v
    bfs_c中可以查询出数据 ... ok
    0~1之间的小数 ... ok
    超出author的时间戳范围 ... ok
    need_filter为1或者不传时，忽略score_low/score_top参数 ... ok
    测试负数 ... ok
    正常时间戳 ... ok
    测试精度 ... ok

    ----------------------------------------------------------------------
    Ran 7 tests in 0.634s

    OK
    ```
2. 支持生成器测试
    比如有如下测试用例
    ```python
    def test_evens():
        for i in range(5):
            yield check_even, i, i*3

    def check_even(n, nn):
        assert n % 2 == 0 or nn % 2 == 0
    ```
    每次调用generator会当做一次单独的用例
    ```bash
    $ nosetests generator.py  -v
    generator.test_evens(0, 0) ... ok
    generator.test_evens(1, 3) ... FAIL
    generator.test_evens(2, 6) ... ok
    generator.test_evens(3, 9) ... FAIL
    generator.test_evens(4, 12) ... ok
    ```
3. 内置插件  
    内置的插件可以满足一些常用的测试需求，比如：
    * --stop, 出错后停止执行用例
    * --pdb, 出错后进入debugger
    * --with-doctests, 支持进行doctest
    * --with-profile, 支持hotshot profiler分析程序性能
    * --failed, 支持单独运行上一轮中出错的用例
    * --processes, 支持多进程运行
    * --with-xunit, 支持生成xunit格式的测试报告
4. 第三方插件
    * [parameterized](https://github.com/wolever/parameterized), 支持测试用例参数化
    * [nose-html-reporting](https://pypi.python.org/pypi/nose-html-reporting), 生成html格式的测试报告
5. 自定义插件
    通过继承`nose.Plugin`类，并实现`nosetests`提供的接口，然后使用`setuptools`可以安装该插件，即可完成自定义插件的开发，具体有哪些接口可用，可以参考[Plugin Interface](http://nose.readthedocs.io/en/latest/plugins/interface.html#nose-plugin-api)

### nosetests的缺点
1. 插件是全局性的，一旦安装完成所有项目均可见，项目级的插件会互相影响，`nosetests`的`-h`信息会变得很臃肿；
2. 生成器用例仅支持方法生成器或非`TestCase`子类的生成器方法，不支持`TestCase`子类的生成器；
2. 插件开发说明文档不够详细，需要仔细参考其他插件实现细节才知道具体接口的用法

## JSON Schema
@import "..\json_schema\震惊！光天化日之下一男子竟在办公室做这种事情.md"

## 接口监控项目结构

```

├─conf // 公用配置
│  ├─query.json // 全局url配置文件
│  └─uid.txt // 可用uid文件
├─plugins // nosetests插件
├─tests // 测试用例
│  ├─caseModule
│  │  ├─conf // 模块配置
│  │  │  ├─query.json // url配置文件
│  │  │  └─schema.json // 接口数据格式定义
│  │  ├─__init__.py // nosetests 默认会遍历所有package中的test开头的文件寻找测试用例
│  │  ├─test_schema.py // 接口返回格式测试用例
│  │  └─test_XXXXXX.py // 自定义测试用例
├─util // 公用函数模块
└─setup.cfg // ini方式配置nosetests的默认参数
```
使用时直接执行`nosetests tests`运行全部测试用例
需要监控的话可以放在jenkins中直接跑，其自带插件可以解析XUnit格式的测试报告，如果出现用例失败发送邮件即可


## 后记
在写这篇分享的时候才注意到一个`nosetests`首页文档的这么一句话
>Nose has been in maintenance mode for the past several years and will likely cease without a new person/team to take over maintainership. New projects should consider using Nose2, py.test, or just plain unittest/unittest2.

大意就是该项目差不多已经没人维护了，新项目可以试试nose2或者干脆直接用unittest2(注意这句话)

然后我看了下`nosetests`的git发布历史，果然已经三年没有更新了（最新版1.3.7,更新于2015/6/2）
然后我顺着推荐链接调研了一下`nosetests2`,发现原班人马基本都跑来这个项目了（最新版0.7.4,更新于2018/2/18）。但是新的问题出现了
>When nose2 was first written, the plan for its future was to wait for unittest2 plugins to be released (nose2 is actually based on the plugins branch of unittest2). Once that was done, nose2 was to become a set of plugins and default configuration for unittest2.
>
>However, based on the current status of unittest2, it is doubtful that this plan will ever be carried out.
>Current Goals
Even though unittest2 plugins never arrived, nose2 is still being maintained! We have a small community interested in continuing to work on and use nose2
>
>However, given the current climate, with much more interest accruing around pytest, nose2 is prioritizing bugfixes and maintenance ahead of new feature development.

大意是等到`unittest2`的`plugins`分支发布后，`nose2`就可以作为增强插件版的`unittest2`发布啦。但是因为该分支迟迟不肯发布，所以我们的宏伟目标差不多就算是凉了。
考虑到当前的环境，推荐大家去用`pytest`，我们目前的主要任务是旧功能维护而不是新功能开发(现在知道为啥上面那句话这么不自信了)

@import "snippet/nose_timeline.json" {as="vega"}

## pytest
鉴于时间关系没有调研该框架，回头抽时间补上
- [ ] pytest调研
