#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Plome_api
@File    ：_tricks.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/8/20 下午3:55
@explain : 文件说明
"""

import numpy as np


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
