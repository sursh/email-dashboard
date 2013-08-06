#! /usr/bin/env python

'''
    Sends an email with all the images in IMAGEDIR displayed inline. Uses the
    Mailgun API for testing.

    To adjust recipients of this email, configure the 'dailyreports'
    mailing list at mailgun.com.

'''

import os
import requests
import json
from werkzeug import MultiDict as MultiDict
from config_mailgun import MAILGUN_KEY, MAILGUN_FROM, MAILGUN_TO
from config import DATAFILE, IMAGEDIR

POST_URL = 'https://api.mailgun.net/v2/refugeesunited.mailgun.org/messages'

def send_email():
    with open(DATAFILE, 'r') as f:
        wholefile = f.read()
        wholefile = json.loads(wholefile)

        files = MultiDict()
        html = ['<html>']
        # this 'i' business is jank to work around a Multidict bug in Requests:
        # https://github.com/kennethreitz/requests/issues/1155
        i = 1
        for graph in wholefile:
            if graph['type'] == 'table':
                pass
            elif graph['type'] == 'timeseries':
                pass
            elif graph['type'] == 'bar' and graph['data']:
                imagename = graph['uniquename'] + '.png'
                files.add('inline[' + str(i) + ']', open(os.path.join(IMAGEDIR, imagename)))
                i += 1
                html.append('<p>%s %s</p> <p><img src="cid:%s" alt="%s"></p>' % (graph['name'].title(), graph['additional'].title(), imagename, graph['name']+' graph'))

        html.append('</html>')

    return requests.post(
        POST_URL,
        auth=('api', MAILGUN_KEY),
        files=files,
        data={"from": MAILGUN_FROM,
              "to": MAILGUN_TO,
              "subject": "Daily Status Report yeahhhh",
              "text": "Daily snapshot of the Refugees United dashboard.",
              "html": ''.join(html),
              })

if __name__ == '__main__':

    r = send_email()
    print r.text