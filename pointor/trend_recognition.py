#-*- encoding: utf-8 -*-

import pointor.stage_handler as stage_handler
from config.config import debug
from config import config

'''
策略: 只吃鱼中, 不吃鱼头, 不吃鱼尾
忽略极端走势: 354, 423, 发送警告信息即可
'''

# 逆转信号 -> 突破之后转换为 3/4

# 转向 逆转 突破 异动
indicator = {
        'zx_up'   : config.TR_ZX,
        'lz_up'   : config.TR_LZ,
        'tp_up'   : config.TR_TP,
        'zx_down' : -1*config.TR_ZX,
        'lz_down' : -1*config.TR_LZ,
        'tp_down' : -1*config.TR_TP
        }

def notice_signal_transfer(stock_info):
    return
    # 查询数据库, 是否建仓
    if debug or stock_info['bought'] == 1:
        pass
        #engine.say(stock_info['name'] + '注意, 逆转信号')
        #engine.runAndWait()

def percent(orig, curr):
    return 100 * (curr - orig)/orig

'''
时间 + 价格
'''
#class StockTrendRecognizerInfo:
#    def __init__(self, code, quote=None):
#        self.code     = code
#        self.quote    = quote
#        self.quote_rt = []
#        self.stagehandler    = stage_handler.Stage()
#        self.stagehandler.tr = self # 彼此引用
#        self.close  = -1
#        self.last   = -1
#        self.dt     = '' # datetime
#        self.ind    = -1
#        self.flag   = -1 # 1, update

