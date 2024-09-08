import math
import urllib.request
from collections.abc import Callable, Iterable
from typing import Any

import numpy as np


def dhondt(total: int, votes: np.ndarray | list[int]) -> np.ndarray:
    """ドント方式で議席数を計算

    :param total: 総議席数
    :param votes: 得票数の1次元配列
    :return: 議席数の1次元配列
    """
    votes_ = np.asarray(votes)
    seats = np.zeros_like(votes_, dtype=int)
    for _ in range(total):
        i = (votes_ / (seats + 1)).argmax()
        seats[i] += 1
    return seats


def enum_sub(iterable: Iterable[Any], target: int, func: Callable[..., int] | None = None) -> list[list[Any]]:
    """指定した合計となる部分集合の列挙

    :param iterable: 任意のオブジェクトのイテラブル
    :param target: 指定した合計
    :param func: オブジェクトを値に変換する関数, defaults to None
    :return: 部分集合の列挙
    """

    def _sub(start, subset, subtotal):
        if subtotal == target:
            result.append(list(subset))
            return
        elif subtotal > target:
            return
        for i in range(start, len(vals)):
            subset.append(objs[i])
            _sub(i + 1, subset, subtotal + vals[i])
            subset.pop()

    result: list[list[Any]] = []
    if func is None:
        func = lambda x: x  # noqa
    objs: list[Any] = list(iterable)
    vals: list[int] = list(map(func, objs))
    _sub(0, [], 0)
    return result


def circle_overlap_area(x1: float, y1, r1: float, x2: float, y2: float, r2: float) -> float:
    """2つの円の重なる面積

    :param x1: 円1のX座標
    :param y1: 円1のY座標
    :param r1: 円1の半径
    :param x2: 円2のX座標
    :param y2: 円2のY座標
    :param r2: 円2の半径
    :return: 面積
    """
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if d >= r1 + r2:
        return 0.0
    elif d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    p1 = r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
    p2 = r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2 * d * r2))
    p3 = math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)) / 2
    return p1 + p2 - p3


def read_spreadsheets(id_: str):
    """GoogleスプレッドシートからCSVの読込

    :param id_: URLのID(誰でも読取り可であること)
    :return: DataFrame
    """
    import pandas as pd

    url = f"https://docs.google.com/spreadsheets/d/{id_}/export?format=csv"
    with urllib.request.urlopen(url) as fp:
        df = pd.read_csv(fp)
    return df
    return df
