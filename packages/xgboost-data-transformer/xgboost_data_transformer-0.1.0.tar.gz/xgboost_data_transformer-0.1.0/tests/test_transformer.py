# tests/test_transformer.py
import unittest
import pandas as pd
import os
import sys

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from xgboost_data_transformer.transformer import XGBoostDataTransformer

class TestXGBoostDataTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = XGBoostDataTransformer()
        self.data = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': ['x', 'y', 'z', None],
            'C': [1.5, 2.5, 3.5, None]
        })

    def test_transform(self):
        transformed_data = self.transformer.transform(self.data)
        self.assertTrue(transformed_data['B'].dtype.name == 'category')
        self.assertFalse(transformed_data.isnull().values.any())
        print(transformed_data)

if __name__ == '__main__':
    unittest.main()
