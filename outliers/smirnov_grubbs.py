"""
Smirnov-Grubbs test for outlier detection.

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
        raise TypeError('Unsupported data format')


def _get_target_index(data):
    """Compute the index of the farthest value from the sample mean. 

    :param numpy.array or pandas.Series data: data set
    :return int: the index of the element
    """
    relative_values = data - data.mean()
    return abs(relative_values).argmax()


def _get_g(data):
    """Compute the test statistic, G.

    :param numpy.ndarray data: data set
    :return: test statistic (G value)
    """
    target_index = _get_target_index(data)
    absolute_normalized_data = abs((data - data.mean()) / data.std())
    return absolute_normalized_data[target_index]


def _get_g_test(n, alpha):
    """Compute a significant value score following these steps, being n the
    data set size and alpha the significance level:

    1. Find the upper critical value of the t-distribution with n-2 degrees of
    freedom and a significance level of alpha/2n, t(alpha / 2n, n-2).

    2. Use this t value to find the score with the following formula:
       ((n-1) / sqrt(n)) * (sqrt(t**2 / (n-2 + t**2)))

    :param int n: data set size
    :param float alpha: significance level
    :return: G_test score
    """
    t = stats.t.isf(alpha / (2*n), n-2)  # For two-sided tests
    g_test = ((n-1) / sqrt(n)) * (sqrt(t**2 / (n-2 + t**2)))
    return g_test


def _test_once(data, alpha):
    """Perform one iteration of the Smirnov-Grubbs test.

    :param numpy.array data: data set
    :param float alpha: significance level
    :return: the index of the outlier if one if found; None otherwise
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
        raise TypeError('Unsupported data format')


def test(data, alpha=0.95):
    """Run the Smirnov-Grubbs test to remove outliers in the given data set.

    :param numpy.array data: data set
    :param float alpha: significance level
    :return: data set without outliers
    """
    data = _check_type(data)
    while True:
        target_index = _test_once(data, alpha)
        if target_index is None:
            break
        data = _delete_item(data, target_index)
    return data
