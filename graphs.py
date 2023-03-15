import math, os, subprocess, graphviz
from random import choice, randint, sample
from randnorm import randint_normal, randint_lognormal

labels = [ chr(i) for i in range(ord('a'), ord('a') + 26) ]

# class Edge:
    # def __init__(self, v1, v2):
        # self.v1, self.v2 = v1, v2
    # def __str__(self):
        # return '{' + self.v1 + ',' + self.v2 + '}'

class Graph:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges

    def size(self):
        return len(self.edges)

    def order(self):
        return len(self.nodes)

    def density(self):
        m = len(self.edges)
        n = len(self.nodes)
        return 2*m / (n*(n-1))

    def adjacent(self, x, y):
        return (x, y) in self.edges or (y, x) in self.edges

    def neighbors(self, x):
        return [ y for y in self.nodes if self.adjacent(x, y) ]

    def adjacency_dict(self):
        return dict( [ (v, self.neighbors(v)) for v in self.nodes ] )

    def adjacency_matrix(self):
        t = [ self.order() * [ 0 ] for i in range(self.order()) ]
        for edge in self.edges:
            c1, c2 = edge
            i = ltridx(c1)
            j = ltridx(c2)
            t[i][j] = 1
            t[j][i] = 1
        return t

    def degree_dict(self):
        adjlis = self.adjacency_dict()
        return dict([ (k,len(adjlis[k])) for k in adjlis ])

    def __str__(self):
        return '(V,E) = ({'+','.join([v for v in self.nodes]) + '},\
{'+','.join(['{'+','.join([v for v in e])+'}' for e in self.edges])+'})'

def ltridx(c):
    return ord(c) - 97

def idxltr(i):
    return chr(97 + i)

def complete_edges(v):
    n = len(v)
    return [ tuple(map(idxltr, (i,j))) for i in range(n) for j in range(i+1,n) ]

def complete_graph(n):
    return Graph(labels[:n], complete_edges(labels[:n]))

def regular_edges(nodes):
    n = len(nodes)
    #t = [ (nodes[0], nodes[1]), (nodes[0], nodes[-1]) ]
    #for i in range(1, n - 1):
    #    t.append((nodes[i], nodes[i+1]))
    #return t
    return sorted( [ tuple(sorted( [ nodes[i],nodes[(i+1)%n ] ] ) ) for i in range(n) ] )

def regular_graph(n):
    return Graph(labels[:n], regular_edges(labels[:n]))

def random_edges(v):
    n = len(v)
    m = randint(1, (n * (n - 1)) / 2)
    return sorted(sample(complete_edges(v), m))

def random_graph():
    n = randint(2, 26)
    return Graph(labels[:n], random_edges(labels[:n]))

# sort of log normal distributed sparse graphs...
def sparse_graph():
    n = randint(4, 26)
    maximum = n * (n - 1) / 2
    lo = 1
    hi = math.ceil(maximum/2) - 1
    m = randint_normal(lo, hi)
    return Graph(labels[:n], sorted(sample(complete_edges(labels[:n]), m)))

def print_adjacency_dict(g):
    d = g.adjacency_dict()
    for k in d:
        print(k + ': ', end='')
        for v in d[k]:
            print(v, end='')
            if v != d[k][-1]:
                print(',', end='')
        print()

def degree(node, g):
    return g.degree_dict()[node]

def descending_order(d):
    return [ k for k,v in sorted(d.items(), key = lambda x: x[1], reverse=True) ]

def print_adjacency_matrix(g):
    m = g.adjacency_matrix()
    for row in m:
        for col in row:
            print(col, end=' ')
        print()

def non_adjacent(v, d):
    return list(set([ key for key in d ]) - set(d[v]))

def all_non_adjacent(node, t, adjdict):
    for v in t:
        if v in adjdict[node]:
            return False
    return True

def colornodes(g):
    colors = ['red','orange','yellow','green','blue','indigo','violet',\
    'powderblue','steelblue','slateblue','slategray','gray','forestgreen',\
    'brown','olive','cyan']
    c0 = len(colors)
    d = g.adjacency_dict()
    q = descending_order(g.degree_dict())
    color_dict = {}
    while len(q) > 0 and len(colors) > 0:
        node = q[0]
        t = non_adjacent(node, d)
        c = colors.pop(0)
        atc = [ ]    # assigned this color
        for v in q:
            if v in t and all_non_adjacent(v, atc, d) == True:
                color_dict[v] = c
                atc.append(v)
                #q.remove(v)
                if len(q) == 0: break
        for v in atc:
            q.remove(v)
    if len(q) > 0:
        raise ValueError("not enough colors")
    print('no. of colors assigned:', c0 - len(colors))
    return color_dict

def dot_point(g, filename):
    dot = graphviz.Graph(os.path.basename(filename))
    dot.attr('node', shape='point')
    for node in g.nodes:
        dot.node(node)
    for edge in g.edges:
        dot.edge(edge[0], edge[1])
    output = dot.render(outfile=filename,engine='circo',cleanup=True)
    print(output)

def dot_color(g, colors, filename):
    dot = graphviz.Graph(os.path.basename(filename))
    # dot.attr(ratio='0.618')
    # dot.attr(pad='1')
    dot.attr('node', shape='circle',style='filled',height='0',width='0',margin='0')
    for node in colors:
        dot.node(node,fillcolor=colors[node])
    for edge in g.edges:
        dot.edge(edge[0], edge[1])
    output = dot.render(outfile=filename,engine='circo',cleanup=True)
    print(output)

def dotlists(g, colors):
    d = g.adjacency_dict()
    for k in d:
        filename = 'list' + str(k)
        dotlist(d[k], filename, k, colors)
    subprocess.run('convert list*.png -append adjlist.png', shell=True)
    subprocess.run('rm list*.png', shell=True)

def dotlist(t, filename, title, colors):
    dot = graphviz.Digraph(filename)
    dot.attr(rankdir='LR')
    dot.attr('node',shape='record',style='filled')
    dot.attr('edge',tailclip='false')

    for node in t:
        dot.node(node,fillcolor=colors[node])
        string = '{<data>'+node+'|<ref>}'
        dot.node(node,label=string)

    dot.attr('node',shape='box',fillcolor=colors[title])
    if len(t) > 0:
        dot.edge(title + ':e', t[0])
        for idx, ele in enumerate(t[:-1]):
            v1 = t[idx] + ':ref:c'
            v2 = t[idx+1]
            dot.edge(v1,v2,arrowtail='dot',dir='both')
    else:
        dot.node(title,tailclip='true',arrowhead='vee',arrowtail='dot',dir='both')

    filename = os.path.basename(filename) + '.png'
    dot.render(cleanup=True,outfile=filename)
