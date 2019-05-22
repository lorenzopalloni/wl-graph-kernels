import rdflib
import networkx as nx
from path import Path
import inspect
from collections import Counter
import pprint

PROJECT_DIR = Path(inspect.getsourcefile(lambda: 0)).abspath().parent
DATA_DIR = PROJECT_DIR / 'data'
filename = DATA_DIR / 'Lexicon_NamedRockUnit.nt'

# parsing the N-Triples file
rdf_graph = rdflib.Graph().parse(filename, format='turtle')

g = Counter(list(rdf_graph.predicates()))
pprint.pprint(g.most_common(2))