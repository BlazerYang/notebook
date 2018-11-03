# 如何利用JSON Schema校验JSON数据格式

最近笔者在工作中需要监控一批http接口，并对返回的JSON数据进行校验。正好之前在某前端大神的分享中得知这个神器的存在，调研一番之后应用在该项目中，并取得了不错的效果，特地在此分享给各位读者。

## 什么是JSON Schema?
JSON Schema是一组特殊的JSON词汇，用来标记和校验JSON数据，也可以理解为一种的对JSON数据格式定义的约定。截至本文撰写时间(2018年3月25日)，该约定的草案已经演进至第7版(draft-07)。JSON Schema使用一种人机都容易理解的方式来描述已有的数据格式。可用于客户端校验用户提交，或者自动化测试中校验结果。

## 如何获取JSON Schema?
JSON Schema在各常用语言下基本都有实现，包括：C/C++, Java, JavaScript, PHP, Python, Scala, Go等，不同语言的实现对约定草案的支持程度不尽相同，单就笔者在自动化测试中进行接口返回格式校验的需求来说均可满足。

各位读者可以在该链接（[Implementations](http://json-schema.org/implementations.html#libraries)）中获取JSON Schema在不同语言中的实现，请按需取用~

## JSON Schema的用法
用过JSON的同学都知道，JSON是构建在以下几种数据结构上的：
* object:
```json
{"name": "picotaro", "age": 38}
```
* array:
```json
["apple", "pen", "pineapple"]
```
* number:
```js
10086
3.1415926
```
* string:
```js
"pen pinapple apple pen"
```
* boolean:
```js
true
false
```
* null:
```js
null
```
通过上述这六种数据格式，我们可以自由组合出复杂的JSON数据，比如：
```json
{
    "errno": 0,
    "errmsg": "success",
    "data": {
        "name": "picotaro",
        "age": 38,
        "favorite": [
            "pen",
            "apple",
            "pinapple"
        ],
        "married": false,
    }
}

{
    "errno": 12345,
    "errmsg": "system error",
    "data": null
}
```
上面两个都是有效的JSON数据，那么当我们需要对接口返回进行校验时，我们该怎么做呢？一般的探活监控可以通过http码或者错误码来进行识别结果是否正确，但如果我们需要精准校验json数据的格式呢？难道我们要写一套复杂的通用逻辑来处理么？不，这个时候我们用JSON Schema就可以啦(众人：少废话，show me the code)。

假设我们需要接口的回显为第一种格式的数据，那么我们可以定义如下的JSON Schema来描述接口：
```json
{
    "type": "object",
    "required": ["errno", "errmsg", "data"],
    "properties": {
        "errno": {
            "type": "integer",
            "const": 0,
        },
        "errmsg": {
            "type": "string",
            "enum": ["success"]
        },
        "data": {
            "type": "object",
            "required": ["name", "age", "favorite", "married"],
            "properties": {
                "name": {
                    "type": "string",
                    "maxLength": 127,
                },
                "age": {
                    "type": "integer",
                    "maximum": 200,
                    "minimum": 0
                },
                "favorite": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "string"
                    },
                },
                "married": {
                    "type": "boolean"
                }
            }
        }
    }
}
```
你可能已经注意到JSON Schema本身就是一个JSON数据，因为其本身就是一段数据而非程序，只是一种"描述其他数据的结构"的描述性格式而已，然后校验器会根据这个schema来判断数据是否满足要求。就目前情况来说，第一种会通过，而第二种就会失败。就这样，我们通过利用一些简单的、配置式的定义来完成复杂JSON数据的校验工作。

以下是上面出现过的配置项的含义：
* `type`: 规定值的类型
* `required`: 规定object下哪些键是必须的
* `properties`: 规定object下键的格式
* `const`: @since draft-07，常量，值必须等于该常量
* `enum`: 枚举值，即值只能是enum数组中的某一项
* `maxLength`: 规定字符串的最大长度
* `maximum`: 规定数字的最大值
* `minimum`: 规定数字的最小值
* `minItems`: 规定数组元素的最少个数

怎么样，是不是觉得非常简单？下一节是可用的配置项信息，可以结合自己的实际需要来编写配置

## 配置项
因最新草案(draft-07)的支持尚不够广泛，本文的配置项以旧版(draft-04)为准
### 通用配置
* `type`: string/array, 规定值的类型只能从6个基础类型中选择：number/integer, string, object, array, boolean, null
* `enum`: array, 规定值必须等于该枚举数组中的某一项

### number/integer
`number`和`integer`作为共享关键字，不得同时出现。两者分别表示数字和整形
* `multipleOf`: number, 规定值必须为该项的倍数
* `maximum`: number, 规定值必须小于等于该项
* `exclusiveMaximum`: boolean, 如果出现该项且不为`false`，那么值就必须小于`maximum`
* `minimum`: number, 规定值必须大于等于该项
* `exclusiveMinimum`: boolean, 如果出现该项且不为`false`，那么值就必须大于`minimum`

### string
* `maxLength`: integer, 规定值的长度必须小于等于该项
* `minLength`: integer, 规定值的长度必须大于等于该项
* `pattern`: string, 正则表达式，规定值必须匹配该项

### object
* `maxProperties`: integer, 规定值所包含的键值个数必须小于等于该项
* `minProperties`: integer, 规定值所包含的键值个数必须大于等于该项
* `required`: array, 规定哪些键必须出现
* `properties`: object, 该项的键为值中可能出现的键，该项的值为有效的schema数据。参考上一节的例子
* `patternProperties`: object, 该项的键为正则表达式，用以匹配可能出现键，该项的值为有效的schema数据  

    __Example__:
    ```js
    // JSON Schema
    {
        "type": "object",
        "patternProperties": {
            "^interest": {
                "type": "string"
            }
        }
    }
    // json 1: pass
    {
        "interesting": "too young too simple",
        "interested": "sometimes naive"
    }
    // json 2: fail, -1 is not type of string
    {
        "interesting": "苟利国家生死以，岂因祸福避趋之",
        "interested": -1
    }
    ```
* `additionalProperties`: boolean/object, 该项比较复杂
    1. 如果出现该项且为false, 那么当对象所有的键经过properties和patternProperties匹配后仍有剩余的，即出错；
    2. 如果该项为object，那么其中定义了经过properties和patternProperties匹配后剩余的键的特性

    __Example__:
    ```js
    // JSON schema
    {
        "type": "object",
        "properties": {
            "Thor": {
                "type": "string"
            }
        },
        "patternProperties": {
            "man$": {
                "type": "string"
            }
        },
        "additionalProperties": false
    }
    // json 1: success
    {
        "Thor": "King of Asthad",
        "ironman": "King of money",
        "spiderman": "pooy guy",
    }
    // json 2: fail, 'Hulk' does not match any of the regexes: 'man$'
    {
        "Thor": "King of Asthad",
        "ironman": "King of money",
        "spiderman": "pooy guy",
        "Hulk": "stronger, faster, greener"
    }
    ```
* `dependencies`: object, 如果出现了某个键则其依赖的键也必须出现
    1. 属性依赖， 则`dependencies`中每个键的值为array，数组的元素该键的依赖 

    __Example__:
    ```js
    // 如果'梁山伯'出现的话，那么'祝英台'也必须出现
    {
        "type": "object",
        "properties": {
            "梁山伯": {},
            "祝英台": {},
        },
        "dependencies": {
            "梁山伯": ["祝英台"],
        }
    }
    ```
    2. schema依赖，则`dependencies`中每个键的值为object，该对象中通过`properties`指定其依赖的键  

    __Example__:
    ```js
    // 同上例效果相同
    {
        "type": "object",
        "properties": {
            "梁山伯": {},
        },
        "dependencies": {
            "梁山伯": {
                "properties": {
                    "祝英台": {}
                }
            },
        }
    }
    ```

### array
* `items`: 规定每个元素的特性
    1. object, 一个有效的schema，对所有数据的元素应用该校验方式  

    __Example__:
    ```js
    // 数组的每一项都必须是string类型
    {
        "type": "array",
        "items": {
            "type": "string"
        }
    }
    ```

    2. array，每个元素均为一个有效的schema，用一一对应的方式对数组中的元素进行校验  

    __Example__:
    ```js
    // 数据元素与对应schema一一进行校验
    {
        "type": "array",
        "items": [
            {"type": "string"},
            {"type": "number"},
            {"type": "boolean"}
        ]
    }
    // pass: 依次出现string, number和boolean类型的数据
    ['david', 22, true]
    // pass: 数据不足也可以
    ['eason', 1984]
    // pass: 提供额外的数据
    ['jj', 89757, false, 'boom']
    // fail: 前三项任意格式不匹配
    [1998, 2011, true]
    ```
* `additionalItems`: boolean, 如果出现该项且为`false`，那么`items`中值为array的情况下，对应数据中不可出现额外的项  

    __Example__:
    ```js
    // 上例相同
    {
        "type": "array",
        "items": [
            {"type": "string"},
            {"type": "number"},
            {"type": "boolean"}
        ],
        "additionalItems": false
    }
    // pass: 依次出现string, number和boolean类型的数据
    ['david', 22, true]
    // pass: 数据不足也可以
    ['eason', 1984]
    // fail: 提供额外的数据
    ['jj', 89757, false, 'boom']
    // fail: 前三项任意格式不匹配
    [1998, 2011, true]
    ```
* `maxItems`: integer, 规定元素个数必须小于等于该项
* `minItems`: integer，规定元素个数必须大于等于该项
* `uniqueItems`: boolean, 如果出现该项且为`true`，那么数组中的每个元素都不能相同

### boolean
无单独配置项

### null
无单独配置项

## 小结
有了JSON Schema这个神器，接口测试的数据校验变得简单了不少，作为接口监控脚本的一部分，也很容易知道结果中哪部分出了问题。实在是居家旅行、测试开发，必备良药。

如果本文对你有用，欢迎收藏点赞。点赞过10，后续会考虑再出一篇关于JSON Schema高级特性的介绍。

## 参考
1. json schema: [http://json-schema.org](http://json-schema.org)
2. Understanding Json Schema: [https://spacetelescope.github.io/understanding-json-schema/index.html](https://spacetelescope.github.io/understanding-json-schema/index.html)
3. JSON Schema: interactive and non interactive validation (draft-fge-json-schema-validation-00): [https://tools.ietf.org/html/draft-fge-json-schema-validation-00](https://tools.ietf.org/html/draft-fge-json-schema-validation-00)