# index

## vscode如何在终端中使用git bash?
在 文件->首选项->设置 中添加如下设置,找到本机Git\bin\bash.exe路径填进去即可
```json
{
    "terminal.integrated.shell.windows": "C:\\Program Files\\Git\\bin\\bash.exe"
}
```

## 如何隐藏指定后缀的文件？
在 文件->首选项->设置 中添加如下设置即可:
```json
{
    "file.exclude": {
        "**/*.pyc": true,

    }
}
```

## 如何隐藏相同文件名指定后缀的文件？
```json
{
  "files.exclude": {
      "**/*.pyc": { "when": "$(basename).py"}
  }
}
```

## 如何在window邮件菜单中添加“open in vs code”?
1. 新建文件,粘贴如下指令:  
前两个注册表意思为在空白处右键菜单中添加  
后两个注册表意思为在文件夹邮件菜单中添加  
```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\Background\shell\VSCode]
@="Open VSCode Here"
"Icon"="C:\\Program Files\\Microsoft VS Code\\Code.exe"

[HKEY_CLASSES_ROOT\Directory\Background\shell\VSCode\command]
@="C:\\Program Files\\Microsoft VS Code\\Code.exe ."

[HKEY_CLASSES_ROOT\Directory\shell\VSCode]
@="Open VSCode Here"
"Icon"="C:\\Program Files\\Microsoft VS Code\\Code.exe"

[HKEY_CLASSES_ROOT\Directory\shell\VSCode\command]
@="C:\\Program Files\\Microsoft VS Code\\Code.exe %1"
```
2. 保存为.reg文件，双击运行即可


## vscode中terminal使用Git bash，运行php查询数据并打印结果，中文为乱码？
1. 确定数据库、表和字段编码均为utf8
2. 确定数据库连接编码为utf8： 
    ```php
    $conn = new mysqli();
    $conn->query('set names utf8');
    ```
3. 确定LANG为zh_CN.UTF-8: `echo $LANG`
4. 确定windows活动代码页为65001: 
    ```bash
    # 查看当前活动代码页，结果为936, 也就是gb2312
    chcp
    # 修改活动代码页为65001, 也就是utf-8
    chcp 65001
    # git bash中需要加上.com
    chcp.com 65001
    # 屏蔽输出
    chcp.com 65001 > /dev/null
    ```

* 附:常见的活动代码页：
    1. 850： latin1
    2. 936: gb2312
    3. 950: 繁体中文(big5)
    4. 1200: Unicode
    5. 1201: Unicode(big endian)
    6. 650001: UTF-8