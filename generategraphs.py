#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import json
import string
import os

DEBUG = True
DATAFILE = 'data/new.json'
BINS = 10

with open(DATAFILE, 'r') as f:
    wholefile = f.read()
    wholefile = json.loads(wholefile)
    # wholefile is now a list, each element being a dict for one graph

    # set up folder for pngs
    try:
        os.chdir('temp')
    except:
        os.mkdir('temp')
        os.chdir('temp')

    for graph in wholefile:

        if DEBUG: print "Starting with this graph: \n", graph, '\n'

        d = graph['data']
        # cast the keys from strings to ints
        for key in d.keys():
            d[int(key)] = d[key]
            del(d[key])

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
        plt.suptitle(graph['name'], fontsize=14)
        plt.title(graph['additional'], fontsize=10)
        plt.xlabel(graph['xlabel'])
        plt.ylabel(graph['ylabel'])

        # remove right&top axes&ticks
        ax = fig.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.tick_params(top=False, right=False)

        # this may be a more robust solution:
        # http://matplotlib.org/faq/howto_faq.html#automatically-make-room-for-tick-labels
        fig.set_size_inches(6,4.5)
        filename = graph['uniquename'] + '.png'
        plt.savefig(filename, dpi=80)
        if DEBUG: print "Created file %s" % filename

        plt.clf()
