#!/usr/bin/env python

import sys
from graphs import Graph, dotpoint, dotcolor, welsh_powell, graph_report, sparsegraph, complete_graph
from time import time

if __name__ == '__main__':
    g = complete_graph(5)
    print(g)
    print('size =', g.size())
    print('order =', g.order())
    g.printnodes()
    g.printedges()
    g.printadjlis()
    print('adjacent(G, b, c) =', g.adjacent('b', 'c'))
    print('antiedge(G, b, c) =', g.antiedge('b', 'c'))
    print('neighbors(G, d) =', g.neighbors('d'))
    print('antiedges(G, d) =', g.antiedges('d'))
    print('writing 1.svg')
    dotcolor(g, welsh_powell(g), '1.svg')

    print('add node f')
    g.add_vertex('f')
    print(g)
    print('writing 2.svg')
    dotcolor(g, welsh_powell(g), '2.svg')

    print('remove node d')
    g.remove_vertex('d')
    print(g)
    print('writing 3.svg')
    dotcolor(g, welsh_powell(g), '3.svg')

    print('add edge {f,b}')
    g.add_edge('f', 'b')
    print(g)
    print('writing 4.svg')
    dotcolor(g, welsh_powell(g), '4.svg')

    print('remove edge {c,b}')
    g.remove_edge('c', 'b')
    print(g)
    print('writing 5.svg')
    dotcolor(g, welsh_powell(g), '5.svg')

    g = sparsegraph()
    graph_report(g)
    try:
        dotcolor(g, welsh_powell(g), 'sparse.svg')
    except Exception as error:
        sys.stderr.write('%s\n' % error)
        dotpoint(g, 'sparse.svg')
