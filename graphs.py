import os, subprocess, graphviz
from math import log
from random import randint, sample
from collections import namedtuple
from randnorm import randint_normal

letters = [ chr(i) for i in range(97,123) ]

def ltridx(ltr):
    return ord(ltr) - 97

Edge = namedtuple('Edge', ['x', 'y'])

class Graph:
    """Represents an undirected simple graph.
    attributes: adjlis
    """
    def __init__(self, nodes, edges):
        self.adjlis = { node: set() for node in nodes }
        for e in edges:
            self.adjlis[e.x].add(e.y)
            self.adjlis[e.y].add(e.x)

    def nodes(self):
        """Method returns graph's node list."""
        return [ v for v in self.adjlis ]

    def edges(self):
        """Method returns graph's edge set."""
        return { Edge(*sorted((x,y))) for x in self.adjlis for y in self.adjlis[x] }

    def size(self):
        """Method returns no. of edges in graph."""
        return sum( [ len(x) for x in self.adjlis.values() ] ) // 2

    def order(self):
        """Method returns no. of vertices in graph."""
        return len(self.adjlis)

    def density(self):
        """Method returns graph's density quotient."""
        m = self.size()
        n = self.order()
        return 2 * m / (n * (n - 1))

    def adjacent(self, x, y):
        """Tests whether there is an edge from vertex x to the vertex y."""
        return y in self.adjlis[x]

    def antiedge(self, x, y):
        """Tests whether there is not an edge from vertex x to the vertex y."""
        return not self.adjacent(x, y)

    def neighbors(self, x):
        """Lists all vertices y such that there is an edge from the vertex x to the vertex y."""
        return self.adjlis[x]

    def antiedges(self, x):
        """Lists all vertices y such that there is not an edge from the vertex x to the vertex y."""
        return set(self.nodes()).difference(self.adjlis[x])

    def add_vertex(self, x):
        """Adds the vertex x, if it is not there."""
        if x not in self.adjlis:
            self.adjlis[x] = set()

    def remove_vertex(self, x):
        """Remove the vertex x, if it is there."""
        self.adjlis.pop(x)
        for node in self.adjlis:
            if x in self.adjlis[node]:
                self.adjlis[node].remove(x)

    def add_edge(self, x, y):
        """Adds the edge from the vertex x to the vertex y if it is not there."""
        if self.antiedge(x, y):
            self.adjlis[x].add(y)
            self.adjlis[y].add(x)

    def remove_edge(self, x, y):
        """Removes the edge from the vertex x to the vertex y if it is there."""
        if self.adjacent(x, y):
            self.adjlis[x].remove(y)
            self.adjlis[y].remove(x)

    def degree(self, x):
        """Method returns no. of other vertices adjacent to the vertex x."""
        return len(self.adjlis[x])

    def degrees(self):
        """Method returns dictionary of the degrees of every vertex in the graph."""
        return dict( [ (k,self.degree(k)) for k in self.adjlis ] )

    def adjmat(self):
        """
        Method returns adjaceny matrix of graph.
        Vertices and edges can be integers or strings.
        """
        n = self.order()
        t = [ [ 0 ] * n for i in range(n) ]
        for edge in self.edges():
            if type(edge.x) is str and type(edge.y) is str:
                i, j = ltridx(edge.x), ltridx(edge.y)
            else:
                i, j = edge.x - 1, edge.y - 1
            t[i][j] = 1
            t[j][i] = 1
        return t

    def printnodes(self):
        print('{' + ','.join(self.nodes()) + '}')

    def printedge(self, e):
        print('{' + ','.join(e) + '}')

    def printedges(self):
        print('{'+','.join(['{'+','.join(e)+'}' for e in sorted(self.edges())])+'}')

    def printadjlis(self):
        for v in self.adjlis:
            print(str(v) + ': ' + ','.join(map(str, sorted(self.adjlis[v]))))

    def printadjmat(self):
        print('\n'.join(' '.join(str(j) for j in i) for i in self.adjmat()))

    def __str__(self):
        v = '{' + ','.join(map(str, self.nodes())) + '}'
        e = '{'+','.join(['{'+','.join(map(str, e))+'}' for e in sorted(self.edges())])+'}'
        return '(V,E) = (' + v + ',' + e + ')'

