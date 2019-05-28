import rdflib
# from wlkernel import *
from refactoring_wlkernel import *
from pprint import pprint

graph = rdflib.Graph().parse('./tests/example.ttl', format='turtle')
max_depth = 4
g_first = WLRDFGraph('A1', graph, max_depth)
g_second = WLRDFGraph('B1', graph, max_depth)
# g_third = WLRDFGraph('A2', graph, max_depth)
relabel(g_first, g_second, max_depth, 1)
