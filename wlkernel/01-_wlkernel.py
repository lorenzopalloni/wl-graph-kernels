from typing import (
    List,
    Dict,
    Tuple,
    Iterable,
    Union,
    Set,
)
from collections import Counter


class Node:
    'A node of a Weisfeiler-Lehman RDF graph'

    def __init__(self):
        self.neighbors = set()

    def add_neighbor(self, edge):
        self.neighbors.add(edge)

    def __hash__(self):
        return hash(id(self))


class Edge:
    'An edge of a Weisfeiler-Lehman RDF graph'

    def __init__(self):
        self.neighbor = None

    def __hash__(self):
        return hash(id(self))


class WLRDFGraph:
    'Weisfeiler-Lehman RDF graph'

    def __init__(self, triples: Iterable[Tuple[str, str, str]],
                 instances: Iterable[str], max_depth: int):
        'Build a Weisfeiler-Lehman RDF graph from an RDF graph'
        triples = list(triples)
        self.max_depth = max_depth
        self.nodes: Set[Node] = set()
        self.edges: Set[Edge] = set()
        self.labels: List[Dict[Tuple[Union[Node, Edge], int], str]] = [dict()]
        self.instance_nodes: Dict[str, Dict[Node, int]] = {
            instance: dict() for instance in instances
        }
        self.instance_edges: Dict[str, Dict[Edge, int]] = {
            instance: dict() for instance in instances
        }

        v_map: Dict[str, Node] = dict()
        e_map: Dict[Tuple[str, str, str], Edge] = dict()

        # 1. Initialization
        for instance in instances:
            root = Node()
            self.nodes.add(root)
            self.labels[0][(root, max_depth)] = 'root'
            v_map[instance] = root

        # 2. Subgraph Extraction
        for instance in instances:
            search_front = {instance}
            for j in reversed(range(0, max_depth)):
                new_search_front = set()
                for r in search_front:
                    r_triples = [(s, p, o) for s, p, o in triples if s == r]
                    for sub, pred, obj in r_triples:
                        new_search_front.add(obj)

                        if obj not in v_map:
                            v = Node()
                            self.nodes.add(v)
                            v_map[obj] = v
                        self.labels[0][(v_map[obj], j)] = obj
                        if v_map[obj] not in self.instance_nodes[instance]:
                            self.instance_nodes[instance][v_map[obj]] = j

                        t = (sub, pred, obj)
                        if t not in e_map:
                            e = Edge()
                            self.edges.add(e)
                            e_map[t] = e
                        self.labels[0][e_map[t], j] = pred
                        if e_map[t] not in self.instance_edges[instance]:
                            self.instance_edges[instance][e_map[t]] = j

                        v_map[obj].add_neighbor(e_map[t])
                        e_map[t].neighbor = v_map[sub]

                search_front = new_search_front



    def relabel(self, iterations: int = 1):
        'Relabeling algorithm'

        for i in range(len(self.labels), len(self.labels) + iterations + 1):
            multisets: Dict[Tuple[Union[Node, Edge], int], List[str]] = dict()

            # 1. Multiset-label determination
            for v in self.nodes:
                for j in range(self.max_depth + 1):
                    if (v, j) in self.labels[0]:
                        multisets[(v, j)] = [
                            self.labels[i - 1][(u, j)] for u in v.neighbors
                            if (u, j) in self.labels[i - 1]
                        ]
            for e in self.edges:
                for j in range(self.max_depth):
                    if (e, j) in self.labels[0]:
                        multisets[(e, j)] = [
                            self.labels[i - 1][(e.neighbor, j + 1)]
                        ]

            # 2. Sorting each multiset
            expanded_labels = {
                (k, j): self.labels[i - 1][(k, j)] + ''.join(sorted(multiset))
                for (k, j), multiset in multisets.items()
            }

            # 3. Label compression
            f = {
                s: str(i)
                for i, s in enumerate(set(expanded_labels.values()))
            }

            # 4. Relabeling
            self.labels.append({
                (k, j): f[expanded_labels[(k, j)]]
                for (k, j) in expanded_labels
            })


def count_commons(a: Iterable, b: Iterable) -> int:
    'Return the number of common elements in the two iterables'
    uniques = set(a).intersection(set(b))
    counter_a = Counter(a)
    counter_b = Counter(b)
    commons = 0
    for u in uniques:
        commons += counter_a[u] * counter_b[u]
    return commons


def wlrdf_kernel(graph: WLRDFGraph, instance_1: str, instance_2: str,
                 iterations: int = 0) -> float:
    'Compute the Weisfeiler-Lehman kernel for two instances'

    if iterations > len(graph.labels) - 1:
        graph.relabel(iterations - len(graph.labels) + 1)

    kernel = 0.0
    for it in range(iterations + 1):
        node_labels_1 = [
            graph.labels[it][(v, d)]
            for v, d in graph.instance_nodes[instance_1].items()
        ]
        node_labels_2 = [
            graph.labels[it][(v, d)]
            for v, d in graph.instance_nodes[instance_2].items()
        ]
        edge_labels_1 = [
            graph.labels[it][(e, d)]
            for e, d in graph.instance_edges[instance_1].items()
        ]
        edge_labels_2 = [
            graph.labels[it][(e, d)]
            for e, d in graph.instance_edges[instance_2].items()
        ]
        w = (it + 1) / (iterations + 1)
        k = (count_commons(node_labels_1, node_labels_2)
            + count_commons(edge_labels_1, edge_labels_2))
        kernel += w * k
    return kernel


def wlrdf_kernel_matrix(graph: WLRDFGraph, instances: List[str],
                        iterations: int = 0) -> List[List[float]]:
    'Compute the matrix of the kernel values between each couple of instances'
    n = len(instances)
    kernek_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            kernel_matrix[i][j] = wlrdf_kernel(graph, instances[i],
                                               instances[j], iterations)
    for i in range(n):
        for j in range(0, i):
            kernel_matrix[i][j] = kernel_matrix[j][i]
    return kernel_matrix

