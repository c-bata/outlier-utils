from unittest import TestCase
import numpy as np
import pandas as pd

from outliers import smirnov_grubbs as grubbs


class SmirnovGrubbsTests(TestCase):
    def test_check_type_when_given_list(self):
        dataset = [1, 10, 10, 10]
        actual_dataset = grubbs._check_type(dataset)
        self.assertIsInstance(actual_dataset, np.ndarray)

    def test_check_type_when_given_pandas_series(self):
        dataset = pd.Series([1, 10, 10, 10])
        actual_dataset = grubbs._check_type(dataset)
        self.assertIsInstance(actual_dataset, pd.Series)

    def test_get_target_index_when_given_numpy_ndarray(self):
        dataset = np.array([1, 10, 10, 10])
        expected_index = 0
        actual_index = grubbs._get_target_index(dataset)
        self.assertEqual(actual_index, expected_index)

    def test_get_target_index_when_given_pandas_series(self):
        dataset = pd.Series([1, 10, 10, 10])
        expected_index = 0
        actual_index = grubbs._get_target_index(dataset)
        self.assertEqual(actual_index, expected_index)

    def test_test_once_when_given_series(self):
        data = pd.Series([0, 10, 10, 10])
        actual_index = grubbs._test_once(data, 0.05)
        expected_index = 0
        self.assertEqual(actual_index, expected_index)

    def test_test_once_when_given_numpy_ndarray(self):
        data = np.array([0, 10, 10, 10])
        actual_index = grubbs._test_once(data, 0.05)
        expected_index = 0
        self.assertEqual(actual_index, expected_index)

    def test_delete_item_when_given_series(self):
        data = pd.Series([0, 1, 2, 3])
        actual_data = grubbs._delete_item(data, 1)
        self.assertEqual(len(actual_data), 3)

    def test_delete_item_when_given_numpy_ndarray(self):
        data = np.array([0, 1, 2, 3])
        actual_data = grubbs._delete_item(data, 1)
        self.assertEqual(len(actual_data), 3)
