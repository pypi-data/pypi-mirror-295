#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/19 上午10:16
# @Author  : @Zhenxi Zhang
# @File    : bucket.py
# @Software: PyCharm

import LockonToolAlpha as lta
from influxdb_client.client.bucket_api import BucketsApi
import logging


def get_bucket_list(client, logger=None, log_file=""):
    if logger is None:
        logger = lta.setup_logger(log_file, "bucket_show")

    buckets_api = client.buckets_api()
    print(f"\n------- List -------\n")
    buckets = buckets_api.find_buckets_iter()

    print("\n".join([f" ---\n Name: {bucket.name}" for bucket in buckets]))
    print("---")
    return [bucket.id for bucket in buckets]


def get_buckets(buckets_api, logger=None, log_file=""):
    """
    获取存储桶列表。

    本函数旨在从提供的API中获取存储桶列表。它允许传入一个日志记录器和一个日志文件名，
    如果没有提供日志记录器，它会使用内置的设置创建一个。

    Parameters
    ----------
    buckets_api : Union[BucketsAPi, InfluxDBClient]
        提供存储桶API的接口或对象。
    logger :  logging.Logger
        用于记录日志的日志记录器对象。
    log_file :  str
        日志文件的路径。

    Returns
    -------
    list
        包含所有存储桶名称的列表。
    """
    if logger is None:
        logger = lta.setup_logger(log_file, "bucket_show")

    # 改进类型检查逻辑
    if not isinstance(buckets_api, BucketsApi):
        try:
            buckets_api = buckets_api.buckets_api()  # 假设buckets_api有buckets_api方法
        except AttributeError as e:  # 只捕获AttributeError
            logger.error(e)  # 使用正确的日志记录方法
            logger.error(
                "buckets_api must be a BucketsApi object or have a buckets_api method."
            )
            raise TypeError(
                "buckets_api must be a BucketsApi object or have a buckets_api method."
            ) from e

    buckets = buckets_api.find_buckets_iter()
    return [bucket.name for bucket in buckets]


def isin_bucket(bucket_name, buckets_api):
    """
    检查存储桶名称是否存在于存储桶列表中。

    此函数通过查询存储桶API来获取所有存储桶的列表，
    然后检查给定的存储桶名称是否在这些存储桶中。

    Parameters
    ----------
    bucket_name : str
        要检查的存储桶名称。
    buckets_api : Union[BucketsAPi, InfluxDBClient]
        用于获取存储桶列表的API或客户端。

    Returns
    -------
    bool
        如果存储桶名称存在于存储桶列表中，则返回True；否则返回False。
    """
    buckets = get_buckets(buckets_api)
    return bucket_name in buckets
