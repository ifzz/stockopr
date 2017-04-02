# Stock Operator
--Stock Investment Suite

1 数据
    基本信息 行情信息
2 选股
    自定义选股策略
3 监控
    实时监控
    自定义策略
4 交易
    自动交易
5 账户
    交易分析

## 概述
* 通过历史数据洞察规律, 华尔街没有新鲜事
* 通过软件系统替代人工分析和人工操作, 杜绝人性弱点
* 通过成交分析, 实现系统自我完善

## 运行环境
* 交易处理器运行环境为Windows 10, python3.5
* 其他功能运行环境为Fedora 25, python3.5

## 软件结构
1 control center
2 instruction server
3 scheduler/distributor


bootstrap

### 0 microservices
微服务
错误收集处理, 各微服务运行出现异常后将异常发送给错误处理模块
日志模块

### 1 data acquisition unit/system - acquisition/tushare
* 描述: 采集行情数据
* 类型: 周期任务(每天下午18:00)
* 错误处理:
* 流程: 从[腾讯财经]下载当日行情信息xls文件, 如2017-03-31-15-31_ranka.xls, 解析xls文件, 行情数据存储到mysql数据库quote表
* 开发优先级: 先以工具的形式使用, 使用crontab定期执行

### 2 selector
* 描述: 执行选股策略, 策略为自定义
* 类型: 周期任务/人工触发(每周五下午19:00)
* 错误处理
* 开发优先级: 先以工具的形式使用, 使用crontab定期执行

### 3 point monitor
* 描述: 自选股监控, 识别交易时机, 发送交易信号
* 类型: 周期任务(每个交易日上午9:00)
* 错误处理: 告警
* 开发优先级: 高

### 4 dealer
* 描述: 接收交易命令, 执行或拒绝命令, 仓位管理, 发送交易指令, 所有交易行为的执行者, 形成一道屏障, 防止人性犯错
* 类型: 条件触发/人工触发
* 错误处理:
* 开发优先级: 高

### 5 instruction processor # 不作为微服务
* 描述: 执行交易指令
* 类型: 被dealer调用
* 错误处理:
* 开发优先级: 高

### 6 transaction analyzer
* 成交分析

### 7 insight
* 洞察规律, 以形成选股策略, 洞察规律, 以形成交易策略

## toolkit
### 历史数据入库
* 描述: 将所有历史数据存储到数据库

