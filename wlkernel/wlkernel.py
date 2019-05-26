import rdflib
from collections import defaultdict
from typing import NoReturn, List


class Node:
    'A node of a Weisfeiler-Lehman RDF graph'

    def __init__(self, label: str, depth: int):
        self.label = label
        self.depth = depth
        self.neighbors = []
        self.prev_label = label

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
        self.prev_label = label

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
        self.nodes[max_depth][0].prev_label = ''

        for edge in self.edges[max_depth - 1]:
            if instance == edge.source.label:
                edge.source.label = ''
                edge.source.prev_label = ''

    def __repr__(self):
        return repr(self.edges)

    def __str__(self):
        return str(self.edges)


def get_multiset_label(nodes: List[Node]) -> str:
    'Sorts and concatenates the labels of a list of nodes into a string.'
    nodes_sorted = sorted(nodes, key=(lambda node: node.prev_label))
    return ''.join([node.prev_label for node in nodes_sorted])


def relabel(g_first: WLRDFGraph, g_second: WLRDFGraph, max_depth: int,
            max_iteration: int) -> NoReturn:
    'Weisfeiler-Lehman Relabeling for RDF subgraph'

    # 0-th and 1-th iterations of Algorithm 3.
    for iteration in range(max_iteration):
        # Steps 1. 2. and 3. of the algorithm 3. for nodes
        uniq_labels_node = defaultdict(set)
        for depth in range(max_depth + 1):
            for node in g_first.nodes[depth]:
                node.label += get_multiset_label(node.neighbors)
                uniq_labels_node[depth].add(node.label)
            for node in g_second.nodes[depth]:
                node.label += get_multiset_label(node.neighbors)
                uniq_labels_node[depth].add(node.label)

        # Steps 1. 2. and 3. of the algorithm 3. for edges
        uniq_labels_edge = defaultdict(set)
        for depth in range(max_depth):
            for edge in g_first.edges[depth]:
                edge.label += edge.neighbor.prev_label
                uniq_labels_edge[depth].add(edge.label)
            for edge in g_second.edges[depth]:
                edge.label += edge.neighbor.prev_label
                uniq_labels_edge[depth].add(edge.label)

        # Step 4. relabeling for nodes
        for depth in range(max_depth + 1):
            uniq_temp = list(uniq_labels_node[depth])
            for node in g_first.nodes[depth]:
                node.label = str(
                    (iteration + 1) * len(uniq_temp) +
                    uniq_temp.index(node.label) % len(uniq_temp)
                )
                node.prev_label = node.label

            for node in g_second.nodes[depth]:
                node.label = str(
                    (iteration + 1) * len(uniq_temp) +
                    uniq_temp.index(node.label) % len(uniq_temp)
                )
                node.prev_label = node.label

        # Step 4. relabeling for edges
        for depth in range(max_depth):
            uniq_temp = list(uniq_labels_edge[depth])
            for edge in g_first.edges[depth]:
                edge.label = str(
                    (iteration + 1) * len(uniq_temp) +
                    uniq_temp.index(edge.label) % len(uniq_temp)
                )
                edge.prev_label = edge.label
            for edge in g_second.edges[depth]:
                edge.label = str(
                    (iteration + 1) * len(uniq_temp) +
                    uniq_temp.index(edge.label) % len(uniq_temp)
                )
                edge.prev_label = edge.label

# def relabel(g_first: WLRDFGraph, g_second: WLRDFGraph, max_depth: int,
#             max_iteration: int):
#     'Weisfeiler-Lehman Relabeling for RDF subgraph'
#
#     uniq_label = set()
#     # first iteration - for now only for the nodes
#     for depth in range(max_depth):
#         for node in g_first.nodes[depth]:
#             M = node.neighbors
#             sort('M by prev_label')
#             node.label += concatenate('all prev_label of the nodes in M')
#             uniq_label.add(node.label)
#         for node in g_second[depth]:
#             pass
#
#     for depth in range(max_depth):
#         # relabella the unique labels with f'{len(uniq_label) + counter(che
#         # itera su range(len(uniq_label)))}'
#         pass
