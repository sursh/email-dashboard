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
import logging
from werkzeug import MultiDict as MultiDict
from config_mailgun import MAILGUN_KEY, MAILGUN_FROM, MAILGUN_TO, POST_URL, SUBJECT
from config import IMAGEDIR
from jinja2 import Environment, PackageLoader

logging.basicConfig(level=logging.INFO)

def send_email(datafile):
  
    env = Environment(loader=PackageLoader('sendemail', 'templates'))
    template = env.get_template('email.html')
    
    with open(datafile, 'r') as f:
        wholefile = f.read()
        wholefile = json.loads(wholefile)

        files = MultiDict()
        # this 'i' business is jank to work around a Multidict bug in Requests:
        # https://github.com/kennethreitz/requests/issues/1155
        i = 1

        context = list()
        
        for graph in wholefile:
            points = list()
            
            if graph['type'] == 'table':
                for row in graph['data']:
                    points.append((row[0], row[1]))
                
                currentgraph = { 
                                    'type' : 'table',
                                    'title' : graph['name'].title(), 
                                    'additional' : graph['additional'].title(), 
                                    'col1' : graph['columns'][0],
                                    'col2' : graph['columns'][1],
                                    'points' : points,
                                }
                
            elif graph['type'] == 'timeseries' or (graph['type'] == 'bar' and graph['data']):
                imagename = graph['uniquename'] + '.png'
                files.add('inline[%s]' % str(i), open(os.path.join(IMAGEDIR, imagename)))
                i += 1
                currentgraph = {
                                    'type' : 'imagegraph',
                                    'title' : graph['name'].title(),
                                    'additional' : graph.get('additional', '').title(),
                                    'cid' : imagename,
                                    'alt' : '%s graph' % graph['name'],
                                    }
            
            context.append(currentgraph)
        
    return requests.post(
                        POST_URL,
                        auth=('api', MAILGUN_KEY),
                            files=files,
                            data={"from": MAILGUN_FROM, 
                                "to": MAILGUN_TO,
                                "subject": SUBJECT,
                                "text": "Analytics by email.",
                                "html": template.render(context=context),
                                })

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Usage: $ %s <inputFile>' % sys.argv[0]
        sys.exit(1)

    datafile = sys.argv[1]

    r = send_email(datafile)
    logging.info(r.text)