#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ Author: stephen.wan
@ Date: 2022-11-08 17:35
@ Email: stephen.wan@colourdata.com.cn
@ LastEditors: stephen.wan
@ LastEditTime: 2022-11-08 17:35
@ ProjectName: YiliEcommerceNewProductProject
@ Description: to do
"""
import os
import logging
from logging import handlers
import toml


def get_base_file(name=None):
    base_path = os.path.dirname(os.path.abspath(name))
    return base_path


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Log:
    def __init__(self, filename=None, log_level=logging.INFO, backup_count=2):
        """日志logger类"""
        # 创建logs文件夹
        self.file_name = filename
        self.log_level = log_level
        self.backup_count = backup_count
        cur_path = os.path.dirname(os.path.realpath(self.file_name))
        self.log_path = os.path.join(cur_path, 'logs')
        # 如果不存在这个logs文件夹，就自动创建一个
        if not os.path.exists(self.log_path): os.mkdir(self.log_path)
        # 文件的命名
        self.logname = os.path.join(self.log_path, f"{os.path.basename(self.file_name).split('.')[0]}.log")
        # self.log_name_error = os.path.join(self.log_path,
        #                       f"{os.path.basename(self.file_name).split('.')[0]}-error.log")

        # 定义日志格式
        log_format = '[%(asctime)s-%(filename)-s-%(lineno)d]-%(levelname)s:%(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        logging.basicConfig(
            # format=log_format,
            datefmt=date_format
        )
        self.logger = logging.getLogger(self.logname)
        self.logger.setLevel(self.log_level)
        self.logger.propagate = False
        # 日志输出格式
        # self.formatter = logging.Formatter('[%(asctime)s]-%(filename)s]-%(levelname)s:%(message)s')
        self.formatter = logging.Formatter(log_format, date_format)

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        # fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        # fh.setLevel(logging.INFO)
        # fh.setFormatter(self.formatter)
        # self.logger.addHandler(fh)
        th = handlers.TimedRotatingFileHandler(filename=self.logname, interval=1,
                                               when='MIDNIGHT', backupCount=self.backup_count,
                                               encoding='utf-8')
        th.suffix = "%Y-%m-%d.log"  # 设置文件后缀
        # info_filter = logging.Filter()
        # info_filter.filter = lambda record: record.levelno <= logging.WARNING  # 设置过滤等级
        # th.addFilter(info_filter)
        th.setFormatter(self.formatter)  # 设置文件里写入的格式
        self.logger.addHandler(th)

        # 创建一个StreamHandler,用于输出到控制台
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.ERROR)
        # ch.setFormatter(self.formatter)
        # self.logger.addHandler(ch)

        # 创建TimedRotatingFileHandler,错误信息输出到对应文件
        # th_error = handlers.TimedRotatingFileHandler(filename=self.log_name_error,
        #                                              interval=1, when='MIDNIGHT',
        #                                              backupCount=2, encoding='utf-8')
        # th_error.suffix = "%Y-%m-%d.log"  # 设置文件后缀
        # th_error.setLevel(logging.ERROR)
        # th_error.setFormatter(self.formatter)  # 设置文件里写入的格式
        # self.logger.addHandler(th_error)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        # self.logger.removeHandler(ch)
        self.logger.removeHandler(th)
        # self.logger.removeHandler(th_error)

        # 关闭
        # ch.close()
        th.close()
        # th_error.close()

    def set_log_level(self, log_level=logging.INFO):
        self.logger.setLevel(log_level)

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


class TomlConfig:
    """
    读写toml对象，实际就是个dict
    """

    def __init__(self, toml_fileanme):
        self.t_dict = dict()  # 创建空字典
        self.toml_file_path = toml_fileanme

    def update(self, t_data):
        # 给toml文件添加配置
        self.t_dict.update(t_data)
        return self.t_dict

    def write(self, t_data):
        # 写入到toml文件
        with open(self.toml_file_path, "w", encoding="utf-8") as fs:
            toml.dump(t_data, fs)

    def read(self):
        # 读取toml文件
        with open(self.toml_file_path, "r", encoding="utf-8") as fs:
            t_data = toml.load(fs)
        return t_data

    def read_str(self, s_data):
        # 从字符串中解析TOML，返回一个字典对象或类的实例对象
        t_data = toml.loads(s_data, _dict=dict)
        return t_data

    def read_dict(self, dict):
        # 将字典对象格式化成toml字符串
        t_data = toml.dumps(dict)
        return t_data


if __name__ == '__main__':
    print(get_base_file(__file__))

