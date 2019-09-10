# pipeline
流水线相关问题记录

## pipeline script

### node
一个node是一个节点，是执行step的具体环境

### agent
代理，用于指定整个流水线或某个阶段在jenkins具体的运行位置。
可用参数：
1. `any`, 可在任何可用的代理上执行
2. `none`, 在pipeline下设置为none，则意味着每个stage必须指定自己的运行位置
3. `label`, 在指定label的位置上运行，比如：`agent {label 'linux'}` , `agent {label 'windows'}`
4. `node`, 其中包含`label`选项，同时还支持其他配置（详见`node`那一节)
5. `docker`, 使用给定的容器来执行
```jenkinsfile
agent {
    docker {
        image 'maven:3-alpine'
        label 'my-defined-label'
        args  '-v /tmp:/tmp'
    }
}
```
6. `dockerfile`, 使用源代码中包含的`Dockerfile`构建的容器来指向性
```jenkinsfile
agent {
    // Equivalent to "docker build -f Dockerfile.build --build-arg version=1.0.2 ./build/
    dockerfile {
        filename 'Dockerfile.build'
        dir 'build'
        label 'my-defined-label'
        additionalBuildArgs  '--build-arg version=1.0.2'
    }
}
```
常见选项：
1、label，，node、docker和dockerfile可用，node中必填
2. customWorkspace，在自定义的目录中运行流水线，而不是默认值，相对路径是相对于当前工作目录，也可用绝对路径
3. reuseNode， 默认false，docker或dockerfile中可用，使用同一个节点的相同目录来购将，而不是重新起一个容器

### post
post会根据前面的pipeline或stage的运行情况来运行，可用在pipeline或stages后面
支持的条件语句：
1. always, 总是执行
2. changed， 当前pipeline或stages的状态变化时执行
3. failure，失败时执行
4. success， 成功是执行
5. unstable，不稳定时执行
6. aborted，手动终止时执行
```jenkinsfile
pipeline {
    agent any
    stages {
        stage('Example') {
            steps {
                echo 'Hello World'
            }
        }
    }
    post {
        always {
            echo 'I will always say Hello again!'
        }
    }
}
```

### stages
包含一系列的stage方法，其中包含了pipeline定义的工作集合，仅可用一次，在pipeline中

### steps
每个stage中均有且仅有一个，用于包含一系列step

### environment
定义一组键值对，根据其定义的位置，在相关的steps中生效
该方法支持一个特殊的辅助函数`credentials()`，其用于获取jenkins中预定义的凭证信息
可用于pipiline或stage下
```
pipeline {
    agent any
    environment { 
        CC = 'clang'
    }
    stages {
        stage('Example') {
            environment { 
                AN_ACCESS_KEY = credentials('my-prefined-secret-text') 
            }
            steps {
                sh 'printenv'
            }
        }
    }
}
```

### options
用于配置流水线
非必填，仅在pipeline下可用一次
可用配置
1. buildDiscarder, 指定保留最近n次运行的结果
2. disableConcurrentBuilds， 禁止并行运行
3. overrideIndexTriggers， 覆盖分支索引触发器的默认处理
4. skipDefaultCheckout，跳过agent方法中的代码检出操作（应该值得是dockerfile？）
5. skipStagesAfterUnstable, 如果构建状态变为unstable，则跳过stages
6. timeout，超时时间
7. retry， 失败重试次数
8. timestamps，在console的输出语句之前加上时间

### parameters
提供一系列用户在触发流水线时需要填写的参数
非必填，仅在pipeline下可用一次
可用参数：
1. string，字符串， `parameters { string(name: 'DEPLOY_ENV',
defaultValue: 'staging', description: '') }`
2. booleanParam, 布尔值, `parameters { booleanParam(name: 'DEBUG_BUILD',
defaultValue: true, description: '') }`

Q: 什么是分支索引触发器？

### triggers
定义流水钱的触发方式
非必填，仅在pipeline下可用一次
可用参数：
1. cron, 轮询
2. pollSCM, 采用类似的cron的方式轮询代码，如果出现变动的话，会执行流水线
3. upstream， 逗号分隔的jenkins任务，其中任意一个达到设定的状态，就触发

### stage
位于stages中，包含steps，可选的agent或其他stage相关方法，jenkins所有实际完成的工作，都被包装在stage中

### tools
定义自动安装和需要放在PATH中的工具，在`agent none`时会被忽略
位于pipeline或stage中
支持的工具：
1. maven
2. jdk
3. gradle


### when
用于指定在何种条件下运行stage，如果包含多个条件，则其为&&的关系
位于stage中
内置条件：
1. branch，当分支为指定值时， `when { branch 'master' }.`
2. environment, 当指定的环境变量为指定值时，`when { environment name: 'DEPLOY_TO', value: 'production' }`
3. expression, 当指定的groovy表达式返回true时，`when {expression { return params.DEBUG_BUILD } }`
4. not， 其他条件可以嵌套叠加，`when { not { branch 'master' } }`
5. allOf，所有子条件均为true时， `when { allOf { branch 'master'; environment name: 'DEPLOY_TO', value:'production' } }`
6. anyOf, 任一子条件为true时， `when { anyOf { branch 'master'; branch 'staging' } }`

### parallel
用于stage中，指示下属的stage采用并行的方式运行，同时可以设置`failFast true`，其中任何一个子进程失败了强制其他进程也失败
```
pipeline {
    agent any
    stages {
        stage('Example') {
            steps {
                echo 'Hello World'

                script {
                    def browsers = ['chrome', 'firefox']
                    for (int i = 0; i < browsers.size(); ++i) {
                        echo "Testing the ${browsers[i]} browser"
                    }
                }
            }
        }
    }
}
```

### steps
以下步骤仅支持在声明式流水线中
1. script，内容为脚本式流水线
```
pipeline {
    agent any
    stages {
        stage('Example') {
            steps {
                echo 'Hello World'

                script {
                    def browsers = ['chrome', 'firefox']
                    for (int i = 0; i < browsers.size(); ++i) {
                        echo "Testing the ${browsers[i]} browser"
                    }
                }
            }
        }
    }
}
```
2. 


## shell script中需要引用shell变量而非pipeline变量，如何对 $ 转义？
jenkins声明式流水线语法中，使用`sh`执行命令时，三单引号和三双引号行为并不同：
* 三单引号：不会将$解析为jenkins变量
* 三双引号：会将$解析为jenkins变量，此时会引用对原shell脚本中对shell变量的引用
三双引号中可以通过 ${'$'} 的方式对$进行转义
参考链接：https://serverfault.com/questions/930312/jenkins-environment-variable-not-setting-up-from-pipeline

## shell script中如何设置环境变量？
固定设置，这方法不能设置动态生成的值：
```sh
echo ${env.VARIABLE='bingo'}
```
动态设置，目前只用通过groovy脚本设置的方法：
```groovy
foo = readFile 'filename'
foo = foo.minus('\n')
env.VARIABLE = foo
```

## 获取jenkins任务触发原因
Started by user admin
Started by timer
Started by an SCM change
Started by upstream project "qixiao_664_403_触发其他流水线" build number 1