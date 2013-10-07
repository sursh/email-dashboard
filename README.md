## This is for a specific client. The generalized version is [here](https://github.com/sursh/email-dashboard).

# Email Stats Dashboard for a DataKind Client

DataKind works with not-for-profits and NGOs to help them use their data to operate more effectively. 

This is an email dashboard that sends daily reports to the NGO staff. It takes in a JSON file and creates an email report. Text and tables are rendered in email-client-agnostic HTML, and plots are generated with matplotlib. Emails are sent with MailGun so the end user doesn't need to touch the code to adjust the recipient list. 

# Usage

Set up your virtual environment and install your dependencies with `pip install -r requirements.txt`. Note that sometimes it takes a few attempts to get all of the dependencies installed properly. 

Configure your backend to put its JSON output in the directory specified in `config.py`. Add your Mailgun credentials to `config_mailgun.py`. Emails will be sent to the list specified here, so head to [Mailgun's site](mailgun.com) and add or remove recipients from the email list. 

`generategraphs.py` will generate any graph images needed. `sendemail.py` will populate the template and send the email via Mailgun. Configure a cron job to run these in sequence once a week. 