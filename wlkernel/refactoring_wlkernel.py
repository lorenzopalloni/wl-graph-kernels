import rdflib
from collections import defaultdict
from itertools import chain
from typing import NoReturn, List, Set, Dict


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

    def __hash__(self):
        return hash(self.label)

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
            f"label='{self.label}', depth={self.depth})"
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

    def __hash__(self):
        return hash(self.label)


class WLRDFGraph:
    'Weisfeiler-Lehman RDF subgraph'

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
                    if edge not in self.edges[depth]:
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

    def all_nodes(self):
        return ( node for node in chain.from_iterable(self.nodes.values()) )

    def all_edges(self):
        return ( edge for edge in chain.from_iterable(self.edges.values()) )

    # def update_labels(self, max_depth: int) -> NoReturn:
    #     'Assign to the label the value of prev_value for each node and edge.'
    #     for depth in range(max_depth + 1):
    #         for node in self.nodes[depth]:
    #             node.label = node.prev_label
    #     for depth in range(max_depth):
    #         for edge in self.edges[depth]:
    #             edge.label = edge.prev_label


def get_multiset_label(edges: List[Edge]) -> str:
    'Sort and concatenate the labels of a list of edges into a string.'
    edges_sorted = sorted(edges, key=(lambda e: e.label))
    return ''.join(edge.label for edge in edges_sorted)


def label_compression(labels: Set, start_index: int) -> Dict:
    return {
        multiset_label: str(new_label + start_index)
        for new_label, multiset_label in enumerate(labels)
    }


def relabel(left_graph: WLRDFGraph, right_graph: WLRDFGraph, max_depth: int,
            max_iteration: int) -> NoReturn:
    'Weisfeiler-Lehman Relabeling for RDF subgraph'

    start_index_label = 0

    for iteration in range(max_iteration):
        uniq_labels = set()
        multiset_mapping = dict()

        for node in chain(left_graph.all_nodes(), right_graph.all_nodes()):
            new_label = node.label + get_multiset_label(node.neighbors)
            uniq_labels.add(new_label)
            multiset_mapping[node] = new_label

        for edge in chain(left_graph.all_edges(), right_graph.all_edges()):
            new_label = edge.label + edge.neighbor.label
            uniq_labels.add(new_label)
            multiset_mapping[edge] = new_label

        label_mapping = label_compression(uniq_labels, start_index_label)
        start_index_label += len(uniq_labels)

        from pprint import pprint
        pprint(multiset_mapping)
        exit()

        for element in chain(left_graph.all_nodes(), left_graph.all_edges(),
                             right_graph.all_nodes(), right_graph.all_edges()):
            multiset_label = multiset_mapping[element]
            element.label = label_mapping[multiset_label]

        # left_graph.update_labels(max_depth)
        # right_graph.update_labels(max_depth)

