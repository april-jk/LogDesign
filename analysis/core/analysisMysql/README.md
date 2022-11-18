
开启logbin
========

使用MySQL的日志记录功能，首先要确定是否开启了logbin，mysq命令：

    show variables like '%log_bin%' 
结果：
Variable|value
---|:--|
log_bin|	ON
sql_log_bin	|ON
log_bin_basename|C:\ProgramData\MySQL\MySQL Server 5.7\Data\mysql-log  
log_bin_index	|C:\ProgramData\MySQL\MySQL Server 5.7\Data\mysql-log.index


**怎么开启？**

如果没有开启需要修改my.ini文件，至于这个文件在哪，Linux当然使用whereis,
Window的话，还是MySQL命令：
    show variables like '%data%' 
结果：
Variable|value
---|:--|
datadir|	C:\ProgramData\MySQL\MySQL Server 5.7\Data\

就在这个目录的父目录下。

**怎么修改？**

log-bin=mysql-log
    # Binary Logging.
    # log-bin
    log-bin=mysql-log
等号后面随便取，这将会是你的日志文件名，如我所取mysql-log

**重启服务器**

重启之后操作一番增删改后，可以看到日志文件，目录就在`show variables like '%data%'`显示的 datadir指向的文件夹里
    文件名为你刚刚设置的名字加00000加数字的二进制文件
    如：mysql-log.000001
这就是MySQL的日志文件。

**针对日志文件show一波命令**

---|:--|
 flush logs |	至此生成新的日志文件
reset master| 清空日志文件


听说在此之前需要保证两个设置是对的

 1. 存储引擎：InnoDB
 2. 日志格式：ROW
由于我的MySQL默认都是对的，我就没有测试，就简单介绍一下吧：

查看存储引擎
    show engines;
查看日志格式
    show variables like '%binlog_format%';
    

mysqlog
=======
**怎么阅读日志文件？**

>下面开始画重点，这也是我写这篇文章的重要目的
既然日志文件是二进制，怎么使用呢，感兴趣的小伙伴可以了解一下**`mysqlbinlog`命令**，这里不做重点；
重点是我写的一个小工具，使用简单，操作流畅，令人心旷神怡。

**功能介绍：**根据MySQL二进制日志文件，生成人类可以理解的操作记录文件，以excel人性化呈现；
而你只需要提供二进制文件以及数据库ip、用户名、和密码即可
项目使用python3开发，所以你电脑要安装python；


**使用步骤：**

 1. /log0000/文件夹内放你要解析的二进制日志文件
 2. 在main.py文件中填入config配置（数据库ip、用户名、和密码）
 3. 运行主方法，在/result/文件下可得到解析结果。
 

