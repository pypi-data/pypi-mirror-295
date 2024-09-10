#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Plome_api
@File    ：influx_api.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/8/22 上午11:40
@explain : 文件说明
"""
from .metaNeuron import MetaNeuron

import logging
import numpy as np
import pandas as pd
import LockonToolAlpha as lta


class BucketDataNeuron(MetaNeuron):
    """ """

    def __init__(
        self,
        conn,
        bucket,
        logging_fp,
        logger_name="BucketDataNeuron",
        logging_level=logging.DEBUG,
    ):
        """

        Parameters
        ----------
        conn : influxConn.InfluxConnector
            数据库连接对象，用于与数据库建立连接。
        logging_fp : str
            日志文件的路径。
        logger_name : str, optional
            日志记录器的名称，默认为 'DataCerebrum'。
        logging_level : int, optional
            日志级别，默认为 `logging.DEBUG`。
        """
        self._conn = conn
        self._bucket = bucket
        super().__init__(logging_fp, logger_name, logging_level)

    def query(
        self,
        measurement,
        start_date: str = "0",
        end_date: str = "now()",
        drop_influx_cols: bool = True,
        codes: str = "",
        tz_info="Asia/Shanghai",
    ):
        """
        调用接口完成查询指令

            Parameters
            ----------
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
            res = self._conn.query(
                self._bucket,
                measurement,
                start_date,
                end_date,
                drop_influx_cols,
                codes,
                tz_info,
            )
            return res
        except Exception as e:
            self.error(f"Error occurred while fetching data: {e}")

    def change_bucket(self, bucket):
        """
        切换数据桶
        """
        self.info(f"change_bucket:{self._bucket}->{bucket}")
        self._bucket = bucket

    def write(self, measurement, df, _timezone="Asia/Shanghai", one_time_threshold=30):
        """
        调用接口完成写入指令
        """
        return self._conn.write(
            self._bucket, measurement, df, _timezone, one_time_threshold
        )

    def get_exist_dates(self, measurement, code="000001.SZ"):
        """
        查询数据库中特定股票代码的存在日期。

        Parameters
        ----------
        measurement : str
            数据库中的测量名称。
        code : str, optional
            股票代码，默认为"000001.SZ"。

        Returns
        -------
        list[datetime.date]
            包含特定股票代码存在日期的列表。
        """
        df = self.query(measurement, codes=code)

        return df.index.tolist()

    def get_exist_codes_by_date(self, measurement, date):
        """
        根据给定的数据库连接和日期信息，查询并返回特定数据桶和测量条件下存在的代码。

        Parameters
        ----------
        measurement : str
            测量名称。
        date : str
            查询的日期，可以是字符串形式或pandas Timestamp对象。

        Returns
        -------
        list
            包含查询结果中所有存在的代码的列表，不包括时间戳和测量名称列。
        """

        df = self.query(measurement, date, date)
        res = df.columns.tolist()
        if len(res) == 0:
            return []
        for c in ["_time", "_measurement"]:
            res.remove(c)
        return res

    def get_exist_code(self, measurement):
        return self._conn.show_codes_in_bucket(self._bucket, measurement)

    def get_exist_measurements(self):
        return self._conn.show_measurements(self._bucket)


class BucketDataAvailableNeuron(BucketDataNeuron):
    """
    数据桶数据可用性管理器类
    """

    def __init__(
        self,
        conn,
        bucket,
        logging_fp,
        logger_name="BucketDataAvailableNeuron",
        logging_level=logging.DEBUG,
        oldest_date="2015-01-01",
    ):
        super().__init__(conn, bucket, logging_fp, logger_name, logging_level)
        self._oldest_date = oldest_date
        self.dMatrix = None

    def get_exist_matrix(
        self,
        basis_date,
        windows_len,
        measurement,
        tz_info="Asia/Shanghai",
        m_type="股票",
    ):
        """
        根据给定的基础日期和窗口长度，获取数据存在性矩阵。

        :param basis_date: 基础日期，用于计算数据矩阵的起始和结束日期。
        :type basis_date: str
        :param windows_len: 窗口长度，用于确定数据矩阵的起始日期，窗口起始日为basis_date的前第windows_len个工作日，-1表示使用最远的日期。
        :type windows_len: int
        :param measurement: 测量类型，如“daily_ret”，用于从数据库中查询数据。
        :type measurement: str
        :param tz_info: basis_date的时间区信息，默认为"Asia/Shanghai"。
        :type tz_info: str
        :return: 数据存在性矩阵，其中包含每个数据字段在特定日期是否存在。
        :rtype: pandas.DataFrame
        """
        windows_len = int(windows_len)
        if m_type == "股票":
            exist_query_code = "000001.SZ"
        else:
            exist_query_code = "000300.SH"

        end_date = str(lta.get_next_trade_date(lta.get_last_trade_date(basis_date)))
        if windows_len == -1:
            start_date = self._oldest_date
        else:
            start_date = end_date
            for _ in range(windows_len):
                start_date = lta.get_last_trade_date(start_date)

        self.info("获取数据存在性矩阵...")
        self.debug(f"数据存在性矩阵日期窗口，start_date: {start_date}, end_date: {end_date}")
        s_date = basis_date
        e_date = end_date
        while True:
            try:
                s_date = str(lta.get_last_trade_date(s_date))
                data_fields_array = self.query(
                    measurement, s_date, str(e_date), tz_info=tz_info
                )["_measurement"].values
                break
            except KeyError:
                self.debug(f"{s_date}:{e_date} data field is empty, try next")
                e_date = s_date
        self.debug(f"当前计算数据字段为:{data_fields_array}")
        exist_date_wind = self.cerebrum.wind_api.get_former_trade_calender_from_wind(
            start_date, end_date
        )
        exist_date_wind = pd.Series(exist_date_wind).apply(
            lambda x: x.strftime("%Y-%m-%d")
        )
        data_matrix = pd.DataFrame(
            0,
            index=exist_date_wind,
            columns=data_fields_array,
        )

        for dfd in data_fields_array:
            df_dates = pd.Series(self.get_exist_dates(dfd, exist_query_code)).apply(
                lambda x: x.strftime("%Y-%m-%d")
            )
            intersection = set(df_dates).intersection(set(exist_date_wind))
            data_matrix.loc[list(intersection), dfd] = 1

        self.dMatrix = data_matrix
        return data_matrix

    def get_empty_indexes_from_dm(self):
        """
        从距离矩阵中获取所有值为0的元素的行和列标签。

        此方法用于识别距离矩阵中未填充（值为0）的位置，并以字典形式返回这些位置的行和列标签。
        如果dMatrix未初始化，则抛出ValueError。
        如果dMatrix不是pandas DataFrame，则抛出ValueError。

        Raises:
            ValueError: 如果dMatrix为None或不是pandas DataFrame类型。

        Returns:
            dict: 包含所有值为0的元素的行和列标签的字典。
        """
        if self.dMatrix is None:
            raise ValueError("请先调用get_exist_matrix方法获取矩阵数据")
        if not isinstance(self.dMatrix, pd.DataFrame):
            raise ValueError("dMatrix必须是一个pandas DataFrame对象，请确认输入类型")

        ret = {}

        zero_indices = np.where(self.dMatrix.values == 0)
        row_labels = self.dMatrix.index[zero_indices[0]]
        col_labels = self.dMatrix.columns[zero_indices[1]]

        for column in col_labels:
            indices = np.where(col_labels == column)[0]
            sorted_indices = np.argsort(row_labels[indices])
            ret[column] = row_labels[indices][sorted_indices].tolist()
        return ret
