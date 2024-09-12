#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Exia 
@File    ：_tricks.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/9/11 下午5:11 
@explain : 文件说明
"""
import functools
import logging
import numpy as np

def log_function_call(func):
    """
    一个装饰器，用于记录被调用的函数及其参数。

    在函数调用前后打印日志信息。
    """
    logger = logging.getLogger("func_logger")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 记录函数调用前的信息
        logger.debug(
            f"Calling function {func.__name__} with args: {args}, kwargs: {kwargs}"
        )

        # 调用原始函数
        result = func(*args, **kwargs)

        # 记录函数调用后的信息
        logger.debug(f"Function {func.__name__} returned: {result}")

        return result

    return wrapper


def split_codes_into_chunks(neuro, raw_list, times=5):
    """
    将代码列表分割成多个子列表（块）。

    Parameters
    ----------
    neuro: MetaNeuron
        调用此函数的神经单元self

    raw_list : list
        需要分割的代码列表。
    times : int, optional
        分割的块数，默认为 5。

    Returns
    -------
    list
        包含分割后的代码块的列表。

    Raises
    ------
    ValueError
        如果 `test_codes` 不是列表，或者 `times` 不是正整数。
    """
    # 输入验证
    if not isinstance(raw_list, list):
        neuro.error(f"test_codes must be a list.Input-{raw_list}")
        raise ValueError("test_codes must be a list.")
    if not isinstance(times, int) or times <= 0:
        neuro.error(f"times must be a positive integer.Input-{times}")
        raise ValueError("times must be a positive integer.")

    codes_num = len(raw_list)
    # 提前计算每个分段的结束索引
    chunk_sizes = [int(np.ceil((i + 1) * codes_num / times)) for i in range(times)]

    res = []
    start_index = 0
    for end_index in chunk_sizes:
        # 显式地检查边界条件
        end_index = min(end_index, codes_num)
        res.append(raw_list[start_index:end_index])
        start_index = end_index
    return res
