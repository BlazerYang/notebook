# anyproxy

## anyproxy --type https?
该指令不是开启拦截https请求，而是对所有发往代理服务器的请求进行加密，即代理服务器本身是一个https服务器

## anyproxy中https的req中的数据格式为何不一致？
anyproxy继承后又覆盖了一部分数据

## anyproxy -g启动后没有关闭全局代理接口，需要在注册表中进行修改
1. `win`+`r`，输入`regedit`并打开
2. 找到`计算机\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings`
3. 清空`proxyEnable`和`proxyServer`即可