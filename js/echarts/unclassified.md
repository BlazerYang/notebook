# unclassified

## 如何在服务端生成echarts图片并保存？
并无直接方式，有苟且的方法
法1：
  浏览器创建图，然后getDataUrl()获取图片base64数据，再post回后端
法2：
  利用phantomjs生成图片并保存
  1. 准备一个空白html引入echarts文件
  2. 启动一个server提供对该html的访问，http-server
  3. phantomjs访问该url并生成图片
