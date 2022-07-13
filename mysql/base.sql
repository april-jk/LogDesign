-- LogAudit_admin存终端信息和认证码
CREATE DATABASE `LogAudit_admin`;
-- LogAudit_log做全日志存储，根据终端的新增创建新表，创建语句和数据添加都在后端实现
CREATE DATABASE `LogAudit_log`;
-- LogAudit_Ana存放分析平台分析后的数据，也是根据终端创建表
CREATE DATABASE `LogAudit_Ana`;

CREATE TABLE `LogAudit_admin`.`client_code`(
		`client_id` VARCHAR(20) NOT NULL,
		`clent_type` VARCHAR(10) NOT NULL,
		`clent_nickname` VARCHAR(20),
		`verify_code` VARCHAR(32),
		PRIMARY KEY(`client_id`)
)ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `LogAudit_admin`.`admin`(
		`uid` INTEGER NOT NULL,
		`realname` VARCHAR(20),
		`tel` VARCHAR(20),
		`uname` VARCHAR(20) NOT NULL,
		`passwd` VARCHAR(40) NOT NULL,
		`authority` VARCHAR(2) NOT NULL,
		`enable` VARCHAR(2),
		 PRIMARY KEY(`uid`)
)ENGINE=INNODB DEFAULT CHARSET=UTF8;