class TrendRecognizer:
    def __init__(self, code, quote=None):
        self.code     = code
        self.quote    = quote
        self.quote_rt = []
        self.stagehandler    = stage_handler.Stage()
        self.stagehandler.tr = self # 彼此引用
        self.close  = -1
        self.last   = -1
        self.dt     = '' # datetime
        self.ind    = -1
        self.flag   = -1 # 1, update

        self.stage_dict = {
                '3'      : self._3,
                '35'     : self._35,
                '354'    : self._354,
                '352'    : self._352,
                '3523'   : self._3523,
                '3526'   : self._3526,
                '35264'  : self._35264,
                '35261'  : self._35261,
                '352613' : self._35261,
                '352614' : self._352614,
                '4'      : self._4,
                '42'     : self._42,
                '423'    : self._423,
                '425'    : self._425,
                '4254'   : self._4254,
                '4251'   : self._4251,
                '42513'  : self._42513,
                '42516'  : self._42516,
                '425164' : self._425164,
                '425163' : self._425163
                }

    #目前处于上升趋势
    def _3(self):
        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        if self.close >= self.last:
            if self.close > mm['max']:
                self.stagehandler.set_stage_info(cur_stage, mm['min'], self.close)
        else:
            if percent(mm['max'], self.close) <= indicator['zx_down']:
                self.stagehandler.chg_stage('35', self.close, mm['max'])

    #目前处于上升趋势->自然回辙
    def _35(self):
        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        if self.close >= self.last:
            if percent(mm['min'], self.close) >= indicator['zx_up']:
                self.stagehandler.chg_stage('352', mm['min'], self.close)
        else:
            #if percent(mm['max'], self.close) <= indicator['zx_down'] + indicator['lz_down']:
            #    self.stagehandler.chg_stage('4', self.close, mm['max'])
            #elif self.close < mm['min']:
            if self.close < mm['min']:
                self.stagehandler.set_stage_info(cur_stage, self.close, mm['max'])

    def _354(self):
        pass

    #目前处于上升趋势->自然回辙->自然回升
    def _352(self):
        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        mm35 = self.stagehandler.get_stage_info('35') #mm35['max'], 就是3状态最大值
        if self.close >= self.last:
            if percent(mm35['max'], self.close) >= indicator['tp_up']:
                self.stagehandler.chg_stage('3', mm['min'], self.close)
            elif self.close > mm['max']:
                self.stagehandler.set_stage_info(cur_stage, mm['min'], self.close)
        else:
            if mm['max'] < mm35['max'] and self.close - mm['max'] <= indicator['lz_down']:
                #只处理为一种信号, 并不作为真正的趋势逆转
                notice_signal_transfer(self.stage)
            if percent(mm['max'], self.close) <= indicator['zx_down']:
                self.stagehandler.chg_stage('3526', self.close, mm['max'])
            elif self.close < mm['min']:
                self.stagehandler.set_stage_info(cur_stage, self.close, mm['max'])

    def _3523(self):
        pass

    #目前处于上升趋势->自然回辙->自然回升->次级回辙
    def _3526(self):

        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        if self.close >= self.last:
            if percent(mm['min'], self.close) >= indicator['zx_up']:
                self.stagehandler.chg_stage('35261', mm['min'], self.close)
        else:
            mm352 = self.stagehandler.get_stage_info('352')
            if percent(mm352['min'], self.close) <= indicator['tp_down']:
                self.stagehandler.chg_stage('4', self.close, mm['max'])
            elif self.close < mm['min']:
                self.stagehandler.set_stage_info(cur_stage, self.close, mm['max'])

    def _35264(self):
        pass

    #目前处于上升趋势->自然回辙->自然回升->次级回辙->次级回升
    def _35261(self):

        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        mm3526 = self.stagehandler.get_stage_info('3526')
        if self.close >= self.last:
            if percent(mm3526['max'], self.close) >= indicator['tp_up']:
                self.stagehandler.chg_stage('3', mm['min'], self.close)
            elif self.close > mm['max']:
                self.stagehandler.set_stage_info(cur_stage, mm['min'], self.close)
        else:
            if mm['max'] < mm3526['max'] and self.close - mm['max'] <= indicator['lz_down']:
                #只处理为一种信号, 并不作为真正的趋势逆转
                notice_signal_transfer(self.stage)
            if percent(mm['max'], self.close) <= indicator['zx_down']:
                self.stagehandler.chg_stage('4', self.close, mm['max'])
            elif self.close < mm['min']: #多余的吧...
                self.stagehandler.set_stage_info(cur_stage, self.close, mm['max'])

    def _352613(self):
        pass

    def _352614(self):
        pass

    def _4(self):
        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        if self.close >= self.last:
            if percent(mm['min'], self.close) >= indicator['zx_up']:
                self.stagehandler.chg_stage('42', mm['min'], self.close)
        else:
            if self.close < mm['min']:
                self.stagehandler.set_stage_info(cur_stage, self.close, mm['max'])

    def _42(self):
        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        if self.close >= self.last:
            if percent(mm['min'], self.close) >= indicator['zx_up'] + indicator['lz_up']:
                self.stagehandler.chg_stage('3', mm['min'], self.close)
            elif self.close > mm['max']:
                self.stagehandler.set_stage_info(cur_stage, mm['min'], self.close)
        else:
            if percent(mm['max'], self.close) <= indicator['zx_down']:
                self.stagehandler.chg_stage('425', self.close, mm['min'])

    def _423(self):
        pass

    def _425(self):
        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        mm42 = self.stagehandler.get_stage_info('42')
        if self.close >= self.last:
            if mm['min'] > mm42['min'] and self.close - mm['min'] >= indicator['lz_up']:
                #只处理为一种信号, 并不作为真正的趋势逆转
                notice_signal_transfer(self.stage)
            if percent(mm['min'], self.close) >= indicator['zx_up']:
                self.stagehandler.chg_stage('4251', mm['min'], self.close)
            elif self.close > mm['max']:
                self.stagehandler.set_stage_info(cur_stage, mm['min'], self.close)
        else:
            if percent(mm42['min'], self.close) <= indicator['tp_down']:
                self.stagehandler.chg_stage('4', self.close, mm['max'])
            elif self.close < mm['min']:
                self.stagehandler.set_stage_info(cur_stage, self.close, mm['max'])

    def _4254(self):
        pass

    def _4251(self):
        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        if self.close >= self.last:
            mm425 = self.stagehandler.get_stage_info('425')
            if percent(mm425['max'], self.close) >= indicator['tp_up']:
                self.stagehandler.chg_stage('3', mm['min'], self.close)
            elif self.close > mm['max']:
                self.stagehandler.set_stage_info(cur_stage, mm['min'], self.close)
        else:
            if percent(mm['max'], self.close) <= indicator['zx_down']:
                self.stagehandler.chg_stage('42516', self.close, mm['max'])

    def _42513(self):
        pass

    def _42516(self):
        cur_stage = self.stagehandler.get_cur_stage()
        mm = self.stagehandler.get_stage_info(cur_stage)
        mm4251 = self.stagehandler.get_stage_info('4251')
        if self.close >= self.last:
            if mm['min'] > mm4251['min'] and self.close - mm['min'] >= indicator['lz_up']:
                #只处理为一种信号, 并不作为真正的趋势逆转
                notice_signal_transfer(self.stage)
            if percent(mm['min'], self.close) >= indicator['zx_up']:
                self.stagehandler.chg_stage('3', mm['min'], self.close)
            elif self.close > mm['max']:
                self.stagehandler.set_stage_info(cur_stage, mm['min'], self.close)
        else:
            if percent(mm4251['min'], self.close) <= indicator['tp_down']:
                self.stagehandler.chg_stage('4', self.close, mm['max'])
            elif self.close < mm['min']:
                self.stagehandler.set_stage_info(cur_stage, self.close, mm['max'])


    def _425164(self):
        pass

    def _425163(self):
        pass

    def _init_tr(self, close):
        if self.close < 0:
            self.close = close
            return
        else:
            self.last = self.close
            self.close = close
            cur_stage = '3' if close > self.last else '4'
            # init
            self.stagehandler.set_cur_stage(cur_stage)
            self.stagehandler.set_stage_info(cur_stage, min(self.close, self.last), max(self.close, self.last))
            self.stagehandler.update_stage_info(cur_stage, start=self.quote.index[0], end=self.quote.index[1])
            #print(self.stagehandler.stage_info)
            return cur_stage

    def _trend_recognition(self, dt, close):
        cur_stage = self.stagehandler.get_cur_stage()
        if not cur_stage:
            cur_stage = self._init_tr(close)
            if not cur_stage:
                return
        else:
            self.last  = self.close
            self.close = close
            self.dt    = dt

        if self.stagehandler.get_pre_stage() != cur_stage:
            self.stagehandler.set_pre_stage(cur_stage)
            #self.stagehandler.update_info()

        self.stage_dict.get(cur_stage)()

    def trend_recognition_quote(self):
        #保存数据库比较好
        '''
        hset stock_info cur_stage
        hset stage_info_stock_info stage val #stage: 3, 35...; val:max, min
        '''

        '''
        "次级回升", "自然回升", "上升趋势", "下降趋势", "自然回辙", "次级回辙"
        #记录关键值和当前值
        '''

        #for close in self.quote.close.values:
        for ind, close in enumerate(self.quote.close):
            #print(ind, self.quote.index[ind], close)
            self.ind += 1 #indicator
            dt = self.quote.index[ind]
            self._trend_recognition(dt, close)

    def trend_recognition(self, dt, close):
        if self.quote:
            trend_recognition_quote()
            self.quote = None
        self._trend_recognition(dt, close)

    def trend_recognition(self):
        self.trend_recognition_quote()

    def print_result(self):
        self.stagehandler.print_stage_info()
