# cmd

## cmd显示中文乱码？
Windows NT出现了（Windows NT就是Windows XP和Windows 7的老祖宗），为了确保不同语言间的兼容性，它使用Unicode存储字符串（Unicode就是万国码，你可以认为它可以编码世界上所有的文字），可是当时大量程序使用本地编码（例如大陆的GB2312编码简体中文（GBK可以使用繁体），台湾的Big5编码繁体中文（其实也可以简体），美国的ISO8859-1只能编码英文和有限的欧洲文字），这样为了兼容性它也支持本地编码，但是系统内核是需要Unicode的，所以就发明了“代码页”这个中介，用来转换本地编码和Unicode  
`chcp`查看或设置活动代码页
936是gbk
65001是utf8

## powershell显示中文乱码？
`$outputEncoding` 可以显示当时输出编码格式  
`$OutputEncoding = New-Object -typename System.Text.UTF8Encoding` 可以修改编码格式

## unix tail equivalent in windows powershell
```bash
# get-content in utf-8 and refresh as content append
get-content filePath -encoding utf8 -wait
```

## window中类似grep的指令？
findstr

## window下如何像linux一样后台启动？

