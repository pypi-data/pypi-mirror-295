#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Plome_api 
@File    ：__init__.py.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/8/19 下午2:53 
@explain : 文件说明
"""
from .cerebrum import DataCerebrum
import logging

# 屏蔽InfluxDB写入时候产生的timeout
logger = logging.getLogger("Rx")
logger.setLevel(logging.WARNING)
logger.propagate = False


__all__ = ["DataCerebrum"]
