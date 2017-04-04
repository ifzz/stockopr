create table if not exists quote (
    code varchar(8),
    trade_date timestamp,
    close float,
    high float,
    low float,
    open float,
    yestclose float,
    updown float,
    percent float,
    hs float,
    volume bigint,
    turnover bigint,
    tcap bigint,
    mcap bigint,
    lb float,
    wb float,
    zf float,
    five_minute float
    );


create index quote_code on quote(code);
create index quote_trade_date on quote(trade_date);
create unique index quote_code_trade_date on quote(code,trade_date);

