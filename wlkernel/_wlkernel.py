from collections import defaultdict
from itertools import chain
from typing import List, Dict, Iterable
from copy import deepcopy

import rdflib


class WLRDFNode:
    'A node of a Weisfeiler-Lehman RDF graph'

    def __init__(self, label: str, depth: int):
        self.label = label
        self.label_expansion = ''
        self.depth = depth
        self.neighbors = []

    def add_neighbor(self, edge):
        'Add an edge as a neighbor'
        self.neighbors.append(edge)

    def __repr__(self):
        return f"WLRDFNode(label='{self.label}', depth={self.depth})"

    def __str__(self):
        return f'{self.label}-{self.depth}'

    def __eq__(self, node):
        return self.label == node.label and self.depth == node.depth


class WLRDFEdge:
    'An edge of a Weisfeiler-Lehman RDF graph'

    def __init__(
        self, source: WLRDFNode, dest: WLRDFNode, label: str, depth: int
    ):
        self.source = source
        self.dest = dest
        self.label = label
        self.label_expansion = ''
        self.depth = depth
        self.neighbor = None

    def __repr__(self):
        return (
            f'WLRDFEdge(source={repr(self.source)}, dest={repr(self.dest)}, '
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


class WLRDFSubgraph:
    'Weisfeiler-Lehman RDF subgraph'

    def __init__(self, instance: str, graph: rdflib.Graph, max_depth: int):
        self.root = WLRDFNode(label=instance, depth=max_depth)
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
                    child = WLRDFNode(obj, depth)
                    if child in self.nodes[depth]:
                        child = self.get_node(obj, depth)
                    edge = WLRDFEdge(parent, child, pred, depth)

                    if child not in new_search_front:
                        new_search_front.append(child)

                    child.add_neighbor(edge)
                    edge.neighbor = parent

                    if child not in self.nodes[depth]:
                        self.nodes[depth].append(child)
                    self.edges[depth].append(edge)
            search_front = new_search_front

        # cleanup the root and the relative edges
        self.nodes[max_depth][0].label = 'root'

        for edge in self.edges[max_depth - 1]:
            if instance == edge.source.label:
                edge.source.label = ''

    def get_node(self, label: str, depth: int):
        'Return the corresponding WLRDFNode object'
        for node in self.nodes[depth]:
            if node.label == label:
                return node
        else:
            raise RuntimeError('The specified node is not in the graph')

    def get_edge(self, source_label: str, dest_label: str, edge_label: str,
                 depth: int):
        'Return the corresponding WLRDFEdge object'
        for edge in self.edges[depth]:
            if (edge.label == edge_label and edge.source.label == source_label
                and edge.dest.label == dest_label):
                return edge
        else:
            raise RuntimeError('The specified edge is not in the graph')

    def all_nodes(self):
        return ( node for node in chain.from_iterable(self.nodes.values()) )

    def all_edges(self):
        return ( edge for edge in chain.from_iterable(self.edges.values()) )

    def __repr__(self):
        return repr(self.edges)

    def __str__(self):
        return str(self.edges)


def get_multiset_label(node: WLRDFNode) -> str:
    'Sort and concatenate the labels of the neighbors of a node'
    edges_sorted = sorted(node.neighbors, key=(lambda e: e.label))
    return ''.join(edge.label for edge in edges_sorted)


def label_compression(labels: Iterable, start_index: int) -> Dict:
    return {
        multiset_label: str(new_label + start_index)
        for new_label, multiset_label in enumerate(labels)
    }


def relabel(subgraphs: List[WLRDFSubgraph],
            iterations: int) -> List[WLRDFSubgraph]:
    'Weisfeiler-Lehman Relabeling for RDF subgraph'

    subgraphs = deepcopy(subgraphs)

    start_index_label = 0

    for iteration in range(iterations):
        uniq_labels = set()

        for subgraph in subgraphs:
            for node in subgraph.all_nodes():
                multiset_label = get_multiset_label(node)
                node.label_extension = multiset_label
                uniq_labels.add(node.label + multiset_label)

            for edge in subgraph.all_edges():
                multiset_label = edge.neighbor.label
                edge.label_extension = multiset_label
                uniq_labels.add(edge.label + multiset_label)

        label_mapping = label_compression(sorted(uniq_labels), start_index_label)
        start_index_label += len(uniq_labels)

        for subgraph in subgraphs:
            for node in subgraph.all_nodes():
                node.label = label_mapping[node.label + node.label_extension]

            for edge in subgraph.all_edges():
                edge.label = label_mapping[edge.label + edge.label_extension]
    return subgraphs
