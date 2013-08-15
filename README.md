# Email Stats Dashboard for DataKind

DataKind works with not-for-profits and NGOs to help them use their data to operate more effectively. 

This is an email dashboard that sends daily reports to the NGO staff. It takes in a JSON file and creates an email report. Text and tables are rendered in email-client-agnostic HTML, and plots are generated with matplotlib. Emails are sent with MailGun so the end user doesn't need to touch the code to adjust the recipient list. 

This dashboard is generalized such that DataKind will be able to use it across many projects. 