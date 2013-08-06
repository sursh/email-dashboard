#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import json
import string
import os

DEBUG = False
DATAFILE = '../data/old_but_good.json'
BINS = 10

with open(DATAFILE, 'r') as f:
    wholefile = f.read()
    wholefile = json.loads(wholefile)
    # wholefile is now a list, each element being a dict for one graph

    # set up folder for pics
    os.mkdir('temp')

    for graph in wholefile:

        if DEBUG: print "Starting with this graph: \n", graph, '\n'
        barheights = [int(y) for y in graph['data'].split(',')]
        barheights = barheights[:BINS]

        bottom = 0
        barwidth = 1
        xlocations = np.arange(len(barheights))

        plt.bar(xlocations, barheights, barwidth, bottom)
        plt.title(graph['name'] + ' ' + graph['additional'])
        plt.xlabel("Times Logged In")
        plt.ylabel("People")

        exclude = set(string.punctuation)
        filename = ''.join(char for char in graph['name'] + graph['additional'] if char not in exclude).replace(' ', '')
        filename = filename + ".png"
        plt.savefig(filename)
        if DEBUG: print "Created file %s" % filename

        plt.clf()
