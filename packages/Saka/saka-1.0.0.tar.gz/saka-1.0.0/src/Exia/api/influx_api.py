#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Exia 
@File    ：influx_api.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/9/11 下午6:38 
@explain : 文件说明
'''
from .metaNeuron import MetaNeuron
from .._tricks import log_function_call
import logging


class InfluxNeuron(MetaNeuron):
    @log_function_call
    def __init__(
        self,
        bucket_name,
        logging_fp,
        logger_name="InfluxNeuron",
        logging_level=logging.DEBUG,
    ):

        self._bucket = bucket_name
        super().__init__(logging_fp, logger_name, logging_level)

    @log_function_call
    def activate(self):
        """
        激活神经元，连接数据库，初始化相关参数
        :return:
        """
        super().activate()
        self._conn = self.cerebro.conn
        self.query = self._conn.query_df
        self.write = self._conn.write_df
        self.write_batching = self._conn.write_df_batching

