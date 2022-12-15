# Installation:

1. (Optional) Create a virtual environment:
`python -m venv .venv`

2. Install the required packages:
`pip install -r requirements.txt`

# Usage:

The program uses the following arguments:

`-v --validate`

Checks if the data file is valid for the script:
- The file can be successfully parsed
- All people have their names and e-mails set
- Each person's birth date is in a valid format and in the past

`-x --execute`

-  Goes through the list of people and sends them birthday reminders, with the exception of the birthday person
- The e-mail template is hardcoded
- The e-mail will be sent a week before the person's birthday

The settings for the SMTP server must be given in an `.env` file:
  `SMTP_SERVER`
  `SMTP_PORT`
  `SENDER_EMAIL`
  `API_KEY`

# Utilities:
  `add_cron_job.sh` - shell script that adds a cron job with the python script
  `remove_cron_job.sh` - shell script that removes the cron job
