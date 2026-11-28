# Author: Aria Deligero
# Purpose: Tests the SurveyDataset implementation.
# Responsibility: Verify dataset creation, data handling,
# and expected dataset behavior.
# Notes: Include valid and invalid dataset scenarios.

import unittest

import pandas as pd

from surveytsek.dataset import SurveyDataset


class TestSurveyDataset(unittest.TestCase):
    def test_rows_and_columns(self):
        dataset = SurveyDataset(pd.DataFrame({"id": [101, 102], "rating": [5, 3]}))
        self.assertEqual(len(dataset), 2)
        self.assertEqual(dataset.get_columns(), ["id", "rating"])

    def test_original_data_is_protected(self):
        original = pd.DataFrame({"rating": [5]})
        dataset = SurveyDataset(original)
        original.loc[0, "rating"] = 1
        self.assertEqual(dataset.get_data().loc[0, "rating"], 5)
        copied = dataset.get_data()
        copied.loc[0, "rating"] = 2
        self.assertEqual(dataset.get_data().loc[0, "rating"], 5)

    def test_rejects_non_dataframe(self):
        with self.assertRaises(TypeError):
            SurveyDataset([1, 2, 3])


if __name__ == "__main__":
    unittest.main()
