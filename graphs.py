from random import choice

labels = [ chr(i) for i in range(97, 122) ]

def ltridx(c):
    return ord(c) - 97

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

def print_adjacency_dict(d):
    for k in d:
        print(k + ': ', end='')
        for v in d[k]:
            print('[' + v + '|-]--> ', end='')
        print('|/|')

def degree(node, graph):
    d = adjacency_dict(graph)
    return len(d[node])

def degrees(g):
    d = adjacency_dict(g)
    return [ degree(k, g) for k in d ]

def ordered_degrees(g):
    d = adjacency_dict(g)
    return sorted([ (k, len(d[k])) for k in d ], key = lambda x: x[1], reverse=True)

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

def print_adjacency_matrix(m):
    for row in m:
        for col in row:
            print(col, end=' ')
        print()

def color_queue(g):
    return [ i[0] for i in ordered_degrees(g) ]

def non_adjacent(v, d):
    return list(set([ key for key in d ]) - set(d[v]))

def all_non_adjacent(node, t, adjdict):
    for v in t:
        if node in adjdict[v]:
            return False
    return True

def paint(g):
    colors = ['red','orange','yellow','green','blue','indigo','violet']
    q = color_queue(g)
    d = adjacency_dict(g)
    nodes = g[0]
    color_dict = {}
    while len(q) > 0:
        node = q[0]
        t = non_adjacent(node, d)
        c = choice(colors)
        colors.remove(c)
        for v in t:
            if v in q and all_non_adjacent(v, t, d) == True:
                color_dict[v] = c
                q.remove(v)
                if len(q) == 0: break
    return color_dict

def dot_dump(g):
    nodes = g[0]
    edges = g[1]
    idx = 0
    for node in nodes:
        idx = (idx + 1) % 7
    s = 'graph { layout=circo; node [ shape=circle margin=0 height=0 width=0 style=filled ]'
    idx = 0
    for edge in edges:
        idx = (idx + 1) % 7
        s += ' ' + str(edge[0]) + ' -- ' + str(edge[1]) + ' '
    s += '\n'
    fillcolors = paint(g)
    for key in fillcolors:
        s += key + ' [fillcolor=' + fillcolors[key] + ']\n'
    s += ' }'
    print(s)
    f = open('graph.gv', 'w')
    f.write(s)
    f.close()
    print('graph data dumped to file graph.gv')
