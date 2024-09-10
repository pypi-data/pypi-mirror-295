#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/16 下午3:09
# @Author  : @Zhenxi Zhang
# @File    : api.py
# @Software: PyCharm

import pandas as pd
import pytz
import warnings
from influxdb_client.client.query_api import QueryApi
from influxdb_client.client.write_api import WriteApi
from influxdb_client import InfluxDBClient
from influxdb_client.extras import pd as pd_ex


def compose_influx_query(
    bucket: str, measurement: str, start_date: str, end_date: str, filter_fields: str
):
    """
    构建InfluxDB查询语句。

    Parameters
    ----------
    bucket : str
        数据桶名称。
    measurement : str
        测量名称，用于过滤结果。
    start_date : str
        查询的起始时间。
    end_date : str
        查询的结束时间。
    filter_fields : str
        需要过滤的字段，以逗号分隔。

    Returns
    -------
    str
        构建好的InfluxDB查询语句。
    """
    prefix = f'from(bucket:"{bucket}") |> range(start:{start_date}, stop:{end_date}) '
    suffix = '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'

    # 使用参数化查询
    if measurement != "":
        measurement_filter = (
            f'|> filter(fn: (r) => r["_measurement"] == "{measurement}" )'
        )
    else:
        measurement_filter = ""

    if filter_fields:
        try:
            field_list = filter_fields.split(",")
        except Exception as e:
            raise ValueError("Invalid filter_fields format.") from e
        code_field_filter_sentence = " or ".join(
            f'r["_field"] == "{field}"' for field in field_list
        )
    else:
        code_field_filter_sentence = ""

    and_word = ""
    if measurement_filter != "" and code_field_filter_sentence != "":
        and_word = " and ("
        measurement_filter = measurement_filter[:-1]
        code_field_filter_sentence += "))"

    sql_ = prefix + measurement_filter + and_word + code_field_filter_sentence + suffix

    return sql_


def query_by_sql(
    influxdb_query_api: QueryApi,
    query_sql: str,
    drop_influx_cols: bool = True,
    tz_info="Asia/Shanghai",
):
    """
    根据提供的SQL查询语句从InfluxDB中查询数据，并进行列筛选和时区转换。

    Parameters
    ----------
    influxdb_query_api : QueryApi
        InfluxDB的查询API实例，用于执行查询。
    query_sql : str
        查询数据的SQL语句。
    drop_influx_cols : bool, optional
        是否丢弃InfluxDB的特定列（如_start, _stop等），默认为True。
    tz_info : str, optional
        结果数据的时间区信息，默认为"Asia/Shanghai"。

    Returns
    -------
    df_set_index : DataFrame
        处理后的数据框，时间列被设为索引。
    """
    df = influxdb_query_api.query_data_frame(query_sql)

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


def query(
    influxdb_query_api: QueryApi,
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
        influxdb_query_api : Union[QueryApi,InfluxDBClient]
            InfluxDB的查询API对象或者 InfluxDBClient 对象。
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
    # 检查 api 类型
    if isinstance(influxdb_query_api, QueryApi):
        pass
    elif isinstance(influxdb_query_api, InfluxDBClient):
        influxdb_query_api = influxdb_query_api.query_api()
    else:
        raise TypeError("Invalid influxdb_query_api type.")

    exist_measurements = show_measurements(influxdb_query_api, bucket)

    if measurement not in exist_measurements:
        import sys

        sys.exit(
            f"Sys.exit 性能保护退出： Measurement '{measurement}' does not exist in bucket '{bucket}'."
        )

    if start_date == end_date:
        start_date = (pd.to_datetime(end_date) - pd.Timedelta(days=1)).strftime(
            "%Y-%m-%d"
        )
    query_sql = compose_influx_query(
        bucket, measurement, start_date, end_date, filter_fields=codes
    )
    return (
        query_by_sql(influxdb_query_api, query_sql, drop_influx_cols, tz_info),
        query_sql,
    )


def write(
    influxdb_client: InfluxDBClient,
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
    influxdb_client : InfluxDBClient
        InfluxDB的写入API对象。
    bucket : str
        InfluxDB中的bucket名称。
    measurement : str
        数据写入InfluxDB时的measurement名称。
    df : pd.DataFrame
        需要写入InfluxDB的DataFrame对象。
    _timezone : str, optional
        DataFrame中时间戳的时区，默认为"Asia/Shanghai"。
    one_time_threshold : int, optional, 已废弃
        单次写入的最大数据行数，默认为30行。

    Returns
    -------
    None
    """
    # 检查 api 类型
    if isinstance(influxdb_client, InfluxDBClient):
        pass
    else:
        raise TypeError("Invalid influxdb_client type.")

    if df.empty:
        print("DataFrame is empty. No data to write.")
        return
    #! 已废弃
    # if df.shape[0] > one_time_threshold:
    #     num_parts = int(df.shape[0] / one_time_threshold)
    #     rows_per_part = len(df) // num_parts
    #     dfs = [
    #         df[i * rows_per_part : (i + 1) * rows_per_part] for i in range(num_parts)
    #     ]
    #     dfs.append(df[num_parts * rows_per_part :])
    #
    # else:
    #     dfs = [df]
    #
    # for i in range(len(dfs)):
    #     df_split = dfs[i]
    #     try:
    #         with influxdb_client.write_api() as wapi:
    #             wapi.write(
    #                 bucket=bucket,
    #                 record=pd_ex.DataFrame(df_split),
    #                 data_frame_measurement_name=measurement,
    #                 data_frame_timestamp_timezone=_timezone,
    #             )
    #     except Exception as e:
    #         print(f"Failed to write data: {e}")
    try:
        with influxdb_client.write_api() as wapi:
            wapi.write(
                bucket=bucket,
                record=pd_ex.DataFrame(df),
                data_frame_measurement_name=measurement,
                data_frame_timestamp_timezone=_timezone,
            )
    except Exception as e:
        print(f"Failed to write data: {e}")


def show_measurements(influxdb_query_api: QueryApi, bucket: str):
    """
    查询InfluxDB中指定bucket下的所有measurement名称。
    """
    if isinstance(influxdb_query_api, QueryApi):
        pass
    elif isinstance(influxdb_query_api, InfluxDBClient):
        influxdb_query_api = influxdb_query_api.query_api()
    else:
        raise TypeError("Invalid influxdb_write_api type.")

    _query = (
        f'import "influxdata/influxdb/schema" schema.measurements(bucket: "{bucket}")'
    )

    resp = influxdb_query_api.query(_query).to_values()

    return [list(r)[-1] for r in resp]


def show_codes_in_bucket(
    influxdb_query_api: QueryApi, bucket: str, measurement: str = ""
):
    if isinstance(influxdb_query_api, QueryApi):
        pass
    elif isinstance(influxdb_query_api, InfluxDBClient):
        influxdb_query_api = influxdb_query_api.query_api()
    else:
        raise TypeError("Invalid influxdb_write_api type.")

    if measurement == "":
        _query = (
            f'import "influxdata/influxdb/schema" schema.fieldKeys(bucket:"{bucket}")'
        )
    else:
        _query = (
            f'import "influxdata/influxdb/schema" schema.measurementFieldKeys(bucket:"{bucket}",'
            f' measurement:"{measurement}",)'
        )

    table = influxdb_query_api.query(_query).to_values()
    return [list(t)[-1] for t in table.__iter__()]
