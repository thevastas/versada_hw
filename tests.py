from main import dataframe_valid, find_birthdays
from datetime import datetime, timedelta
import pandas as pd
import unittest


class BaseClass:
    def _construct_data_dict(self) -> dict:
        data = {
            "name": ["John", "Peter", "Janet"],
            "email": ["a@b.com", "b@a.com", "c@d.com"],
            "birthdate": ["2000-01-01", "1999-01-01", "1998-01-01"],
        }
        return data


class TestDataFrameValidation(unittest.TestCase, BaseClass):
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


class TestFindBirthdays(BaseClass):
    def test_no_birthdays(self):
        data = self._construct_data_dict()
        for entry in data["birthdate"]:
            entry = datetime.today() + timedelta(days=8)
        df = pd.DataFrame(data)
        birthday_list = find_birthdays(df)
        assert birthday_list == []

    def test_find_birthdays(self):
        data = self._construct_data_dict()
        data["birthdate"][0] = (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")
        data["birthdate"][1] = (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")
        data["birthdate"][2] = (datetime.today() + timedelta(days=8)).strftime("%Y-%m-%d")
        df = pd.DataFrame(data)
        birthday_list = find_birthdays(df)
        assert birthday_list == [
            {"name": data["name"][0], "email": data["email"][0], "birthdate": data["birthdate"][0]},
            {"name": data["name"][1], "email": data["email"][1], "birthdate": data["birthdate"][1]},
        ]
