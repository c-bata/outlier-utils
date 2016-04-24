from unittest import TestCase

import numpy as np

from scipy import stats

from outliers import smirnov_grubbs as grubbs

try:
    import pandas as pd
except ImportError:
    pd = None


class SmirnovGrubbsTests(TestCase):
    def setUp(self):
        self.data1 = [1, 10, 10, 10]
        self.data2 = [0, 10, 10, 10]
        self.data3 = [0, 1, 2, 3]

        self.rvs = self._get_normal_rvs_with_outliers()
        self.default_alpha = 0.1

    def _get_normal_rvs_with_outliers(self, n=50):
        random_values = stats.norm.rvs(size=n-2)
        std = random_values.std()
        random_values = np.append(random_values, random_values.min()-5*std)
        random_values = np.append(random_values, random_values.max()+5*std)
        return random_values

    def test_check_type_when_given_list(self):
        grubbs_test = grubbs.TwoSidedGrubbsTest(self.data1)
        copied_data = grubbs_test._copy_data()

        self.assertIsInstance(copied_data, np.ndarray)

    def test_check_type_when_given_pandas_series(self):
        if pd is not None:
            data = pd.Series(self.data1)
            grubbs_test = grubbs.TwoSidedGrubbsTest(data)
            copied_data = grubbs_test._copy_data()

            self.assertIsInstance(copied_data, pd.Series)

    def test_get_target_index_when_given_numpy_ndarray(self):
        data = np.array(self.data1)
        grubbs_test = grubbs.TwoSidedGrubbsTest(data)

        expected_index = 0
        actual_index, _ = grubbs_test._target(data)
        self.assertEqual(actual_index, expected_index)

    def test_get_target_index_when_given_pandas_series(self):
        if pd is not None:
            data = pd.Series(self.data1)
            grubbs_test = grubbs.TwoSidedGrubbsTest(data)

            expected_index = 0
            actual_index, _ = grubbs_test._target(data)
            self.assertEqual(actual_index, expected_index)

    def test_test_once_when_given_pandas_series(self):
        if pd is not None:
            data = pd.Series(self.data2)
            grubbs_test = grubbs.TwoSidedGrubbsTest(data)

            expected_index = 0
            actual_index = grubbs_test._test_once(data, 0.05)
            self.assertEqual(actual_index, expected_index)

    def test_test_once_when_given_numpy_ndarray(self):
        data = np.array(self.data2)
        grubbs_test = grubbs.TwoSidedGrubbsTest(data)

        expected_index = 0
        actual_index = grubbs_test._test_once(data, 0.05)
        self.assertEqual(actual_index, expected_index)

    def test_delete_item_when_given_pandas_series(self):
        if pd is not None:
            data = pd.Series(self.data3)
            grubbs_test = grubbs.TwoSidedGrubbsTest(data)

            actual_data = grubbs_test._delete_item(data, 1)
            self.assertEqual(len(actual_data), 3)

    def test_delete_item_when_given_numpy_ndarray(self):
        data = np.array(self.data3)
        grubbs_test = grubbs.TwoSidedGrubbsTest(data)

        actual_data = grubbs_test._delete_item(data, 1)
        self.assertEqual(len(actual_data), 3)

    def test_two_sided_outlier_detection(self):
        outliers = grubbs.two_sided_test_outliers(self.rvs,
                                                  alpha=self.default_alpha)

        self.assertIn(self.rvs.min(), outliers)
        self.assertIn(self.rvs.max(), outliers)

    def test_two_sided_outlier_detection_with_data_output(self):
        data = grubbs.two_sided_test(self.rvs, alpha=self.default_alpha)

        self.assertNotIn(self.rvs.min(), data)
        self.assertNotIn(self.rvs.max(), data)
        self.assertGreater(len(data), 0)
        for value in data:
            self.assertIn(value, self.rvs)

    def test_two_sided_outlier_detection_with_index_output(self):
        outlier_indices = grubbs.two_sided_test_indices(
            self.rvs, alpha=self.default_alpha)

        n = len(self.rvs) - 2
        self.assertIn(n, outlier_indices)
        self.assertIn(n+1, outlier_indices)

    def test_one_sided_min_outlier_detection(self):
        outliers = grubbs.min_test_outliers(self.rvs, alpha=self.default_alpha)

        self.assertIn(self.rvs.min(), outliers)
        self.assertNotIn(self.rvs.max(), outliers)

    def test_one_sided_max_outlier_detection(self):
        outliers = grubbs.max_test_outliers(self.rvs, alpha=self.default_alpha)

        self.assertIn(self.rvs.max(), outliers)
        self.assertNotIn(self.rvs.min(), outliers)
