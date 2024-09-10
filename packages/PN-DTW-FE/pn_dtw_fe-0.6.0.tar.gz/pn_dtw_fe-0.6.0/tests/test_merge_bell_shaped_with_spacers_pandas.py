import unittest
import pandas as pd
import numpy as np
from PN_DTW_FE.merge_bell_shaped_with_spacers_pandas import merge_bell_shaped_with_spacers_pandas

class TestMergeBellShapedWithSpacersPandas(unittest.TestCase):
    def test_merge_bell_shaped_with_spacers_pandas(self):
        original_chunks = [pd.Series([1, 2, 3]), pd.Series([4, 5, 6]), pd.Series([7, 8, 9])]
        bell_shaped_chunks = [pd.Series([2, 3]), pd.Series([5, 6]), pd.Series([8, 9])]
        final_chunks = merge_bell_shaped_with_spacers_pandas(original_chunks, bell_shaped_chunks)
        self.assertTrue(isinstance(final_chunks, pd.Series))
        self.assertEqual(len(final_chunks), sum(len(chunk) for chunk in original_chunks) + sum(len(chunk) for chunk in bell_shaped_chunks))

if __name__ == '__main__':
    unittest.main()
