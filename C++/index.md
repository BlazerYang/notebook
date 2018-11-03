# index

## \#ifndef
如果宏未定义则会进入分支，主要用防止头文件的重复包含和编译

## \#define

## error LNK2019: 无法解析的外部符号
1. 可能是只找到了函数声明而没有找到函数实现，把函数实现文件也一并引入即可

## c++为什么要将声明（.h）和实现(.cpp)分开？
1. 声明等于是函数说明，用户只需要阅读声明即可知道怎么用它
2. 声明等于是接口声明，具体实现只要在满足接口不变的情况下可以自由重构
3. 编译器工作时需要的是声明部分而不是实现部分，比如：
    1. 变量类型
    2. 方法参数列表、参数类型和返回值
    3. 类的框架，即其成员变量和方法

## \#include "" 和 <>的区别？
* <>是C++自带的库文件，编译时，c++会去vc++的include文件中去查找，如果使用该方式包含自定义的文件则会报错
* ""会先在文件所在目录进行搜索，如果没有的话再去include文件夹里面找，因此无论该文件是自己编写还是vc++提供，该方式一般不会出错，这就是为什么有的地方要求一定要用该方式的原因。

## const int*, const int * const, and int const * 
1. int* - pointer to int
2. int const * - pointer to const int
3. int * const - const pointer to int
4. int const * const - const pointer to const int
其中const和int的位置可以互换
1. const int * == int const *
2. const int * const == int const * const
```c++
const int * foo;
// you need to set this pointer, cuz you cannot change it anymore
int * const bar;
```
`foo` is a pointer to const int, which pointer can be changed to what you want to point to, but not the value can not be;
`bar` is a const pointer to a value that can be changed, but the pointer cannot be changed
[https://stackoverflow.com/questions/1143262/what-is-the-difference-between-const-int-const-int-const-and-int-const](https://stackoverflow.com/questions/1143262/what-is-the-difference-between-const-int-const-int-const-and-int-const)

## c++ reference
c++引用是变量别名。它与指针比较像，主要有以下不同：
* 不存在空引用
* 引用一旦初始化就不可指向其他变量
* 引用必须在创建时初始化
使用方式
```c++
int i = 1;
int& r = i;
```

## main函数的int argc, char* argv[]是什么？
用于命令行调用时传入参数，其中argc意味arguments count，即参数数量；argv意味arguments value/vector，即参数值。其中argv[0]为程序运行的全路径名，argv[1]为程序名后的第一个字符串，依次类推

## what is const last in c++ method mean?
* const是函数签名的一部分，意思是你可以实现两个版本，调用const对象的方法会调用带const的，而非const对象的方法会调用没用const的
```cpp
#include <iostream>

class MyClass
{
private:
    int counter;
public:
    void Foo()
    { 
        std::cout << "Foo" << std::endl;    
    }

    void Foo() const
    {
        std::cout << "Foo const" << std::endl;
    }

};

int main() {
    MyClass cc;
    const MyClass& ccc = cc;
    cc.Foo(); // Foo
    ccc.Foo(); // Foo const
    return 0;
}
```
* 变量只能在在非const中使用，而const无法使用（除非使用mutable声明）
```c++
    void Foo()
    {
        counter++; //this works
        std::cout << "Foo" << std::endl;    
    }

    void Foo() const
    {
        counter++; //this will not compile
        std::cout << "Foo const" << std::endl;
    }
```
[https://stackoverflow.com/questions/751681/meaning-of-const-last-in-a-c-method-declaration](https://stackoverflow.com/questions/751681/meaning-of-const-last-in-a-c-method-declaration)

## what is "= 0" mean last in virtual method?
在普通虚函数后面加上"= 0"可以将其声明为纯虚函数

### 什么是虚函数？
使用virual关键字声明的方法，主要用于实现多态和多重继承

### 什么是纯虚函数？
定义见上。包含纯虚函数的类是无法被实例化的（编译时会报错），而如果通过删除虚函数实现的方式阻止类被实例化的方式只能在link时报错

## 友元函数？
函数定义在类的外部，但是可以访问函数内部的元素，使用friend关键字修饰，相似地还有友元类。

## 重载运算符？
相同函数名、不同参数或返回值的即为重载

## string

### string.c_str()
返回指向该字符串的的char指针

## fcntl.h
file control options
* O_CREAT, create file if not exist
* O_RDWT, open for reading and writing


## int64_t 和 int的区别
在32位和64位系统中，long类型占用空间分别为4字节和8字节，为了屏蔽平台差异，使用固定大小的数据类型宏定义
使用int64_t声明的变量统一占8字节
```cpp
typedef signed char       int8_t

typedef short int             int16_t;

typedef int                      int32_t;

#if __WORDSIZE == 64
typedef long int              int64_t;
#else
typedef long long int      int64_t;
#endif
```

## 成员函数末尾加上const是什么意思？
如下
```cpp
class Rectangle{
    private:
        std::string name;
        Sharp sharp;

    public:
        void initial(void);
        // tail const
        const Sharp getSharp() const;
        static void onEvent(int param){  //---------------(1)
            std::cout << "invode onEvent method,get parameter: " << param << std::endl;
        }

};
```
意思为该函数是只读方法，不会改变类的数据成员。
* 提高程序可读性
* 企图修改数据成员时会直接抛出编译错误
