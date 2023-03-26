#!/usr/bin/env python

import sys
from graphs import sparsegraph, graph_report, dotpoint, welsh_powell, dotcolor

def main():
    imagefile = 'graph.svg'
    g = sparsegraph()
    graph_report(g)
    try:
        dotcolor(g, welsh_powell(g), imagefile)
    except Exception as error:
        sys.stderr.write('%s\n' % error)
        dotpoint(g, imagefile)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        sys.stderr.write('%s\n' % error)
        sys.exit(1)
