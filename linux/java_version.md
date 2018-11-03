# why java version is 1.7 rather than 1.8

## steps
```
[cloud@test42 /da2/huangying/jmeter3.0/sh]$ java -version
java version "1.7.0_09"
Java(TM) SE Runtime Environment (build 1.7.0_09-b05)
Java HotSpot(TM) 64-Bit Server VM (build 23.5-b02, mixed mode)

[cloud@test42 /da2/huangying/jmeter3.0/sh]$ which java
/da2/luting/video/jmeter3.0/jdk/bin/java

[cloud@test42 /da2/huangying/jmeter3.0/sh]$ echo $PATH
/da2/luting/jdk//bin:/sbin:/usr/sbin:/usr/local/sbin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin::/home/s/ops/pantheon/tools:/usr/local/bin:/usr/local/sbin:/da2/luting/video/jmeter3.0/jdk/bin:/da2/luting/video/jmeter3.0/jdk/jre/bin:/home/cloud/bin

[cloud@test42 /da2/huangying/jmeter3.0/sh]$ export PATH=/sbin:/usr/sbin:/usr/local/sbin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/da2/cloud/software/java/jdk/bin

[cloud@test42 /da2/huangying/jmeter3.0/sh]$ java -version
java version "1.8.0_161"
Java(TM) SE Runtime Environment (build 1.8.0_161-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.161-b12, mixed mode)
```