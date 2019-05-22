import rdflib
from collections import defaultdict


class Node:
    'A node of a Weisfeiler-Lehman RDF graph'

    def __init__(self, label: str, depth: int):
        self.label = label
        self.depth = depth
        self.neighbors = []

    def add_neighbor(self, edge):
        'Add an edge as a neighbor'
        self.neighbors.append(edge)

    def __repr__(self):
        return f"Node(label='{self.label}', depth={self.depth})"

    def __str__(self):
        return f'{self.label}-{self.depth}'

    def __eq__(self, node):
        return self.label == node.label and self.depth == node.depth


class Edge:
    'An edge of a Weisfeiler-Lehman RDF graph'

    def __init__(self, source: Node, dest: Node, label: str, depth: int):
        self.source = source
        self.dest = dest
        self.label = label
        self.depth = depth
        self.neighbor = None

    def __repr__(self):
        return (
            f'Edge(source={repr(self.source)}, dest={repr(self.dest)}, '
            f'label={self.label}, depth={self.depth})'
        )

    def __str__(self):
        return (
            f'({str(self.source)})--({self.label}-{self.depth})'
            f'-->({str(self.dest)})'
        )

    def __eq__(self, edge):
        return (
            self.source == edge.source and self.dest == edge.dest
            and self.label == edge.label and self.depth == edge.depth
        )


class WLRDFGraph:
    'Weisfeiler-Lehman RDF graph'

    def __init__(self, instance: str, graph: rdflib.Graph, max_depth: int):
        self.root = Node(label=instance, depth=max_depth)
        self.nodes = defaultdict(list, {max_depth: [self.root]})
        self.edges = defaultdict(list)

        search_front = [self.root]

        for depth in range(max_depth - 1, -1, -1):
            new_search_front = []
            for parent in search_front:
                triples = [
                    (str(s), str(p), str(o))
                    for (s, p, o) in graph if str(s) == parent.label
                ]
                for (subj, pred, obj) in triples:
                    child = Node(obj, depth)
                    edge = Edge(parent, child, pred, depth)
                    new_search_front.append(child)

                    child.add_neighbor(edge)
                    edge.neighbor = child

                    if child not in self.nodes[depth]:
                        self.nodes[depth].append(child)
                    self.edges[depth].append(edge)
            search_front = new_search_front

        # cleanup the root and the relative edges
        self.nodes[max_depth][0].label = ''

        for edge in self.edges[max_depth - 1]:
            if instance == edge.source.label:
                edge.source.label = ''

    def __repr__(self):
        return repr(self.edges)

    def __str__(self):
        return str(self.edges)
