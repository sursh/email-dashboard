#! /usr/bin/env python

'''
    Sends an email with all the images in IMAGEDIR displayed inline. Uses the
    Mailgun API for testing.

    To adjust recipients of this email, configure the 'dailyreports'
    mailing list at mailgun.com.

'''

import sys
import os
import requests
import json
from werkzeug import MultiDict as MultiDict
from config_mailgun import MAILGUN_KEY, MAILGUN_FROM, MAILGUN_TO
from config import IMAGEDIR

DEBUG = False
POST_URL = 'https://api.mailgun.net/v2/refugeesunited.mailgun.org/messages'

def send_email(datafile):
    with open(datafile, 'r') as f:
        wholefile = f.read()
        wholefile = json.loads(wholefile)

        files = MultiDict()
        html = ['<html>\n']
        # this 'i' business is jank to work around a Multidict bug in Requests:
        # https://github.com/kennethreitz/requests/issues/1155
        i = 1
        for graph in wholefile:
            if graph['type'] == 'table':
                html.append('<h3>%s %s</h3>' % (graph['name'], graph['additional']))
                html.append('<table cellspacing="10" text-align="center">\n')
                html.append('<th>%s</th><th>%s</th>\n' % (graph['columns'][0], graph['columns'][1]))
                for row in graph['data']:
                    html.append('<tr><td>%s</td><td>%s</td></tr>\n' % (row[0], row[1]))
                html.append('</table>')
            elif graph['type'] == 'timeseries':
                pass
            elif graph['type'] == 'bar' and graph['data']:
                imagename = graph['uniquename'] + '.png'
                files.add('inline[' + str(i) + ']', open(os.path.join(IMAGEDIR, imagename)))
                i += 1
                html.append('<h3>%s %s</h3> <p><img src="cid:%s" alt="%s"></p>\n' % (graph['name'].title(), graph['additional'].title(), imagename, graph['name']+' graph'))

        html.append('</html>')

        if DEBUG: print ''.join(html)

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

    if len(sys.argv) != 2:
        print 'Usage: $ %s <inputFile>' % sys.argv[0]
        sys.exit(1)

    datafile = sys.argv[1]

    r = send_email(datafile)
    print r.text
