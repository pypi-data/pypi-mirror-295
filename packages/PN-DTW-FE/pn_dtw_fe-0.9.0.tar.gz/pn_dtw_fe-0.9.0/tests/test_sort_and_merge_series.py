import unittest
import pandas as pd
from PN_DTW_FE.sort_and_merge_series import sort_and_merge_series

class TestSortAndMergeSeries(unittest.TestCase):
    def test_sort_and_merge_series(self):
        series = pd.Series([1, 2, 3, 4, 5, 6])
        merged_series = sort_and_merge_series(series)
        self.assertEqual(len(merged_series), len(series))
        self.assertTrue((merged_series.sort_values().values == series.sort_values().values).all())

if __name__ == '__main__':
    unittest.main()
