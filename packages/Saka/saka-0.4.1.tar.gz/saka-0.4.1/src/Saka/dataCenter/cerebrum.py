#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Plome_api 
@File    ：cerebrum.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/8/22 上午11:50 
@explain : 文件说明
"""

from configparser import ConfigParser
from ..influxConn import InfluxConnector
import logging
import LockonToolAlpha as lta
from .influx_api import BucketDataAvailableNeuron
from .wind_api import WindDataNeuron
from .metaNeuron import MetaNeuron


class DataCerebrum:
    """ """

    def __init__(
        self,
        conf_fp,
        bucket,
        logging_fp="",
        logger_name="DataCerebrum",
        logging_level=logging.DEBUG,
    ):
        """

        Parameters
        ----------
        conf_fp : str
            配置文件路径
        bucket : str
            InfluxDB 存储数据的 bucket 名称。
        logging_fp : str, optional
            日志文件的路径, 默认为''
        logger_name : str, optional
            日志记录器的名称，默认为 'DataCerebrum'。
        logging_level : int, optional
            日志级别，默认为 `logging.DEBUG`。

        """

        config = ConfigParser()
        config.read(conf_fp, encoding="utf-8")
        self.fp_conf = config

        self.logger = lta.setup_logger(logging_fp, logger_name, logging_level)
        self.conn = InfluxConnector(conf_fp, logging_fp, logging_level)
        self.wind_api = WindDataNeuron(logging_fp, logging_level=logging_level)
        self.influx_api = BucketDataAvailableNeuron(
            self.conn, bucket, logging_fp, logging_level=logging_level
        )
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
