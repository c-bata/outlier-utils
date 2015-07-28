"""
スミルノフグラブス検定による棄却検定。


"""

import numpy as np
import pandas as pd
from scipy import stats
from math import sqrt


__all__ = ['test']


def _check_type(data):
    if isinstance(data, np.ndarray):
        return data
    elif isinstance(data, pd.Series):
        return data
    elif isinstance(data, list):
        return np.array(data)
    else:
        raise TypeError('データセットの型がおかしいです。')


def _get_target_index(data):
    """最も平均値からの差が大きい値のindexを取得.

    :param numpy.array or pandas.Series data: データ群
    :return int: 最も平均値からの差が大きい値のindex
    """
    relative_values = data - data.mean()
    return abs(relative_values).argmax()


def _get_g(data):
    """データセットを正規化し、検定の対象となる値を取得.

    :param numpy.ndarray data:
    :return:
    """
    target_index = _get_target_index(data)
    absolute_normalized_data = abs((data - data.mean()) / data.std())
    return absolute_normalized_data[target_index]


def _get_g_test(n, alpha):
    """有意点を返す。
    有意点の求め方.

    1. t値を求める。

      nをデータ数, alphaを有意水準とすると、
      t(alpha / n, n-2)となるt値を探す。

      例えば棄却率5%, nが10の時、t(0.05, 8)を調べれば良い。

    2. 有意点を求める

      https://ja.wikipedia.org/wiki/外れ値

      g_test = ((n-1) / sqrt(n)) * (sqrt(t**2 / (n-2 + t**2)))

    :param int n: data size
    :param float alpha: 有意水準(Significance level)
    :return: Gtest
    """
    t = stats.t.isf(alpha / (2*n), n-2)  # 両側検定の時は
    g_test = ((n-1) / sqrt(n)) * (sqrt(t**2 / (n-2 + t**2)))
    return g_test


def _test_once(data, alpha):
    """データセットの中で1回だけスミルノフグラブス検定を行う
    棄却検定に成功すればそのndarrayのインデックスを返す。
    失敗すればNone。

    :param numpy.array data: データセット
    :param float alpha: 有意水準(Significance level)
    :return:
    """
    target_index = _get_target_index(data)
    g = _get_g(data)
    g_test = _get_g_test(len(data), alpha)
    if g > g_test:
        return target_index
    return


def _delete_item(data, index):
    if isinstance(data, pd.Series):
        return data.drop(index)
    elif isinstance(data, np.ndarray):
        return np.delete(data, index)
    else:
        raise TypeError('データの型がおかしいです。')


def test(data, alpha=0.95):
    """スミルノフグラブス検定をデータセットに対して適用し、残ったデータセットを返す.

    :param numpy.array data: データセット
    :param float alpha: 有意水準(Significance level)
    :return:
    """
    data = _check_type(data)
    while True:
        target_index = _test_once(data, alpha)
        if target_index is None:
            break
        data = _delete_item(data, target_index)
    return data
