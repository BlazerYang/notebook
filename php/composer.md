# composer

## 如何改变依赖的安装位置？
默认安装位置为`./vendor`, 可以通过在composer.json中添加如下语句调整
```json
{
  "config": {
    "vendor-dir": "./ThinkPHP/Library/Vendor"
  }
}
```

## 如何在ThinkPHP中可以直接use composer安装的依赖？
在`index.php`中引入composer的autoloader, 注意要放在Thinkphp的autoloader之前：
```php
require('./ThinkPHP/Library/Vendor/autoloader.php');
```