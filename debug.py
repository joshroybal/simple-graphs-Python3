#!/usr/bin/env python

import sys, os, random
import graphs

def main():
    # random graph
    print('random graph')
    g = graphs.random_graph()
    print(g)
    if g.density() <= .5:
        graphs.print_adjacency_dict(g)
    if g.density() >= .5:
        graphs.print_adjacency_matrix(g)
    print('size = {:d}, order = {:d}, density = {:f}'.format(g.size(), g.order(), g.density()))
    graphs.dot_point(g, 'random.svg')
    # complete graph
    print('complete graph')
    n = random.randint(2, 12)
    g = graphs.complete_graph(n)
    print(g)
    graphs.print_adjacency_matrix(g)
    print('size = {:d}, order = {:d}, density = {:f}'.format(g.size(), g.order(), g.density()))
    graphs.dot_point(g, 'complete.svg')
    # regular graph
    print('regular graph')
    n = random.randint(3, 26)
    g = graphs.regular_graph(n)
    print(g)
    if g.density() <= .5:
        graphs.print_adjacency_dict(g)
    if g.density() >= .5:
        graphs.print_adjacency_matrix(g)
    print('size = {:d}, order = {:d}, density = {:f}'.format(g.size(), g.order(), g.density()))
    graphs.dot_point(g, 'regular.svg')
    # sparse graph
    print('sparse graph')
    g = graphs.sparse_graph()
    print(g)
    graphs.print_adjacency_dict(g)
    print('size = {:d}, order = {:d}, density = {:f}'.format(g.size(), g.order(), g.density()))
    graphs.dot_point(g, 'sparse.svg')

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        sys.stderr.write('%s\n' % error)
        sys.exit(1)
