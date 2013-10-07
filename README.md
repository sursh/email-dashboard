# Email Stats Dashboard for DataKind

[DataKind](datakind.org) connects volunteer data scientists with not-for-profits and NGOs to help them use their data to operate more effectively. 

This is an email dashboard that sends daily reports to the NGO/nonprofit staff. Getting reports by email saves them time and increases the usefulness of the data. 

This frontend takes in a JSON file (created by a separate backend) and creates an email report. Text and tables are rendered in email-client-agnostic HTML, and PNG plots are generated with matplotlib. Emails are sent with MailGun so the end user doesn't need to touch the code to adjust the recipient list. 

It's low-maintenance and lightweight, with little to configure and maintain. There is no archiving or database at this level, relying on the backend for history. 

# Usage

1. Set up your virtual environment and install your dependencies with `pip install -r requirements.txt`. Note that sometimes it takes a few attempts to get all of the dependencies installed properly. 

1. Configure your backend to put its JSON output in the directory specified in `config.py`. 

1. Rename `_config_mailgun.py` to `config_mailgun.py` (removing the leading underscore) and add your Mailgun credentials. Emails will be sent to the list specified here, so head to [Mailgun's site](mailgun.com) and add or remove recipients from the email list. This config file is ignored by your .gitignore. 

1. `generategraphs.py` will generate any graph images needed. `sendemail.py` will populate the template and send the email via Mailgun. Configure a cron job to run these in sequence once a week. 