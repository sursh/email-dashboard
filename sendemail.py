#! /usr/bin/env python

'''
    Sends an email with all the images in PICDIR displayed inline. Uses the
    Mailgun API for testing.

    To adjust recipients of this email, configure the 'dailyreports'
    mailing list at mailgun.com.

'''

import os
import requests
from werkzeug import MultiDict as MultiDict
from config_mailgun import MAILGUN_KEY, MAILGUN_FROM, MAILGUN_TO

POST_URL = 'https://api.mailgun.net/v2/refugeesunited.mailgun.org/messages'

PICDIR = 'temp'

def send_inline_image(imagelist):
    files = MultiDict()
    html = ['<html>']
    i = 1
    # this 'i' business is jank to work around a Multidict bug in Requests:
    # https://github.com/kennethreitz/requests/issues/1155
    for image in imagelist:
        files.add('inline[' + str(i) + ']', open(os.path.join(PICDIR, image)))
        html.append('<p>Inline image here: <img src="cid:%s" alt="%s"></p>' % (image, image)) #TODO make this alt text more readable
        i += 1
    html.append('</html>')

    return requests.post(
        POST_URL,
        auth=('api', MAILGUN_KEY),
        files=files,
        data={"from": MAILGUN_FROM,
              "to": MAILGUN_TO,
              "subject": "Daily Status Report",
              "text": "Daily snapshot of the Refugees United dashboard.",
              "html": ''.join(html),
              })

if __name__ == '__main__':

    imagelist = []
    for f in os.listdir(PICDIR):
        if f.endswith('.png'):
            imagelist.append(f)

    r = send_inline_image(imagelist)
    print r.text