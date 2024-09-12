#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Exia 
@File    ：influxConn.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/9/11 下午2:11 
@explain : 文件说明
"""
import logging
import warnings
import pytz
import pandas as pd
import LockonToolAlpha as lta
from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from ._tricks import log_function_call

class InfluxConn:
    @log_function_call
    def __init__(
        self, conn_conf, logging_fp, logger_name="InfluxConn", log_level=logging.WARN
    ):
        self.client = InfluxDBClient.from_config_file(conn_conf, encoding="utf-8")
        self.logger = lta.setup_logger(logging_fp, logger_name, log_level)
        self._set_logging()
        self.test_conn()

    @log_function_call
    def _set_logging(self):
        self.info = self.logger.info
        self.warn = self.logger.warn
        self.debug = self.logger.debug
        self.error = self.logger.error

    @log_function_call
    def test_conn(self):
        try:
            self.client.api_client.call_api("/ping", "GET")
            self.debug("Connected to InfluxDB")
        except Exception as e:
            self.error(f"Failed to connect to InfluxDB:{e}")

    @log_function_call
    def get_buckets(self):
        """
        获取所有桶的名称

        本方法通过调用客户端的buckets_api().find_buckets_iter()方法来查找所有桶，并返回一个包含所有桶名称的列表

        :return: 包含所有桶名称的列表
        :rtype: list of str
        """
        buckets = self.client.buckets_api().find_buckets_iter()
        return [bucket.name for bucket in buckets]

    @log_function_call
    def is_in_bucket(self, bucket_name):
        """
        检查存储桶名称是否存在于存储桶列表中。

        此函数通过查询存储桶API来获取所有存储桶的列表，
        然后检查给定的存储桶名称是否在这些存储桶中。

        Parameters
        ----------
        bucket_name : str
            要检查的存储桶名称。
        Returns
        -------
        bool
            如果存储桶名称存在于存储桶列表中，则返回True；否则返回False。
        """
        return bucket_name in self.get_buckets()

    @log_function_call
    def get_measurements(self, bucket_name: str):
        """
        查询InfluxDB中指定bucket下的所有measurement名称。
        Returns
        ---------
        list
            所有measurements的名称
        """
        _query = f'import "influxdata/influxdb/schema" schema.measurements(bucket: "{bucket_name}")'
        qapi = self.client.query_api()
        resp = qapi.query(_query)[0]

        return [i.values["_value"] for i in resp]

    class BatchingCallback(object):
        def __init__(self, root):
            self.root = root

        def success(self, conf: (str, str, str), data: str):
            self.root.debug(f"Written batch: {conf}, data: {data}")

        def error(self, conf: (str, str, str), data: str, exception: InfluxDBError):
            self.root.error(
                f"Cannot write batch: {conf}, data: {data} due: {exception}"
            )

        def retry(self, conf: (str, str, str), data: str, exception: InfluxDBError):
            self.root.debug(
                f"Retryable error occurs for batch: {conf}, data: {data} retry: {exception}"
            )

        """
        将df传入数据库，df的格式规范应该为:
        ---------------------------------------------------------
        ---index       id_code        field_name(e.g daily_Ret)
        2024-01-02     000001.SZ        0.025
        2024-01-02     000002.SZ        0.032
        2024-01-03     000001.SZ        0.025
        2024-01-03     000002.SZ        0.032
        .....
        ---------------------------------------------------------
        """

    @log_function_call
    def write_df_batching(
        self,
        df,
        bucket_name,
        measurement_name,
        tag_columns=None,
        _timezone="Asia/Shanghai",
    ):
        def _formatting_index(_df):
            index_old = _df.index
            index_new = pd.to_datetime(index_old)
            _df.index = index_new
            return _df

        if tag_columns is None:
            tag_columns = ["id_code"]
        callback = self.BatchingCallback(self)
        with self.client.write_api(
            success_callback=callback.success,
            error_callback=callback.error,
            retry_callback=callback.retry,
        ) as wapi:
            from influxdb_client.extras import pd as pd_ex

            wapi.write(
                bucket=bucket_name,
                record=pd_ex.DataFrame(_formatting_index(df)),
                data_frame_measurement_name=measurement_name,
                data_frame_tag_columns=tag_columns,
                data_frame_timestamp_timezone=_timezone,
            )

    @log_function_call
    def write_df(
        self,
        df,
        bucket_name,
        measurement_name,
        tag_columns=None,
        _timezone="Asia/Shanghai",
    ):
        def _formatting_index(_df):
            index_old = _df.index
            index_new = pd.to_datetime(index_old)
            _df.index = index_new
            return _df

        if tag_columns is None:
            tag_columns = ["id_code"]
        callback = self.BatchingCallback(self)
        with self.client.write_api(
            success_callback=callback.success,
            error_callback=callback.error,
            retry_callback=callback.retry,
        ) as wapi:
            wapi.write(
                bucket=bucket_name,
                record=_formatting_index(df),
                data_frame_measurement_name=measurement_name,
                data_frame_tag_columns=tag_columns,
                data_frame_timestamp_timezone=_timezone,
            )

    @log_function_call
    @staticmethod
    def compose_influx_query(
        self,
        bucket: str,
        measurement: str,
        start_date: str,
        end_date: str,
        filter_tags: dict,
        filter_fields: str,
    ):
        prefix = (
            f'from(bucket:"{bucket}") |> range(start:{start_date}, stop:{end_date}) '
        )
        suffix = (
            '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
        )
        filter_sentence = ""

        if measurement != "" or filter_tags != "" or filter_fields != "":
            prefix += "|> filter(fn: (r) => "
            suffix = ")" + suffix

        # 使用参数化查询
        if measurement != "":
            filter_sentence += f'r["_measurement"] == "{measurement}"'

        if filter_fields:
            try:
                field_list = filter_fields.split(",")
            except Exception as e:
                raise ValueError("Invalid filter_fields format.") from e
            code_field_filter_sentence = " or ".join(
                f'r["_field"] == "{field}"' for field in field_list
            )
            filter_sentence += f" and ({code_field_filter_sentence})"

        if filter_tags:
            try:
                tag_name = list(filter_tags.keys())[0]
                tags_list = filter_tags[tag_name].split(",")
            except Exception as e:
                raise ValueError("Invalid filter_fields format.") from e
            code_tag_filter_sentence = " or ".join(
                f'r["{tag_name}"] == "{tag}"' for tag in tags_list
            )
            filter_sentence += f" and ({code_tag_filter_sentence})"

        return prefix + filter_sentence + suffix

    @log_function_call
    def query_df(
        self,
        bucket,
        measurement="",
        start_date="0",
        end_date="now()",
        filter_tags=None,
        filter_fields="",
        drop_influx_cols=True,
        tz_info="Asia/Shanghai",
    ):
        '''

        :param bucket:
        :type bucket:
        :param measurement:
        :type measurement:
        :param start_date:
        :type start_date:
        :param end_date:
        :type end_date:
        :param filter_tags:
        :type filter_tags:
        :param filter_fields:
        :type filter_fields:
        :param drop_influx_cols:
        :type drop_influx_cols:
        :param tz_info:
        :type tz_info:
        :return:
        :rtype:
        '''
        if filter_tags is None:
            filter_tags = {}
        exist_measurements = self.get_measurements(bucket)
        if measurement not in exist_measurements:
            raise ValueError(f"measurement {measurement} not exist in bucket {bucket}")
        if start_date == end_date:
            start_date = (pd.to_datetime(end_date) - pd.Timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )
        query_sql = self.compose_influx_query(
            bucket, measurement, start_date, end_date, filter_tags, filter_fields
        )
        return self.query_by_sql(query_sql, drop_influx_cols, tz_info)

    @log_function_call
    def query_by_sql(self, sql, drop_influx_cols, tz_info="Asia/Shanghai"):
        self.debug(sql)
        query_api = self.client.query_api()
        df = query_api.query_data_frame(sql)
        if drop_influx_cols:
            columns_to_drop = ["_start", "_stop", "result", "table"]
            df.drop(
                columns=columns_to_drop, inplace=True, errors="ignore"
            )  # errors='ignore' 避免因不存在的列而抛出异常
        _tz = pytz.timezone(tz_info)

        if df.empty:
            return pd.DataFrame()

        tmp_series = df["_time"].copy()
        tmp_series = pd.to_datetime(tmp_series).dt.tz_convert(_tz)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            df_time = tmp_series.dt.date
            df["time"] = df_time
        return df.set_index("time")
