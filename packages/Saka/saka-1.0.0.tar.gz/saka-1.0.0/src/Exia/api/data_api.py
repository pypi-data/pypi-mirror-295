#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Exia 
@File    ：data_api.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/9/11 下午4:56 
@explain : 文件说明
"""
from WindPy import w
from .metaNeuron import MetaNeuron
import concurrent.futures
import logging
import pandas as pd
import LockonToolAlpha as lta
from .._tricks import log_function_call, split_codes_into_chunks
from abc import abstractmethod

WIND_QUERIES = ["wsd"]


def wind_res_df_formatted(df, fields):
    df = df.melt(ignore_index=False)
    cols = ['id_code']
    cols.extend(fields)
    df.columns = cols
    return df

class DataSourceNeuron(MetaNeuron):
    @log_function_call
    def __init__(
        self,
        logging_fp,
        logger_name="DataNeuron",
        logging_level=logging.DEBUG,
    ):
        super().__init__(logging_fp, logger_name, logging_level)

    @abstractmethod
    def get_former_trade_calender(self, start_date, end_date):
        pass

    @abstractmethod
    def get_total_ashare_code(self, date):
        pass

    @abstractmethod
    def query(self):
        pass

    @abstractmethod
    def query_multithread(self):
        pass


class WindDataNeuron(MetaNeuron):
    @staticmethod
    def check_w_decorator(func):
        """
        一个装饰器，用于在调用被装饰的函数前检查 `w` 的连接状态。

        如果 `w` 没有连接，则启动 `w`。
        """

        def wrapper(*args, **kwargs):
            # 在调用原始函数前检查 `w` 的连接状态
            if not w.isconnected():
                w.start()
            return func(*args, **kwargs)

        return wrapper

    @log_function_call
    @check_w_decorator
    def get_former_trade_calender(self, start_date, end_date):
        """
        从Wind数据库中获取时间段内的交易日历，含头含尾
        Parameters
        ----------
        start_date : 开始日期，格式为"YYYY-MM-DD"
        end_date : 结束日期，格式为"YYYY-MM-DD"

        Returns
        -------
        list
            包含从开始日期到结束日期范围内所有交易日的日期列表，格式为date对象
        """
        self.debug("get_former_trade_calender_from_wind")
        # response = w.wsd(used_code, "pct_chg", start_date, end_date, "", usedf=True)[1]
        # return response.index.tolist()
        response = w.tdays(start_date, end_date).Data[0]
        ret = [i.date() for i in response]
        return ret

    @log_function_call
    @check_w_decorator
    def get_total_ashare_code(self, date):
        """
        根据给定日期获取所有 A 股的 Wind 代码及证券名称。

        Parameters
        ----------
        date : datetime-like
            需要获取数据的日期。

        Returns
        -------
        pandas.DataFrame
            包含 'wind_code' 和 'sec_name' 两列的 DataFrame。
        """

        # 确保 Wind 已经连接
        if not w.isconnected():
            w.start()

        # 构建请求参数
        request_params = f"date={lta.date2str(date)};sectorid=a001010100000000"

        try:
            self.debug(f"get_total_ashare_code_from_wind")
            # 发送请求
            response = w.wset("sectorconstituent", request_params, usedf=True)

            # 检查响应
            # resp_code = response[0]  # 可以保留这部分用于调试
            df = response[1]

            # 返回结果
            return df[["wind_code", "sec_name"]]

        except Exception as e:
            # 更具体的错误处理
            error_message = f"Wind 获取 A 股代码失败: {type(e).__name__} - {str(e)}"
            self.error(error_message)
            raise ValueError(error_message) from e

    def query(self, wind_query_type, *args):
        qtypes = WIND_QUERIES
        if wind_query_type not in qtypes:
            self.error("Invalid wind query type: {wind_query_type}")
            raise ValueError(f"Invalid wind query type: {wind_query_type}")
        if wind_query_type == "wsd":
            field = args[1]
            wsd_result = self._wsd_query(*args)
            return wind_res_df_formatted(wsd_result, [field])

    def query_multithread(self, wind_query_type, *args):
        qtypes = WIND_QUERIES
        if wind_query_type not in qtypes:
            self.error("Invalid wind query type: {wind_query_type}")
            raise ValueError(f"Invalid wind query type: {wind_query_type}")
        if wind_query_type == "wsd":
            return self._wsd_query_multi_threads(*args)

    @log_function_call
    @check_w_decorator
    def _wsd_query(
        self, codes, wind_data_field, start_date, end_date, wind_batch_times=1, opt=""
    ):
        """
        从 Wind.wsd获取数据的函数。该函数按批次从 Wind 数据库中提取股票或其他金融数据，以提高效率和避免连接问题。

        Parameters
        ----------
        codes : list
            需要获取数据的股票代码列表。
        wind_data_field : str
            需要获取的 Wind 数据字段，例如 pct_chg 等。
        start_date : str
            数据的起始日期, 格式为 YYYY-MM-DD。
        end_date : str
            数据的结束日期, 格式为 YYYY-MM-DD。
        wind_batch_times : int, optional
            分批请求数据的批次数量，用于控制每次请求的代码数量，避免因请求过多导致的问题。
            默认值为 1，表示不分批。
        opt:str,optional
            表示用于wind查询的可选项，如ALLDAYS等参数

        Returns
        -------
        pandas.DataFrame or None
            包含所请求数据的 DataFrame，如果发生错误则返回 None。

        Raises
        ------
        ValueError
            如果 `wind_batch_times` 为 None 或者不是正整数。
        """
        if not w.isconnected():
            w.start()

        if wind_batch_times is None:
            raise ValueError("Wind batch times cannot be None")

        if start_date == end_date:
            # 如果只查询单日数据，为了防止wind返回的结构不一致，这里将起始日前移一天
            start_date = lta.get_last_trade_date(start_date)

        try:
            i = 0
            if wind_batch_times > 0:
                ret_total = []
                code_sets = split_codes_into_chunks(self, codes, wind_batch_times)
                for codes_chunk in code_sets:
                    i += 1
                    data = w.wsd(
                        codes_chunk,
                        wind_data_field,
                        start_date,
                        end_date,
                        opt,
                        usedf=True,
                    )[1]
                    ret_total.append(data)
                    self.debug(f"No. {i} batch data fetching")

                # 合并数据
                result = pd.concat(ret_total, axis=1)
                return result
            else:
                self.error(
                    f"Wind batch times should be a positive integer,input-{wind_batch_times}"
                )
                raise ValueError("Wind batch times should be a positive integer")
        except Exception as e:
            self.error(f"Error occurred while fetching data: {e}")
            return None

    @log_function_call
    @check_w_decorator
    def _wsd_query_multi_threads(
        self, codes, wind_data_field, start_date, end_date, wind_batch_times=1
    ):
        """
        从 Wind.wsd 多线程获取数据的函数。该函数按批次从 Wind 数据库中提取股票或其他金融数据，以提高效率和避免连接问题。

        Parameters
        ----------
        codes : list
            需要获取数据的股票代码列表。
        wind_data_field : str
            需要获取的 Wind 数据字段，例如 pct_chg 等。
        start_date : str
            数据的起始日期, 格式为 YYYY-MM-DD。
        end_date : str
            数据的结束日期, 格式为 YYYY-MM-DD。
        wind_batch_times : int, optional
            分批请求数据的批次数量，用于控制每次请求的代码数量，避免因请求过多导致的问题。
            默认值为 1，表示不分批。

        Returns
        -------
        pandas.DataFrame or None
            包含所请求数据的 DataFrame，如果发生错误则返回 None。

        Raises
        ------
        ValueError
            如果 `wind_batch_times` 为 None 或者不是正整数。
        """
        if not w.isconnected():
            w.start()

        if wind_batch_times is None:
            raise ValueError("Wind batch times cannot be None")

        if start_date == end_date:
            # 如果只查询单日数据，为了防止 Wind 返回的结构不一致，这里将起始日前移一天
            start_date = lta.get_last_trade_date(start_date)

        try:
            if wind_batch_times > 0:
                code_sets = split_codes_into_chunks(self, codes, wind_batch_times)

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [
                        executor.submit(
                            w.wsd,
                            codes_chunk,
                            wind_data_field,
                            start_date,
                            end_date,
                            "",
                            usedf=True,
                        )
                        for codes_chunk in code_sets
                    ]

                    # 等待所有任务完成
                    results = [future.result()[1] for future in futures]

                # 合并数据
                result = pd.concat(results, axis=1)
                return result
            else:
                self.error(
                    f"Wind batch times should be a positive integer,input-{wind_batch_times}"
                )
                raise ValueError("Wind batch times should be a positive integer")
        except Exception as e:
            self.error(f"Error occurred while fetching data: {e}")
            return None
