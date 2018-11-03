# index

## Feature
对应某个功能，通常一个.feature文件放一个Feature模块，类似于一个测试集

## Scenario
对应功能的某个测试点，一个Feature会有多个Scenario模块，类似于一个测试

## Given
Given用于在用户（或外部系统）在于系统交互前开始前，将系统的状态设置为指定状态，类似于单元测试setup。避免在这里描述用户交互(应在When中)

## When
When用于执行用户的关键操作，用户交互放在这里，主要的测试执行在这里

## Then
Then用于观测输出

## And
会被behave解析为其紧跟的step语句，比如
```feature
When you walking in the sun
And lick Cream Cone
```
其中的`And lick Cream Cone`会被解析为`When lick Cream Cone`

## But
效果与And一样，只是为了语义通顺

## feature中的'''包裹的文本可以在context.text中获取

## feature中的表格数据可以在context.table中获取

## 在step中调用其他step可以用context.execute_steps()
```
@when('I do the same thing as before')
def step_impl(context):
    context.execute_steps('''
        when I press the big red button
         and I duck
    ''')
```

## context.failed
设置在context的root位置，如果任何step失败了就会被置为true

## Backgroud
```
@tags @tag
Feature: feature name
  description
  further description

  Background: some requirement of this test
    Given some setup condition
      And some other setup action

  Scenario: some scenario
      Given some condition
       When some action is taken
       Then some result is expected.

  Scenario: some other scenario
      Given some other condition
       When some action is taken
       Then some other result is expected.

  Scenario: ...
```
Background可用于执行setup，其在每一个Scenario之前和任意before_钩子函数之后执行
* 每个feature最多有一个Background
* Backgroud需要放在所有的Scenario之前

优秀实践：
* 不要使用Background设置复杂的装填，除非该状态是客户端需要知道的  
    比如，如果用户名和网站名不是客户端关心的，那么你应该用一个高层级step类似于"Given that I am logged in as a site owner"
* 保持Background简明
    应该让使用者能在阅读Scenario的时候仍记得Background的内容。如果Background超过4行，你应该考虑将无关的内容移到高等级的step中，然后用step中调用step的方式处理
* 保持Background达意
    使用更生动、更故事性的叙述，因为人脑更容易记住故事而不是"User A", "User B", "Site 1"这种名字
* 保持场景简短，且不要太多
    如果一屏都写不完Background，那么你可以考虑使用高层级step或者把feature文件拆成两个

## 如何在behave中打印信息
启动时使用`behave --no-capture`

## 如何让behave在用例失败后停止执行用例
--stop
Stop running tests at the first failure.