import argparse
from os import linesep
import pandas as pd
from datetime import datetime, timedelta


def dataframe_valid(dataframe: pd.DataFrame) -> bool:
    expected_columns = ["name", "email", "birthdate"]
    if not all([item in dataframe.columns.values for item in expected_columns]):
        raise ValueError("The data file is missing a required column.")
    if pd.isna(dataframe["name"]).any() or pd.isna(dataframe["email"]).any():
        raise ValueError("The data file contains empty values.")
    if not pd.to_datetime(dataframe["birthdate"], format="%Y-%m-%d", errors="coerce").notnull().all():
        raise ValueError("The date format of an entry in the data file is invalid.")
    for birthdate in dataframe["birthdate"]:
        if datetime.strptime(birthdate, "%Y-%m-%d") > datetime.today():
            raise ValueError("The birthdate in the data file is in the future.")
    return True


def read_datafile(filename: str) -> pd.DataFrame:
    # TODO raise exception for reading
    dataframe = pd.read_csv(filename)
    return dataframe


def find_birthdays(dataframe: pd.DataFrame, days_until_birthday: int = 7) -> list[dict]:
    birthday_people = []
    date_week_after = datetime.today() + timedelta(days=days_until_birthday)
    date_week_after_string = date_week_after.strftime("%Y-%m-%d")

    for index, row in dataframe.iterrows():
        birthdate = datetime.strptime(row["birthdate"], "%Y-%m-%d")
        if birthdate.month == date_week_after.month and birthdate.day == date_week_after.day:
            birthday_people.append(
                {
                    "name": row["name"],
                    "email": row["email"],
                    "celebrates_on": date_week_after_string,
                }
            )

    return birthday_people


def send_single_email(
    recipient: str, name_of_birthday_person: str, date: str, name: str, amount_of_days: int = 7, dry_run: bool = False
):
    subject = f"Birthday Reminder: {name_of_birthday_person} birthday on {date}"
    body = (
        f"Hi {name},{linesep}This is a reminder that {name_of_birthday_person} "
        + f"will be celebrating their birthday on {date}.{linesep}There are {amount_of_days} days left to get a present!"
    )
    if dry_run:
        print(f"to: {recipient}")
        print(f"subject: {subject}")
        print(f"body: {body}")
        print("---------")


def send_emails(birthday_people: list[dict], dataframe: pd.DataFrame):
    for birthday_person in birthday_people:
        for index, row in dataframe.iterrows():
            if not row["email"] == birthday_person["email"]:
                send_single_email(
                    recipient=row["email"],
                    name_of_birthday_person=birthday_person["name"],
                    date=birthday_person["celebrates_on"],
                    name=row["name"],
                    dry_run=True,
                )


parser = argparse.ArgumentParser(description="Birthday program")
parser.add_argument(
    "-v", "--validate", type=str, nargs=1, metavar="file_name", default=None, help="Opens and validates the input file."
)
parser.add_argument(
    "-x",
    "--execute",
    type=str,
    nargs=1,
    metavar="file_name",
    default=None,
    help="Sends birthday reminders to people that are present in the input file.",
)

if __name__ == "__main__":
    args = parser.parse_args()
    dataframe = pd.DataFrame()
    if args.validate != None:
        try:
            dataframe = read_datafile(args.validate[0])
            dataframe_valid(dataframe)
        except ValueError as err:
            print(err)
    if args.execute != None:
        dataframe = read_datafile(args.execute[0])
        birthday_list = find_birthdays(dataframe)
        send_emails(birthday_list, dataframe)
