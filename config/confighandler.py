#-*- encoding: utf-8 -*-
import configparser

class ConfigHandler:
    def __init__(self, cfg, section):
        self.cp = configparser.ConfigParser()
        self.cp.read(cfg)
        self.section = section

    def __getattr__(self, attr):
        return self.cp.get(self.section, attr)

if __name__ == '__main__':
    ch = ConfigHandler('config.ini', 'db')
    print(ch.db_host)
