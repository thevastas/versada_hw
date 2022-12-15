from main import dataframe_valid
import pandas as pd
import unittest


class TestDataFrameValidation(unittest.TestCase):
    def _construct_data_dict(self) -> dict:
        data = {
            "name": ["John", "Peter", "Janet"],
            "email": ["a@b.com", "b@a.com", "c@d.com"],
            "birthdate": ["2000-01-01", "1999-01-01", "1998-01-01"],
        }
        return data

    def test_dataframe_missing_column(self):
        data = {"name": ["John", "Peter", "Janet"], "email": ["a@b.com", "b@a.com", "c@d.com"]}
        df = pd.DataFrame(data)
        with self.assertRaises(ValueError):
            dataframe_valid(df)

    def test_dataframe_correct(self):
        data = self._construct_data_dict()
        df = pd.DataFrame(data)
        assert dataframe_valid(df)

    def test_dataframe_empty_value(self):
        data = self._construct_data_dict()
        data["name"][1] = None
        df = pd.DataFrame(data)
        with self.assertRaises(ValueError):
            dataframe_valid(df)

    def test_dataframe_wrong_date_format(self):
        data = self._construct_data_dict()
        data["birthdate"][1] = "01-01-1991"
        df = pd.DataFrame(data)
        with self.assertRaises(ValueError):
            dataframe_valid(df)

    def test_dataframe_date_in_future(self):
        data = self._construct_data_dict()
        data["birthdate"][1] = "2050-01-01"
        df = pd.DataFrame(data)
        with self.assertRaises(ValueError):
            dataframe_valid(df)
