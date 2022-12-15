Installation:

(Optional) Create a virtual environment:
python -m venv .venv
Install the required packages:
pip install -r requirements.txt

Usage:

The program uses the following arguments:

-v --validate

Checks if the data file is valid for the script:
1. The file can be successfully parsed
2. All people have their names and e-mails set
3. Each person's birth date is in a valid format and in the past

-x --execute

Goes through the list of people and sends them birthday reminders, with the exception of the birthday person
The e-mail template is hardcoded
The e-mail will be sent a week before the person's birthday
