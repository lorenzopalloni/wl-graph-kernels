import rdflib
from pathlib import Path
from pprint import pprint

filename = './data/subset_NamedRockUnit.nt'

# parsing the N-Triples file
g = rdflib.Graph().parse(filename, format='nt')


def get_instances(g: rdflib.Graph(), predicate_name: str):
    return [t[0] for t in g if str(t[1]).endswith(predicate_name)]


instances = get_instances(g, 'P2')

V = []
E = []
depth = 1
labels = dict()
vMap = []
eMap = []
search_front = []
V_sub = dict()
E_sub = dict()


# 1. Initialization
for i in instances:
    V.append(i)
    labels[(i, depth)] = 'e'
    vMap.append(i)
# 2. Subgraph Extraction
for i in instances:
    search_front.append(i)
    for i in range(depth - 1, -1, -1):
        new_search_front = []
        for r in search_front:
            triples = [(s, p, o) for (s, p, o) in g if s == r]
            for (s, p, o) in triples:
                new_search_front.append(o)
                if o not in vMap:
                    V.append(o)
                    vMap.append(o)
                labels[(o), depth] = o
                if o not in V_sub.keys():
                    V_sub[o] = depth
                if (s, p, o) not in eMap:
                    E.append((s, p, o))
                    eMap.append((s, p, o))
                labels[(s, p, o)] = p
                if (s, p, o) not in E_sub:
                    E_sub[(s, p, o)] = depth
        search_front = new_search_front


print('vMap:')
pprint(vMap)
print('eMap:')
pprint(eMap)
print('V:')
pprint(V)
print('E:')
pprint(E)
print('V_sub:')
pprint(V_sub)
print('E_sub:')
pprint(E_sub)
print('labels:')
pprint(labels)
