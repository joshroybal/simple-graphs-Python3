from random import choice

labels = [ chr(i) for i in range(65, 91) ]

def vertices(n):
    return labels[:n]

def random_edges(vertices):
    n = len(vertices)
    v = list(vertices)
    edges = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            if choice([ True, False ]):
                edges.append( ( labels[i], labels[j] ) )
    return edges

def random_graph(n):
    v = vertices(n)
    return [ v, random_edges(v) ]

def adjacency_dict(g):
    d = dict()
    v, e = g
    for i in v:
        d[i] = []
        for j in e:
            if i in j:
                d[i].extend([ k for k in j if k is not i ])
    return d

def ltridx(c):
    return ord(c) - 65

def adjacency_matrix(g):
    v, e = g
    n = len(v)
    t = [ n * [ 0 ] for i in range(n) ]
    for edge in e:
        c1, c2 = edge
        i = ltridx(c1)
        j = ltridx(c2)
        t[i][j] = 1
        t[j][i] = 1
    return t

def dot_dump(g):
    colors = [ 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet' ]
    #c = ' node [fillcolor=green] '
    nodes = g[0]
    edges = g[1]
    idx = 0
    fillcolors = '\n'
    for node in nodes:
        fillcolors += '"' + node + '" [fillcolor=' + colors[idx] + ']\n'
        idx = (idx + 1) % 7
    print(fillcolors)
    s = 'graph { layout=circo; node [ shape=circle height=0 width=0 margin=0 \
style=filled ] ratio=0.618; pad=1.0;'
    idx = 0
    for edge in edges:
        idx = (idx + 1) % 7
        s += ' ' + str(edge[0]) + ' -- ' + str(edge[1]) + ' '
    s += fillcolors
    s += ' }'
    print(s)
    f = open('graph.gv', 'w')
    f.write(s)
    f.close()
