# index

## broker?
kafka集群中的每一台机器就是一个broker

## topic？
发送到kafka的消息都有一个类别，即topic。物理上不同topic内容分开存储，同一个topic也可能存在不同partition上；逻辑上用户只需指定topic进行使用即可

## partition？
一个topic包含一到多个partition，物理上每个partition对应一个文件夹

## producer？
向broker发送消息

## consumer？
从broker读取消息

## consumer group?
每个consumer都属于一个group，没有指定的则属于默认group

## commit offset？
consumer group从partition读取过信息后会将信息对应的offset存储到zookeeper中，该数值是对应consumer group来存储的（以此实现消息的多播）