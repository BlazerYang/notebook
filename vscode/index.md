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