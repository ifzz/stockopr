import config.config as config

def almost_equal(m, n, almost=config.ALMOST_EQUAL):
    l = m
    if m > n:
        l = n
    if abs(m - n) * 100 / l < almost:
        return True
    return False

def gen_ma(quote, n=config.MA_NUM, l=config.MAS):
    r = []
    for i in range(n):
        r.append(ma(quote, l[i]))

    return r



