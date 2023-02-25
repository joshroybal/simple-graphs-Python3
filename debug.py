#!/usr/bin/env python3

import sys, subprocess
from random import randint
from graphs import random_graph, print_adjacency_dict,\
print_adjacency_matrix, dot_point, dot_color, graphstr, dotlists

def main(n):
    if n > 20:
        print('Graphs with more than 20 nodes not implemented.')
        return
    g = random_graph(n)
    print(graphstr(g))
    print_adjacency_dict(g)
    print_adjacency_matrix(g)
    dot_point(g, 'point.gv')
    dot_color(g, 'color.gv')
    dotlists(g)
    subprocess.run('dot -Tpng point.gv > point.png', shell=True)
    subprocess.run('dot -Tpng color.gv > color.png', shell=True)
    subprocess.run('./convert.sh')
    subprocess.run('geeqie', shell=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage %s n\n' % sys.argv[0])
        sys.exit(1)
    try:
        main(int(sys.argv[1]))
    except Exception as error:
        sys.stderr.write('%s\n' % error)
        sys.exit(1)
