import unittest
import pandas as pd
from PN_DTW_FE.sort_and_divide_series_into_n_chunks import sort_and_divide_series_into_n_chunks

class TestSortAndDivideSeriesIntoNChunks(unittest.TestCase):
    def test_sort_and_divide_series_into_n_chunks(self):
        series = pd.Series([1, 3, 2, 5, 4, 6])
        total_chunks = 3
        chunks = sort_and_divide_series_into_n_chunks(series, total_chunks)
        self.assertEqual(len(chunks), 3)
        self.assertTrue(all(isinstance(chunk, pd.Series) for chunk in chunks))

if __name__ == '__main__':
    unittest.main()
