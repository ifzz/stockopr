#import redis
from config import dbip, dbport
import time

# conn = redis.StrictRedis(host='192.168.1.227', port=6379, db=0, password='server')
#conn = redis.StrictRedis(host=dbip, port=dbport, db=0)

def exec_cmd(*args, **options):
    r = conn.execute_command(*args, **options)
    return r

def set_day(day):
    exec_cmd('set', 'today', day)

def same_day():
    r = exec_cmd('get', 'today')
    _tm = time.localtime()
    if r and int(r) == _tm.tm_yday:
        return True
    set_day(_tm.tm_yday)

    return False

def save_to_db(stock_info):
    for key in stock_info:
        exec_cmd('hset', stock_info['name'], key, stock_info[key])
    #exec_cmd('save')

def load_data_from_db(stock_info):
    r = exec_cmd('hgetall', stock_info['name'])
    _stock_info = {}
    for i in range(0, len(r) - 1, 2):
        key = r[i].decode()
        val = r[i + 1].decode()
        if key == 'last_min':
            val = float(val)
        _stock_info.setdefault(key, val)
    return _stock_info

#
class Stage:
    def __init__(self):
        self.host = None
        self.cur_stage = None
        self.stages = []
        self.stage_info = {} #{stage:{'start':'', 'end':'', 'min':'', 'max':''}, }
        self.stage_info_history = []

    def save_cur_stage(self, stock_info):
        #same day
        if not same_day():
            del_stage(stock_info)

        # 历史数据
        # 3 -> 3 or 3 -> 4 or 4 -> 3 or 4 -> 4 过程中发生过的状态, 持续时间, 价格变化幅度...
        # 以分析哪个阶段持续时间最长, 价格变化幅度最大
        # 哪些状态出现最频繁

        # 是否需要分库 stockminer
        # create table stage (code varchar(8), start date, end date, substart date, subend date, stage varchar(8), min float, max float);
        #exec_cmd('hset', stock_info['stock_info'], 'cur_stage', stock_info['cur_stage'])
        #exec_cmd('rpush', 'cur_stage_%s' % stock_info['name'], stock_info['cur_stage'])

    def get_cur_stage(self):
        return self.cur_stage

    def set_cur_stage(self, stage):
        self.cur_stage = stage
        self.stages.append(stage)

    def get_all_stage(self):
        return self.stages

    def del_stage(self, stock_info):
        pass

    def del_all_stages(self):
        pass

    #def set_stage_info(self, stage, start, end, min, max):
    def set_stage_info(self, stage, min, max):
        #print(stage, 'set_stage_info...')
        #print(self.host.quote.index[self.host.ind], min, max)
        #print("*"*50)
        #self.stage_info[stage] = {'start':start, 'end':end, 'min':min, 'max':max}
        if stage in self.stage_info:
            self.stage_info[stage].update({'min':min, 'max':max, 'end':self.host.quote.index[self.host.ind]})
        else:
            self.stage_info.update({stage:{'min':min, 'max':max, 'end':self.host.quote.index[self.host.ind]}})

    def update_stage_info(self, stage, **info):
        self.stage_info[stage].update(info)

    def get_stage_info(self, stage):
        return self.stage_info[stage]

    def print_stage_info(self):
        key_list = ['start', 'end', 'min', 'max']
        _2d = len(self.stage_info_history)
        _1d = len(self.stages)
        i = 0
        for stage_info in self.stage_info_history:
            while 1:
                stage = self.stages[i]
                if stage not in stage_info:
                    break
                _stage_info = stage_info[stage]
                cnt = '%5s %s %s %5.2f %5.2f' % (stage, _stage_info['start'], _stage_info['end'], _stage_info['min'], _stage_info['max'])
                #for key in key_list:
                #    cnt += ' ' + str(stage_info[stage][key])
                print(cnt)
                i+=1
            print('*'*50)
        while i < len(self.stages):
            stage = self.stages[i]

            _stage_info = self.stage_info[stage]
            cnt = '%5s %s %s %5.2f %5.2f' % (stage, _stage_info['start'], _stage_info['end'], _stage_info['min'], _stage_info['max'])
            print(cnt)
            #for key in key_list:
            #    print(key, self.stage_info[stage][key])
            i+=1

    def chg_stage(self, cur_stage, _min, _max):
        #print('%s %5s %f %f' % (self.host.quote.index[self.host.ind], cur_stage, _min, _max))
        #print(self.stage_info)
        if self.stage_info != None and (cur_stage == '3' or cur_stage == '4'):
            self.stage_info_history.append(self.stage_info)
            self.stage_info = {}

        #设置
        self.set_cur_stage(cur_stage)
        self.set_stage_info(cur_stage, _min, _max)
        self.update_stage_info(cur_stage, start=self.host.quote.index[self.host.ind])

        #cur_stage_idx = cur_stage[len(cur_stage) - 1]
        #if cur_stage_idx == '3' or cur_stage_idx == '4':
        #open_stock_realtime_graph(stock_info, cur_stage_idx)

        #threading.Thread(target=draw_simplified_realtime_graph, kwargs=stock_info).start() #各种错误, TypeError: draw_simplified_realtime_graph() got an unexpected keyword argument 'lowest'
        #draw_simplified_realtime_graph(stock_info)


if __name__ == '__main__':
    pass
