grant all on *.* to kylin@localhost identified by 'xxxxxx' with grant option;

-- 如下脚本创建数据库yourdbname，并制定默认的字符集是utf8。
-- CREATE DATABASE IF NOT EXISTS yourdbname DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
-- 如果要创建默认gbk字符集的数据库可以用下面的sql:
-- create database yourdb DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci;
-- create database stock default charset utf8;

create database if not exists stock default charset utf8;
use stock;

-- 与股价挂钩的指标，就不记录历史数据了
-- 基本信息，代码，名称，市盈率，市净率，板块，概念，
-- 板块使用id
create table if not exists basic_info(code varchar(8), name varchar(16), `type` varchar(8) default 'A股');
CREATE TABLE future_variety (code varchar(8), name varchar(8), type varchar(8), prev_dc varchar(8), curr_dc varchar(8), next_dc varchar(8));

-- 日期 开盘价 最高价 最低价 收盘价 成交量(手) 成交金额(万元)
-- 昨收 涨跌额 涨跌幅(%) 振幅(%) 换手率(%) 量比
create table if not exists quote (code varchar(8), trade_date date, open float, high float, low float, close float, volume bigint, turnover bigint);

-- 建仓
create table selected(code varchar(8), added_date date, class varchar(8), rank integer);
create table selected_history(code varchar(8), added_date date, class varchar(8), rank integer);
-- 交易记录
create table trade_detail (code varchar(8), trade_date date, op varchar(8), price float, count integer, account varchar(16));
create table trade_detail_history (code varchar(8), trade_date date, op varchar(8), price float, count integer, account varchar(16));

-- 业务逻辑
-- 监控
create table bought (code varchar(8), date date);
-- 平仓
create table cleared (code varchar(8), date date);

-- 账户
-- op: i o s b a(adjust)
create table account_detail (code varchar(16), trade_date date, op varchar(8), price float, count integer);


-- 索引
create unique index basic_info_code on basic_info(code);

create index quote_code on quote(code);
create index quote_trade_date on quote(trade_date);
create unique index quote_code_trade_date on quote(code,trade_date);

-- mysql> insert into history_price (code, trade_day) values("600839","2015-12-25"); --date 可以这样插入
-- ERROR 1062 (23000): Duplicate entry '600839-2015-12-25' for key 'history_price_code_trade_day'



-- current_date() CURRENT_TIMESTAMP, all is ok
