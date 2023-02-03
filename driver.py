#!/usr/bin/env python3

import sys, subprocess
from random import randint
from graphs import random_graph, dot_dump

def main():
    dot_dump(random_graph(randint(3, 12)))
    subprocess.run('dot -Tsvg graph.gv > graph.svg', shell=True)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        sys.stderr.write('%s\n' % error)
        sys.exit(1)
