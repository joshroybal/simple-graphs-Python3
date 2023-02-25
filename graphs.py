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

def print_adjacency_dict(g):
    d = adjacency_dict(g)
    for k in d:
        print(k + ': ', end='')
        for v in d[k]:
            print(v, end='')
            if v != d[k][-1]:
                print(',', end='')
        print()

def adjlist_str(g):
    d = adjacency_dict(g)
    s = ''
    for k in d:
        s += k + ': '
        for v in d[k]:
            s += v
            if v != d[k][-1]:
                s += ','
        s += '\n'
    return s

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

def print_adjacency_matrix(g):
    m = adjacency_matrix(g)
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

def colornodes(g):
    colors = ['red','orange','yellow','green','blue','indigo',\
    'violet','brown','coral','cyan','maroon','gold','silver',\
    'powderblue','midnightblue','steelblue','slateblue','slategray',\
    'gray','white']
    c0 = len(colors)
    q = color_queue(g)
    d = adjacency_dict(g)
    nodes = g[0]
    color_dict = {}
    while len(q) > 0 and len(colors) > 0:
        node = q[0]
        t = non_adjacent(node, d)
        c = colors.pop(0)
        atc = []    # assigned this color
        for v in t:
            if v in q and all_non_adjacent(v, atc, d) == True:
                color_dict[v] = c
                atc.append(v)
                q.remove(v)
                if len(q) == 0: break
    #print('no. of colors assigned:', c0 - len(colors))
    return color_dict

def dot_point(g, filename):
    nodes = g[0]
    edges = g[1]
    s = 'graph { node [ shape=point ]'
    for edge in edges:
        s += ' ' + str(edge[0]) + ' -- ' + str(edge[1]) + ' '
    s += '\n'
    s += ' }'
    outfile = open(filename, 'w')
    outfile.write(s)
    outfile.close()
    #print('graphviz dot data written to file', filename)

def dot_color(g, filename):
    nodes = g[0]
    edges = g[1]
    nodecolors = colornodes(g)
    s = 'graph {\n'
    s += 'layout=circo; ratio=0.618; pad=1.0;\n'
    #s += 'layout=circo;\n'
    s += 'node [shape=circle margin=0 height=0 width=0 style=filled]\n'
    for edge in edges:
        s += ' ' + str(edge[0]) + ' -- ' + str(edge[1]) + ' '
    s += '\n'
    for key in nodecolors:
        s += key + ' [fillcolor=' + nodecolors[key] + ']\n'
    s += ' }'
    outfile = open(filename, 'w')
    outfile.write(s)
    outfile.close()
    #print('graphviz dot data written to file', filename)

def dotlists(g):
    d = adjacency_dict(g)
    nodecolors = colornodes(g)
    for k in d:
        filename = 'list' + str(k) + '.gv'
        dotlist(d[k], filename, k, nodecolors)

def dotlist(lis, filename, title, colors):
    dotstr = 'digraph {\n'
    dotstr += 'rankdir = LR;\n'
    dotstr += 'node [shape=record style=filled];\n'
    dotstr += 'edge [tailclip=false];\n'
    dotstr += title + ' [ shape=box color=' + colors[title]  + ' ]\n';
    for e in lis:
        dotstr += e + ' [label="{ <data> ' + e + ' | <ref> }"];\n'
    dotstr += title + ':e -> '+ lis[0] + '\n'
    #for idx, ele in enumerate(lis[:-1]):
    #    dotstr += ele + ':ref:c -> ' + lis[idx+1] + ':data [arrowhead=vee, arrowtail=dot, dir=both];\n'
    for i in range(len(lis) - 1):
        dotstr += lis[i] + ':ref:c -> ' + lis[i+1] + ':data [arrowhead=vee, arrowtail=dot, dir=both];\n'
    for node in lis:
        dotstr += node + ' [fillcolor=' + colors[node] + ']\n'
    dotstr += '}'
    outfile = open(filename, 'w')
    outfile.write(dotstr)
    outfile.close()

def graphstr(g):
    nodes = g[0]
    edges = g[1]
    nodestr = '{' + ','.join([v for v in nodes]) + '}\n'
    edgestr='{'+','.join(['{'+','.join([v for v in e])+'}' for e in edges])+'}'
    return nodestr + edgestr
