import argparse
import pandas as pd


def dataframe_valid(dataframe):
    expected_columns = ["name", "email", "birthdate"]
    if not all([item in dataframe.columns.values for item in expected_columns]):
        raise ValueError("The data file is missing a required column.")
    if pd.isna(dataframe["name"]).any() or pd.isna(dataframe["email"]).any():
        raise ValueError("The data file contains empty values.")
    if not pd.to_datetime(dataframe["birthdate"], format="%Y-%m-%d", errors="coerce").notnull().all():
        raise ValueError("The date format is invalid.")
    for date in dataframe["birthdate"]:
        if pd.DatetimeIndex([date]) > pd.Timestamp.now():
            raise ValueError("The birthdate is in the future.")
    return True


def file_valid(filename):
    # TODO raise exception for reading
    dataframe = pd.read_csv(filename)
    dataframe_valid(dataframe)
    return True


parser = argparse.ArgumentParser(description="Birthday program")
parser.add_argument(
    "-v", "--validate", type=str, nargs=1, metavar="file_name", default=None, help="Opens and validates the input file."
)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.validate != None:
        try:
            file_valid(args.validate[0])
        except ValueError as err:
            print(err)
