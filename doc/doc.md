
1, http://stock.gtimg.cn/data/get_hs_xls.php?id=ranka&type=1&metric=chr
create database if not exists stock default charset utf8;
create table if not exists basic_info(code varchar(8), name varchar(16), type varchar(8)) default 'A股';
create index

python3 history/get_all_stock_list.py ./2016-11-28-08-02_ranka.xls

2, python3 history/dl_history.py
create table if not exists quote (code varchar(8), trade_date date, open float, high float, low float, close float, volume bigint, turnover bigint);

create unique index basic_info_code on basic_info(code);
create index quote_code on quote(code);
create index quote_trade_date on quote(trade_date);
create unique index quote_code_trade_date on quote(code,trade_date);

create table selected(code varchar(8), added_date date, class varchar(8), rank integer);
create table selected_history(code varchar(8), added_date date, class varchar(8), rank integer);

CREATE TABLE `tick` (
  `code` varchar(8),
  `time` varchar(63) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `pchange` varchar(63) DEFAULT NULL,
  `change` double DEFAULT NULL,
  `volume` bigint(20) DEFAULT NULL,
  `amount` bigint(20) DEFAULT NULL,
  `type` varchar(63) DEFAULT NULL
)


# 成交明细
http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=sh600050&d=20161222

http://stockhtm.finance.qq.com/sstock/ggcx/300152.shtml
