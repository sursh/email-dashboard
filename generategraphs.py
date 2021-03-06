#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import json
import string
import os
import sys
import logging
from datetime import datetime
from config import IMAGEDIR

BINS = 10
logging.basicConfig(level=logging.INFO)

def generate_graphs(datafile):
    with open(datafile, 'r') as f:
        wholefile = f.read()
        wholefile = json.loads(wholefile)
        
        # set up folder for pngs
        try:
            os.chdir(IMAGEDIR)
        except:
            os.mkdir(IMAGEDIR)
            os.chdir(IMAGEDIR)

        for graph in wholefile:

            logging.debug("Graphing %s." % graph['uniquename'])

            if graph['type'] == 'bar' and graph['data']:

                d = graph['data']
                # cast the keys from strings to ints
                d = { int(k):d[k] for k in d.keys() }

                # store dict's values in array for graphing
                barheights = []
                for i in range(1, max(d.keys())+1):
                    barheights.append(d.get(i, 0))
                barheights = barheights[:BINS]

                bottom = 0
                barwidth = 1
                xlocations = np.arange(len(barheights))

                fig = plt.figure()
                plt.bar(
                    xlocations,
                    barheights,
                    barwidth,
                    bottom,
                    color=(.4,.4,.4),
                    linewidth=0,
                )

                # graph labels
                plt.suptitle(graph.get('name', ''), fontsize=14)
                plt.title(graph.get('additional', ''), fontsize=10)
                plt.xlabel(graph['xlabel'])
                plt.ylabel(graph['ylabel'])

                # remove right&top axes&ticks
                ax = fig.gca()
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.tick_params(top=False, right=False)
                ax.set_xticks(np.arange(BINS) + barwidth/2.)
                ax.set_xticklabels(d.keys()[:BINS])

                # this may be a more robust solution:
                # http://matplotlib.org/faq/howto_faq.html#automatically-make-room-for-tick-labels
                fig.set_size_inches(6,4.5)
                filename = graph['uniquename'] + '.png'
                plt.savefig(filename, dpi=80)
                logging.info("Created file %s" % filename)

                plt.clf()

            elif graph['type'] == 'timeseries' and graph['data']:
                d = graph['data']

                fig = plt.figure()
                x = [datetime.strptime(key, "%Y-%m-%d") for key in sorted(d.keys())]
                y = [d[key] for key in sorted(d.keys())]
                plt.plot(x, y, 'o-')
                fig.autofmt_xdate()

                # labels
                plt.suptitle(graph.get('name', ''), fontsize=14)
                plt.title(graph.get('additional', ''), fontsize=10)
                plt.ylabel(graph['ylabel'])

                # save and resize image file
                fig.set_size_inches(6,4.5)
                filename = graph['uniquename'] + '.png'
                plt.savefig(filename, dpi=80)
                logging.info("Created file %s" % filename)

                plt.clf()

            else:
                message = 'Did NOT create graph for "%s" (type: %s) ' % (graph['uniquename'], graph['type'])
                if not graph['data']: message += 'because it didn\'t contain any data'
                else: message += 'because it\'s not a supported graph type'
                logging.error(message)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Usage: $ %s <inputFile>' % sys.argv[0]
        sys.exit(1)

    datafile = sys.argv[1]

    generate_graphs(datafile)
