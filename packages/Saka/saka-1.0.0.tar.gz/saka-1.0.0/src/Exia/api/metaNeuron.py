#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Exia 
@File    ：metaNeuron.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/9/11 下午4:55 
@explain : 文件说明
"""

import logging
import LockonToolAlpha as lta
from abc import ABC


class MetaNeuron(ABC):
    def __init__(
        self, logging_fp, logger_name="DefaultNeuron", logging_level=logging.DEBUG
    ):
        """
        初始化 MetaNeuron 实例，设置日志记录器。

        Parameters:
        - logging_fp: str，日志文件的路径。
        - logger_name: str, optional，日志记录器的名称，默认为 'DefaultNeuron'。
        - logging_level: int, optional，日志级别，默认为 logging.DEBUG。
        """

        self.logger = lta.setup_logger(logging_fp, logger_name, logging_level)
        self.info = self.logger.info
        self.debug = self.logger.debug
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.cerebro = None

    def link2cerebrum(self, cerebrum):
        """
        将当前实例与 cerebrum 关联。
        """
        self.cerebro = cerebrum

    def activate(self):
        """
        激活当前实例，执行其具体的逻辑。
        """
        pass
