#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 下午3:08
# @Author  : @Zhenxi Zhang
# @File    : __init__.py.py
# @Software: PyCharm
from influxdb_client import InfluxDBClient
from .api import query as q
from .api import write as w
from .api import compose_influx_query as ciq
from .api import show_measurements, show_codes_in_bucket
import pandas as pd
import LockonToolAlpha as lta
import logging


class InfluxConnector:
    def __init__(self, config_file, logging_fp="", log_level=logging.DEBUG):
        """
        初始化函数

        Parameters
        ----------
        config_file : str
            配置文件路径，用于初始化InfluxDB客户端
        logging_fp : str, optional
            日志文件路径，用于设置日志记录位置，默认为空字符串
        log_level : logging level, optional
            日志记录级别，默认为logging.DEBUG
        """
        self.client = InfluxDBClient.from_config_file(config_file, encoding="utf-8")
        self._info = self.client.__dict__
        self.logger = lta.setup_logger(logging_fp, "Conn", log_level)
        try:
            self.client.api_client.call_api("/ping", "GET")
            self.logger.debug(f"client connection is ok")
        except Exception as e:
            self.logger.error(f"client connection is error: {e}")

    def show_measurements(self, bucket: str):
        """
        获取指定bucket中的所有measurement名称。
        """
        self.measurements = show_measurements(self.client, bucket)
        return self.measurements

    def show_codes_in_bucket(self, bucket: str, measurement: str = ""):
        """
        获取指定bucket中的所有代码。
        """
        self.codes = show_codes_in_bucket(self.client, bucket, measurement)
        return self.codes

    def __del__(self):
        """
        析构函数，用于关闭数据库连接。
        """
        self.client.close()

    def query(
        self,
        bucket: str,
        measurement: str = "",
        start_date: str = "0",
        end_date: str = "now()",
        drop_influx_cols: bool = True,
        codes: str = "",
        tz_info="Asia/Shanghai",
    ):
        """
        从InfluxDB中查询数据并处理的api接口。

            Parameters
            ----------
            bucket : str
                数据桶名称，相当于数据库中的表。
            measurement : str
                测量名称，InfluxDB中数据的逻辑分组。
            start_date : str
                查询的开始时间，默认为"0"，表示从最早的时间开始。
            end_date : str
                查询的结束时间，默认为"now()"，表示查询到当前时间。
            drop_influx_cols : bool
                是否丢弃InfluxDB的内部列，如"_start", "_stop"等。
            codes : str
                查询中要筛选的代码，多个字段用","分隔。
            tz_info : str
                结果数据的时间区信息，默认为"Asia/Shanghai"。

            Returns
            -------
            pandas.DataFrame
                查询结果的DataFrame，以日期为索引。
        """

        try:
            res, sql = q(
                self.client,
                bucket,
                measurement,
                start_date,
                end_date,
                drop_influx_cols,
                codes,
                tz_info,
            )

            self.logger.debug(sql)

            return res
        except Exception as e:
            sql = ciq(bucket, measurement, start_date, end_date, codes)
            self.logger.error(f"query error: {e}")
            self.logger.error(f"query error: {sql}")
            return pd.DataFrame()

    def write(
        self,
        bucket: str,
        measurement: str,
        df: pd.DataFrame,
        _timezone="Asia/Shanghai",
        one_time_threshold=30,
    ):
        """
        将DataFrame中的数据写入InfluxDB。

        Parameters
        ----------
        bucket : str
            InfluxDB中的bucket名称。
        measurement : str
            数据写入InfluxDB时的measurement名称。
        df : pd.DataFrame
            需要写入InfluxDB的DataFrame对象。
        _timezone : str, optional
            DataFrame中时间戳的时区，默认为"Asia/Shanghai"。
        one_time_threshold : int, optional
            单次写入的最大数据行数，默认为30行。

        Returns
        -------
        None
        """

        try:
            w(
                self.client,
                bucket,
                measurement,
                df,
                _timezone,
                one_time_threshold,
            )
            return None
        except Exception as e:
            self.logger.error(f"write error: {e}")
            return pd.DataFrame()
