import unittest
import pandas as pd
from PN_DTW_FE.exclude_and_assign_above_threshold import exclude_and_assign_above_threshold

class TestExcludeAndAssignAboveThreshold(unittest.TestCase):
    def test_exclude_and_assign_above_threshold(self):
        series = pd.Series([100, 200, 300, 400, 500])
        threshold = 300
        below_threshold, above_threshold = exclude_and_assign_above_threshold(series, threshold)
        self.assertTrue((below_threshold == pd.Series([100, 200, 300])).all())
        self.assertTrue((above_threshold == pd.Series([400, 500])).all())

if __name__ == '__main__':
    unittest.main()