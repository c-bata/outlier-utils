from unittest import TestCase
import numpy as np

from outliers import smirnov_grubbs as grubbs


class SmirnovGrubbsTests(TestCase):
    def test_check_type_when_given_list(self):
        dataset = [1, 10, 10, 10]
        actual_dataset = grubbs._check_type(dataset)
        self.assertIsInstance(actual_dataset, np.ndarray)

    def test_get_target_index_when_given_numpy_ndarray(self):
        dataset = np.array([1, 10, 10, 10])
        expected_index = 0
        actual_index = grubbs._get_target_index(dataset)
        self.assertEqual(actual_index, expected_index)
