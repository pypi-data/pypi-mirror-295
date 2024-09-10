import unittest
import pandas as pd
from PN_DTW_FE.optimize_chunks_for_normality_pandas import optimize_chunks_for_normality_pandas

class TestOptimizeChunksForNormalityPandas(unittest.TestCase):
    def test_optimize_chunks_for_normality_pandas(self):
        series_list = [pd.Series([1, 2, 3]), pd.Series([4, 5, 6]), pd.Series([7, 8, 9])]
        num_new_chunks = 2
        seed = 1
        random_state = 42
        optimized_chunks, best_score = optimize_chunks_for_normality_pandas(series_list, num_new_chunks, seed, random_state)
        self.assertEqual(len(optimized_chunks), num_new_chunks)
        self.assertIsInstance(best_score, float)

if __name__ == '__main__':
    unittest.main()
