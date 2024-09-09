import unittest
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import List, Tuple
from ivers.temporal import leaky_endpoint_split, leaky_folds_endpoint_split
import os
import shutil
import tempfile
from unittest.mock import patch

class TestLeakyFoldsEndpointSplit(unittest.TestCase):
    def setUp(self):
        """Set up the DataFrame and parameters for the tests."""
        self.data = {
            'smiles': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
            'date_1': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01', '2020-06-01', '2020-07-01', '2020-08-01', '2020-01-01'],
            'date_2': ['2020-01-15', '2020-02-15', '2020-03-15', '2020-04-15', '2020-05-15', '2020-06-15', '2020-07-15', '2020-08-15', '2020-09-15'],
            'value_1': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'value_2': [10, None, 30, None, 50, None, 70, 80, 90],
            'feature_1': [10, 20, 30, 40, 50, 60, 70, 80, 90],
            'feature_2': [100, 200, 300, 400, 500, 600, 700, 800, 900]
        }
        self.df = pd.DataFrame(self.data)
        self.num_folds = 5
        self.smiles_column = 'smiles'
        self.endpoint_date_columns = {'value_1': 'date_1', 'value_2': 'date_2'}
        self.exclude_columns = ['feature_2']
        self.chemprop = False
        self.save_path = tempfile.mkdtemp()  # Using tempfile for testing to avoid directory issues

    def tearDown(self):
        """Remove all .csv files and the directory after the test is done."""
        shutil.rmtree(self.save_path)
        print(f"Deleted directory and all files in: {self.save_path}")

    def test_splits(self):
        """Test the training/test splits to ensure proper handling, including checks for compound 'C9'."""
        # Execute the function
        result = leaky_folds_endpoint_split(self.df, self.num_folds, self.smiles_column, self.endpoint_date_columns, self.exclude_columns, self.chemprop, self.save_path)

        # Assert the results
        self.assertEqual(len(result), self.num_folds, "Incorrect number of folds returned.")
        found_in_train = found_in_test = False
        for train, test in result:
            # Check presence of 'C9' in both train and test sets
            if 'C9' in train[self.smiles_column].values:
                found_in_train = True
            if 'C9' in test[self.smiles_column].values:
                found_in_test = True

        self.assertTrue(found_in_train, "'C9' not found in any train set across all folds.")
        self.assertTrue(found_in_test, "'C9' not found in any test set across all folds.")

if __name__ == '__main__':
    unittest.main()
