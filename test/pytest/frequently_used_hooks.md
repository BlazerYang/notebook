# pytest hook简介
`pytest`是一个基于`python`、功能强大的测试框架，很多项目会采用该框架维护测试用例。`pytest`除了强大的用例发现、收集、执行和报告输出之外，还提供了丰富的函数hook可以自定义插件或者框架行为，只需在`项目目录/conftest.py`文件中实现对应hook名称的函数，即可完成hook函数的注册。

下面来为大家介绍一下`pytest`中常用hook都有哪些

## 引导型hook
引导型hook仅在内部或`setuptools`安装的插件中才会调用  
* `pytest_load_initial_conftests(early_config, parser, args)`  
  实现了在命令行参数解析之前调用conftest文件
* `pytest_cmdline_parse(pluginmanager, args)`  
  解析指定参数并返回初始化的配置对象，返回第一个非None结果后停止调用后续实现
* `pytest_cmdline_main(config)`  
  用于执行命令行指令。默认实现中会调用配置hook和测试运行的主循环

## 初始化型hook
初始化型hook主要在插件和conftest.py文件中调用
* `pytest_addoption(parser)`  
  注册`argparse`风格的选项和`ini`配置风格的配置值，在测试开始时调用一次。注册的值在`config`获取到，而`config`可以通过很多内部对象的`.config`属性获取，或者使用`pytestconfig`夹具来获取
* `pytest_addhooks(pluginmanager)`  
  在插件注册时调用以添加新的`hook`，其可被其他插件实现用以改变本插件或者同本插件交互
* `pytest_configure(config)`  
  在命令行参数解析完成之后，以及插件和conftest文件加载之前调用。用于插件和conftest文件执行一下初始化操作。
* `pytest_unconfigure(config)`  
  测试进程退出之前调用
* `pytest_sessionstart(session)`  
  在`Session`对象创建之后，执行运行收集之前调用
* `pytest_sessionfinish(session, exitstatus)`  
  在测试运行结束之后，返回退出码之前调用

## 测试运行hook
每个测试用例运行周期相关的hook
* `pytest_runtestloop(session)`  
  调用以开始运行测试用例循环
* `pytest_runtest_protocol(item, nextitem)`  
  用于实现runtest_setup/call/teardown协议，包括收集异常和调用报告hook
* `pytest_runtest_logstart(nodeid, location)`  
  在用例setup之前调用
* `pytest_runtest_logfinish(nodeid, location)`  
  在用例teardown之后调用
* `pytest_runtest_setup(item)`  
  在用例执行之前调用
* `pytest_runtest_call(item)`  
  调用以执行用例
* `pytest_runtest_teardown(item, nextitem)`  
  在用例执行完成后调用
* `pytest_runtest_makereport(item, call)`  
  在runtest_setup/call/teardown之后执行，用于返回当前运行的结果

## 用例收集hook
* `pytest_collection(session)`  
  在用例收集之前调用，用于在指定的session上收集用例
* `pytest_ignore_collect(path, config)`  
  返回`True`则不会收集当前路径下的用例，所有文件/目录开始收集前均会调用该hook查询是否继续
* `pytest_collect_directory(path, parent)`  
  在遍历目录中文件之前调用
* `pytest_collect_file(path, parent)`  
  返回`Node`或者`None`作为收集的用例
* `pytest_pycollect_makeitem(collector, name, obj)`  
  为模块中的python对象返回自定义用例
* `pytest_generate_tests(metafunc)`  
  生成参数化的用例
* `pytest_make_parametrize_id(config, val, argname)`  
  生成自定义的参数化用例id
* `pytest_collection_modifyitems(session, config, items)`  
  用例收集完成之后，可用来添加、删除或者排序收集好的用例

## 报告型hook
Session相关的报告hook
* `pytest_collectstart(collector)`  
  用例开始收集之前
* `pytest_itemcollected(item)`  
  收集一个用例之后
* `pytest_collectreport(report)`  
  收集完成之后
* `pytest_deselected(items)`  
  通过关键字删除用例
* `pytest_report_header(config, startdir)`  
  定义报告标题
* `pytest_report_collectionfinish(config, startdir, items)`  
  定义显示在"collected X items"之后的文字
* `pytest_report_teststatus(report)`  
  设置用例测试结果、错误信息和状态信息
* `pytest_terminal_summary(terminalreporter, exitstatus)`  
  用于设置测试总结信息(运行完成后最后一行的 "X failed, Y passed")
* `pytest_fixture_setup(fixturedef, request)`  
  执行夹具的setup操作，返回结果会作为对应夹具的输入
* `pytest_fixture_post_finalizer(fixturedef, request)`  
  在夹具teardown，cache清空前执行
* `pytest_runtest_logreport(report)`  
  在测试setup/call/teardown之后执行，可以用于自定义相关信息
* `pytest_assertrepr_compare(config, op, left, right)`  
  定义出错断言的解释信息

## debug/交互型 hook
下面这些主要是关于特殊的报告和异常互动，较少用到
* `pytest_internalerror(excrepr, excinfo)`  
  发生内部错误时调用
* `pytest_keyboard_interrupt(excinfo)`  
  键盘中断时调用
* `pytest_exception_interact(node, call, report)`  
  抛出异常时调用
* `pytest_enter_pdb(config)`  
  进入pdb之前调用
  

## hook生命周期概览


## 应用示例：
必须需要收集出错的信息，并在测试完成后存入数据库就可以在`pytest_runtest_logreport`中保存错误信息，并在`pytest_sessionfinish`测试完成后将对应的信息保存至数据库

## 最后
通过pytest强大的hook可以定制很多自己需要的功能，通用型的功能还可以制作插件后开源，为社区添砖加瓦
