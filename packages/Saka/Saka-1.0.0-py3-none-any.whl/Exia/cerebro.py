#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Exia 
@File    ：cerebro.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/9/11 下午6:29 
@explain : 文件说明
'''
import logging
from configparser import ConfigParser
import LockonToolAlpha as lta
from .influxConn import InfluxConn
from .api import *
from ._tricks import log_function_call

DATA_SOURCE = ['Wind']

class Cerebro(object):
    DATA_SOURCE_LIST = DATA_SOURCE

    @log_function_call
    def __init__(self, cerebro_conf, bucket,data_source, logging_fp, logger_name="Cerebro", log_level=logging.DEBUG):
        self.conf = ConfigParser()
        self.conf.read(cerebro_conf,encoding="utf-8")

        self.logger = lta.setup_logger(logging_fp, logger_name, log_level)
        self.conn = InfluxConn(cerebro_conf, logging_fp,log_level=log_level)
        self.influx_api = InfluxNeuron(bucket, logging_fp, logger_name="InfluxNeuron", logging_level=log_level)


        if data_source not in self.DATA_SOURCE_LIST:
            self.logger.error(f"{data_source} is not supported")
            raise ValueError
        if data_source == 'Wind':
            self.data_api = WindDataNeuron(logging_fp,logging_level=log_level)
        self.neuron_relink2cerebrum()
    def neuron_relink2cerebrum(self):
        """
        遍历类的所有属性，如果属性值是 `MetaNeuron` 的实例，则将其 `cerebrum` 属性设置为当前实例。

        Returns
        -------
        None
        """
        for neuron in vars(self):
            attr = getattr(self, neuron)
            if isinstance(attr, MetaNeuron):
                attr.link2cerebrum(self)
                attr.activate()
