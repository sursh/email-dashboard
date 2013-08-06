#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import json
import string
import os

DEBUG = False
DATAFILE = 'data/old_but_good.json'
BINS = 10

with open(DATAFILE, 'r') as f:
    wholefile = f.read()
    wholefile = json.loads(wholefile)
    # wholefile is now a list, each element being a dict for one graph

    # set up folder for pics
    try:
        os.chdir('temp')
    except:
        os.mkdir('temp')
        os.chdir('temp')

    for graph in wholefile:

        if DEBUG: print "Starting with this graph: \n", graph, '\n'
        barheights = [int(y) for y in graph['data'].split(',')]
        barheights = barheights[:BINS]

        bottom = 0
        barwidth = 1
        xlocations = np.arange(len(barheights))

        fig = plt.figure()
        plt.bar(xlocations, barheights, barwidth, bottom)
        plt.suptitle(graph['name'], fontsize=14)
        plt.title(graph['additional'], fontsize=10)
        plt.xlabel("Times Logged In")
        plt.ylabel("People")

        exclude = set(string.punctuation)
        filename = ''.join(char for char in graph['name'] + graph['additional'] if char not in exclude).replace(' ', '')
        filename = filename + ".png"

        # this may be a more robust solution:
        # http://matplotlib.org/faq/howto_faq.html#automatically-make-room-for-tick-labels
        fig.set_size_inches(6,4.5)
        plt.savefig(filename, dpi=80)
        if DEBUG: print "Created file %s" % filename

        plt.clf()
