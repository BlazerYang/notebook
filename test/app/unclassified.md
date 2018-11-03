# unclassified

## 为什么使用真机进行测试，而不用安卓或ios虚拟机呢？
有些问题在虚拟机下不会出现

## 小米手机连接usb并打开usb调试后使用adb devices无法发现设备？
解决办法
1. 拨号界面输入 **\*\#\*\#717717\#\*\#\***
2. 在~/.andorid/目录下找到adb_usb.ini文件(没有则创建)
3. 添加'0x2717'（小米的VenderID）
4. 重启adb server
```bash
adb kill-server
abd devices
```

## how to get phone's vender id?
```bash
lsusb
# Example
# Bus 001 Device 057: ID 18d1:d002 Google Inc.
# 18d1 above is vender id
```

## \*\#\*\#717717\#\*\#\*这串神秘数字是啥？
小米手机打开调试的指令