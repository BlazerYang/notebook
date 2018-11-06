#unclassified

## 利用mysql自动记录时间？
以下是代码片段：
自动初始化和更新:
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
只自动初始化:
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
只自动更新
ts TIMESTAMP DEFAULT 0 ON UPDATE CURRENT_TIMESTAMP
只是给一个常量（注：0000-00-00 00:00:00）
ts TIMESTAMP DEFAULT 0 

## ts timestamp not null default '0000-00-00 00:00:00' invalid default value?
STRICT MODE下默认会有NO_ZERO_DATE选项，在my.ini文件中使用sql_mode=''予以清除

## 使用source iw.sql导入的文件中文均为乱码？
1. 导出sql文件的时候需要指定字符编码
```
mysqldump -uroot -p --default-character-set=utf8 dbname > E://xxxx.sql
```
2. 使用cli登陆的时候指定字符编码
```
mysql -uroot --default-character-set=utf8 dbname
source iw.sql
```

## double类型添加unsigned约束？
不可以，这样的话该字段类型会变成unsigned int型

## 如何在mysql中取出第一四分位数、中位数和第三四分位数？
做不到

## mysql模糊group

## 6303 ERR: 1267:Illegal mix of collations (gb2312_chinese_ci,IMPLICIT) and (utf8_general_ci,COERCIBLE) for operation '='
采用字符集进行排序的列无法混合，这是前期建表时没有统一字符编码留下的隐患，可以通过统一所有表的编码方式解决
```sql
ALTER TABLE tablename COLLATE utf8_general_ci
```
该语句同时会将表的默认字符集(DEFAULT CHARACTER)设置为utf8

### utf8_general_ci中的ci是什么？
utf8_general_ci: case insensitive，大小写不敏感，相似地还有
utf8_general_cs: case sensitive, 大小写敏感
utf8_bin: binary, 二进制，每个字符使用二进制存储，区分大小写。因为cs经常没有，一般使用utf8_bin来区分大小写

## alter table tablename engine=innodb 报错 'Table storage engine for '#sql-168c_5e' doesn't have this option'?
建表时使用了引擎为MYISAM同时用了某些INNODB不支持的特性就会报这个错误，将ROW_FORMAT由FIXED调整为DEFAULT

## mysql的rollback没有生效？
引擎使用INNODB，MYISAM不支持事务

## myisam为什么不支持事务处理？
myisam工作在自动提交模式，会忽略会话中的commit/rollback指令. [MyIsam engine transaction support
](https://stackoverflow.com/questions/8036005/myisam-engine-transaction-support)

## 添加ip白名单
GRANT ALL PRIVILEGES ON *.* TO 'username'@'host' IDENTIFIED BY 'password' WITH GRANT OPTION;

## 联合索引
联合索引又叫复合索引, 形如`index index_name (user_id, project_id)`
1. 需要加索引的字段，要在where条件中
2. 数据量少的字段不需要加索引
3. 如果where条件中是OR关系，加索引不起作用
4. 符合最左原则

### 

### 为什么where中or不会走索引？

## 为什么text会影响表中其他字段的索引效率？
1. 非定长字段在mysql查询时，因为偏移量不固定，每次都需要获取主键才能找到下一条

那么就可以利用垂直分表，将表分为定长字段和非定长字段以提高查询性能。前提是分表之间不需要join，否则性能比不分还要差


## 为什么varchar建立索引要指定索引长度？
1. 在区分度足够的情况下，速度不会比全文索引慢很多
2. 索引占用磁盘空间会小很多
3. insert性能会高很多

## 页面搜索中的左模糊和全模糊是什么？
1. 左模糊：like '%needle'
2. 全模糊：like '%needle%'

## 什么是索引的有序性？

## 什么是file_sort？

## 为什么select * 不使用索引？

## explain指令？

### explain 中的extra是什么？using index又是什么意思？


### 什么是覆盖索引？
覆盖索引（covering index）指一个查询语句的执行只用从索引中就能够取得，不必从数据表中读取
[覆盖索引](https://www.jianshu.com/p/77eaad62f974)
explain的extra中出现using index即为使用了覆盖索引

## 什么是普通索引(normal index)?
使用`index`关键字声明的索引，最普通，没有任何限制

## 什么是延迟关联？什么是子查询优化？


## 什么是NPE问题？
Null Pointer Exception, 空指针异常

## 级联更新
<https://www.cnblogs.com/panxuejun/p/5975741.html>

## 存储过程
为什么要避免in操作


## 如何在排序情况下查询某个节点的相邻节点
法1：来自stackoverflow的解决方案，one query stand
```sql
SELECT
	t1.id,
	t1.
FROM
	,
	t1. TO
FROM
	(
		SELECT
			*, @rn1 := @rn1 + 1 AS row_num
		FROM
			t
		CROSS JOIN (SELECT @rn1 := 0) p1
	) t1
CROSS JOIN (
	SELECT
		@target := (
			SELECT
				t2.row_num
			FROM
				(
					SELECT
						*, @rn2 := @rn2 + 1 AS row_num
					FROM
						t
					CROSS JOIN (SELECT @rn2 := 0) p2
				) t2
			WHERE
				t2.id = 1053
		)
) p3
WHERE
	t1.row_num IN (
		@target - 1,
		@target,
		@target + 1
	);
```
法2：将结果全部查询出来之后再遍历


## 为什么相同的sql语句在相同的表结构中执行的默认顺序不同？
该表中存在UNIQUE索引(UNIQUE (user_id, category, name))，一个查询会用UNIQUE中的user_id索引，但另一个却是全表扫，为什么？

## 如果将一个表中查询出来的结果插入另一个表？
注意此时子查询之前不要使用`VALUES`, 不然会报错
```sql
INSERT INTO tb_field_visibility (
	`name`,
	`mask`,
	`category`,
	`type`,
	`prev`,
	`next`,
	`visible`,
	`sort`,
	`user_id`
)(
	SELECT
		`name`,
		`mask`,
		`category`,
		`type`,
		0,
		0,
		0,
		`sort`,
		`user_id`
	FROM
		tb_field_default_visibility
	JOIN (
		SELECT
			user_id
		FROM
			tb_field_visibility
		WHERE
			category = 'manage_project'
		GROUP BY
			user_id
	) AS u
	WHERE
		id IN (55, 56, 57)
);

```

## 如何修改一个表及其中所有字段的编码格式？
`ALTER TABLE tablename CONVERT TO CHARACTER SET utf8`,