def complete_nodes(n):
    return letters[:n]

def complete_edges(v):
    """Function returns complete edges of givern vertices v."""
    return [ Edge(x,y) for x in v[:-1] for y in v[v.index(x) + 1:] ]

def complete_graph(n):
    """Function returns the complete graph of order n."""
    v = complete_nodes(n)
    e = complete_edges(v)
    return Graph(v, e)

def randgraph(n=randint(2, 26)):
    """Function returns pseudo-uniformly distributed graph."""
    maxm = (n * (n - 1)) // 2
    m = randint(1, maxm)
    v = letters[:n]
    e = sample(complete_edges(v), m)
    return Graph(v, e)

def sparsegraph(n=randint_normal(4,26)):
    """Function returns pseudo-normally distributed sparse graph."""
    maxm = round((n * (n - 1)) / 4 - 1)
    hi = round(n * log(n, 2))
    m = randint_normal(1, min(hi, maxm))
    v = letters[:n]
    e = sample(complete_edges(v), m)
    return Graph(v, e)

def dotpoint(g, filename):
    """Function creates line and point image file of graph g."""
    dot = graphviz.Graph(os.path.basename(filename))
    dot.attr('node', shape='point')
    #for node in g.nodes():
    #    dot.node(node)
    for edge in g.edges():
        dot.edge(edge.x, edge.y)
    output = dot.render(outfile=filename,engine='circo',cleanup=False)
    print(output)

def dotcolor(g, colors, filename):
    """Function creates image file of Welsh-Powell colored graph."""
    c = len( { v for v in colors.values() } )
    m = g.size()
    n = g.order()
    d = g.density()
    # label = 'colors = {:d}, size = {:d}, order = {:d}, density = {:.3f}'.format(c, m, n, d)
    dot = graphviz.Graph(os.path.basename(filename))
    # dot.attr(ratio='0.618')
    # dot.attr(pad='1')
    # dot.attr('graph',label=label)
    dot.attr('node', shape='circle',style='filled',height='0',width='0',margin='0')
    for node in colors:
        dot.node(node,fillcolor=colors[node])
    for edge in g.edges():
        dot.edge(edge.x, edge.y)
    output = dot.render(outfile=filename,engine='circo',cleanup=True)
    print(output)

#def descending_order(d):
#    return [ k for k,v in sorted(d.items(), key = lambda x: x[1], reverse=True) ]

# Welsh-Powell vertex coloring algorithm.
def welsh_powell(g):
    """Welsh-Powell graph vertex coloring algorithm."""
    colors = ['red','orange','yellow','green','blue','indigo','violet']
    d = g.adjlis
    # q = descending_order(g.degrees())
    q = [ k for k,v in sorted(g.degrees().items(), key = lambda x: x[1], reverse=True) if v > 0 ]
    color_dict = {}
    while len(q) > 0 and len(colors) > 0:
        node = q[0]
        t = [ v for v in q if v not in d[node] ]
        c = colors.pop(0)
        atc = []    # assigned this color
        for v in t:
            if any( [ v in d[x] for x in atc ] ):
                continue
            color_dict[v] = c
            atc.append(v)
            q.remove(v)
            if len(q) == 0:
                break
    if len(q) > 0:
        raise ValueError("not enough colors")
    return color_dict

def graph_report(g):
    # processing
    size = g.size()
    order = g.order()
    density = g.density()
    # output
    print(g)
    if density <= .5:
        g.printadjlis()
    if density >= .5:
        g.printadjmat()
    # for v, d in g.degrees().items():
        # print('degree({:s}) = {:d}'.format(str(v), d))
    # for v in g.nodes():
        # print(str(v) + ': ', g.antiedges(v))
    print('size = {:d}, order = {:d}, density = {:f}'.format(size, order, density))
