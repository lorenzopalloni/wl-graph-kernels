from typing import (
    List,
    Dict,
    Tuple,
    Iterable,
    Union,
    Set,
)
from collections import Counter
from itertools import chain

from nptyping import Array
import numpy as np


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


class WLGraph:
    'Standard Weisfeiler-Lehman graph with directed labeled edges'

    def __init__(self, triples: Iterable[Tuple[str, str, str]],
                 instance: str, max_depth: int):
        'Build a Weisfeiler-Lehman graph from a list of RDF triples'
        triples = list(triples)
        self.max_depth = max_depth
        self.nodes: Set[Node] = set()
        self.edges: Set[Edge] = set()
        self.labels: List[Dict[Union[Node, Edge], str]] = [dict()]

        v_map: Dict[str, Node] = dict()
        e_map: Dict[Tuple[str, str, str], Edge] = dict()

        root = Node()
        self.nodes.add(root)
        self.labels[0][root] = 'root'
        v_map[instance] = root

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
                        self.labels[0][v_map[obj]] = obj

                    t = (sub, pred, obj)
                    if t not in e_map:
                        e = Edge()
                        self.edges.add(e)
                        e_map[t] = e
                        self.labels[0][e_map[t]] = pred

                    v_map[obj].add_neighbor(e_map[t])
                    e_map[t].neighbor = v_map[sub]

            search_front = new_search_front


def wl_relabel(wl_graphs: Iterable[WLGraph], iterations: int = 1):
    'Relabeling algorithm'

    wl_graphs = list(wl_graphs)

    assert len(set(len(wl_graph.labels) for wl_graph in wl_graphs))
    m = len(wl_graphs[0].labels)
    for i in range(m, m + iterations):

        # 1. Multiset-label determination
        multisets_list: List[Dict[Union[Node, Edge], List[str]]] = [
            dict() for _ in range(len(wl_graphs))
        ]
        for wl_graph, multisets in zip(wl_graphs, multisets_list):
            for v in wl_graph.nodes:
                if v in wl_graph.labels[0]:
                    multisets[v] = [
                        wl_graph.labels[i - 1][u] for u in v.neighbors
                        if u in wl_graph.labels[i - 1]
                    ]
            for e in wl_graph.edges:
                if e in wl_graph.labels[0]:
                    multisets[e] = [ wl_graph.labels[i - 1][e.neighbor] ]

        # 2. Sorting each multiset
        expanded_labels_list: List[Dict[Union[Node, Edge], str]] = [
            dict() for _ in range(len(wl_graphs))
        ]
        for wl_graph, multisets, expanded_labels in zip(wl_graphs,
                                                        multisets_list,
                                                        expanded_labels_list):
            for k, multiset in multisets.items():
                expanded_labels[k] = (
                    wl_graph.labels[i - 1][k] + ''.join(sorted(multiset))
                )

        # 3. Label compression
        total_label_set = (
            set(chain.from_iterable(e.values() for e in expanded_labels_list))
        )
        f = {
            old_label: str(compressed_label)
            for compressed_label, old_label in enumerate(total_label_set)
        }


        # 4. Relabeling
        for wl_graph, expanded_labels in zip(wl_graphs, expanded_labels_list):
            wl_graph.labels.append({
                k: f[expanded_labels[k]] for k in expanded_labels
            })


def wl_kernel(wl_graph_1: WLGraph, wl_graph_2: WLGraph,
              iterations: int = 0) -> float:
    'Compute the Weisfeiler-Lehman kernel for two WLGraphs'

    assert len(wl_graph_1.labels) == len(wl_graph_2.labels)
    m = len(wl_graph_1.labels)
    if iterations > m - 1:
        wl_relabel([wl_graph_1, wl_graph_2], iterations - m + 1)

    kernel = 0.0
    for it in range(iterations + 1):
        node_labels_1 = [
            wl_graph_1.labels[it][node] for node in wl_graph_1.nodes
        ]
        node_labels_2 = [
            wl_graph_2.labels[it][node] for node in wl_graph_2.nodes
        ]
        edge_labels_1 = [
            wl_graph_1.labels[it][edge] for edge in wl_graph_1.edges
        ]
        edge_labels_2 = [
            wl_graph_2.labels[it][edge] for edge in wl_graph_2.edges
        ]
        cc_nodes = count_commons(node_labels_1, node_labels_2)
        cc_edges = count_commons(edge_labels_1, edge_labels_2)
        w = (it + 1) / (iterations + 1)
        kernel += w * (cc_nodes + cc_edges)
    return kernel


def wl_kernel_matrix(wl_graphs: Iterable[WLGraph],
                     iterations: int = 0) -> List[List[float]]:
    'Compute the matrix of the kernel values between each couple of WLGraphs'
    wl_graphs = list(wl_graphs)

    m = len(wl_graphs[0].labels)
    if iterations > m - 1:
        wl_relabel(wl_graphs, iterations - m + 1)

    n = len(wl_graphs)
    kernel_matrix = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            kernel_matrix[i][j] = wl_kernel(
                wl_graphs[i], wl_graphs[j], iterations
            )
    for i in range(n):
        for j in range(0, i):
            kernel_matrix[i][j] = kernel_matrix[j][i]
    return kernel_matrix


class WLRDFGraph:
    'Weisfeiler-Lehman RDF graph'

    def __init__(self, triples: Iterable[Tuple[str, str, str]],
                 instances: Iterable[str], max_depth: int):
        'Build a Weisfeiler-Lehman RDF graph from a list of RDF triples'
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
                    r_triples = ((s, p, o) for s, p, o in triples if s == r)
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

        for i in range(len(self.labels), len(self.labels) + iterations):

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
        cc_nodes = count_commons(node_labels_1, node_labels_2)
        cc_edges = count_commons(edge_labels_1, edge_labels_2)
        w = (it + 1) / (iterations + 1)
        kernel += w * (cc_nodes + cc_edges)
    return kernel


def wlrdf_kernel_matrix(graph: WLRDFGraph, instances: List[str],
                        iterations: int = 0) -> Array[float]:
    'Compute the matrix of the kernel values between each couple of instances'
    n = len(instances)
    kernel_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            kernel_matrix[i][j] = wlrdf_kernel(
                graph, instances[i], instances[j], iterations
            )
    for i in range(n):
        for j in range(0, i):
            kernel_matrix[i][j] = kernel_matrix[j][i]
    return kernel_matrix


def kernel_normalization(kernel_matrix: Array[float]) -> Array[float]:
    n = kernel_matrix.shape[0]
    res = np.zeros((n, n))
    assert kernel_matrix.shape[1] == n
    for i in range(n):
        for j in range(n):
            res[i][j] = kernel_matrix[i][j] / np.sqrt(
                kernel_matrix[i][i] * kernel_matrix[j][j]
            )
    return res
