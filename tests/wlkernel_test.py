from os.path import abspath
from pkg_resources import resource_filename
from itertools import chain

import pytest
import rdflib

import wlkernel


example_data = abspath(resource_filename('tests.resources', 'example.ttl'))


def test_node_repr():
    node = wlkernel.WLRDFNode(label='A', depth=2)
    assert "WLRDFNode(label='A', depth=2)" == repr(node)


def test_node_str():
    n = wlkernel.WLRDFNode(label='A', depth=2)
    assert "A-2" == str(n)


def test_node_eq():
    n1 = wlkernel.WLRDFNode(label='A', depth=2)
    n2 = wlkernel.WLRDFNode(label='A', depth=2)
    assert n1 == n2

    n2 = wlkernel.WLRDFNode(label='B', depth=2)
    assert n1 != n2

    n2 = wlkernel.WLRDFNode(label='A', depth=3)
    assert n1 != n2


def test_edge_repr():
    source = wlkernel.WLRDFNode(label='A', depth=3)
    dest = wlkernel.WLRDFNode(label='B', depth=2)
    edge = wlkernel.WLRDFEdge(source, dest, label='P1', depth=2)
    assert (
        "WLRDFEdge(source=WLRDFNode(label='A', depth=3), "
        "dest=WLRDFNode(label='B', depth=2), label='P1', depth=2)"
        == repr(edge)
    )


def test_edge_str():
    source = wlkernel.WLRDFNode(label='A', depth=3)
    dest = wlkernel.WLRDFNode(label='B', depth=2)
    edge = wlkernel.WLRDFEdge(source, dest, label='P1', depth=2)
    assert '(A-3)--(P1-2)-->(B-2)' == str(edge)


def test_edge_eq():
    source = wlkernel.WLRDFNode(label='A', depth=3)
    dest = wlkernel.WLRDFNode(label='B', depth=2)
    edge1 = wlkernel.WLRDFEdge(source, dest, label='P1', depth=2)
    source = wlkernel.WLRDFNode(label='A', depth=3)
    dest = wlkernel.WLRDFNode(label='B', depth=2)
    edge2 = wlkernel.WLRDFEdge(source, dest, label='P1', depth=2)
    assert edge1 == edge2

    source = wlkernel.WLRDFNode(label='C', depth=3)
    dest = wlkernel.WLRDFNode(label='B', depth=2)
    edge2 = wlkernel.WLRDFEdge(source, dest, label='P1', depth=2)
    assert edge1 != edge2

    source = wlkernel.WLRDFNode(label='A', depth=5)
    dest = wlkernel.WLRDFNode(label='B', depth=4)
    edge2 = wlkernel.WLRDFEdge(source, dest, label='P1', depth=2)
    assert edge1 != edge2

    source = wlkernel.WLRDFNode(label='A', depth=5)
    dest = wlkernel.WLRDFNode(label='B', depth=4)
    edge2 = wlkernel.WLRDFEdge(source, dest, label='P2', depth=2)
    assert edge1 != edge2


def test_wlrdfgraph_depth_0():
    '''
    ######
    # A1 #
    ######
    '''
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    wl_graph = wlkernel.WLRDFSubgraph('A1', rdf_graph, 0)

    root = wl_graph.get_node('root', 0)
    assert [root] == wl_graph.nodes[0]
    assert root.neighbors == []

    assert len(list(wl_graph.all_nodes())) == 1
    assert len(list(wl_graph.all_edges())) == 0


def test_wlrdfgraph_depth_1():
    r'''
          ######
          # A1 #
          ######
          /    \
      P2 /      \ P3
        /        \
    #####        #####
    # C #        # D #
    #####        #####
    '''
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    wl_graph = wlkernel.WLRDFSubgraph('A1', rdf_graph, 1)

    root = wl_graph.get_node('root', 1)
    assert [root] == wl_graph.nodes[1]
    assert root.neighbors == []

    assert len(wl_graph.edges[0]) == 2
    p2_edge = wl_graph.get_edge('root', 'C', 'P2', 0)
    assert p2_edge in wl_graph.edges[0]
    assert p2_edge.neighbor is root
    p3_edge = wl_graph.get_edge('root', 'D', 'P3', 0)
    assert p3_edge in wl_graph.edges[0]
    assert p3_edge.neighbor is root

    assert len(wl_graph.nodes[0]) == 2
    c_node = wl_graph.get_node('C', 0)
    assert c_node in wl_graph.nodes[0]
    assert c_node.neighbors == [p2_edge]
    d_node = wl_graph.get_node('D', 0)
    assert d_node in wl_graph.nodes[0]
    assert d_node.neighbors == [p3_edge]


def test_wlrdfgraph_depth_2():
    r'''
          ######
          # A1 #
          ######
          /    \
      P2 /      \ P3
        /        \
    #####        #####
    # C #        # D #
    #####        #####
        \       /
      P4 \     / P4
          \   /
          #####
          # H #
          #####
    '''
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    wl_graph = wlkernel.WLRDFSubgraph('A1', rdf_graph, 2)

    root = wl_graph.get_node('root', 2)
    assert [root] == wl_graph.nodes[2]
    assert root.neighbors == []

    assert len(wl_graph.edges[1]) == 2
    p2_edge = wl_graph.get_edge('root', 'C', 'P2', 1)
    assert p2_edge in wl_graph.edges[1]
    assert p2_edge.neighbor is root
    p3_edge = wl_graph.get_edge('root', 'D', 'P3', 1)
    assert p3_edge in wl_graph.edges[1]
    assert p3_edge.neighbor is root

    assert len(wl_graph.nodes[1]) == 2
    c_node = wl_graph.get_node('C', 1)
    assert c_node in wl_graph.nodes[1]
    assert c_node.neighbors == [p2_edge]
    d_node = wl_graph.get_node('D', 1)
    assert d_node in wl_graph.nodes[1]
    assert d_node.neighbors == [p3_edge]

    assert len(wl_graph.edges[0]) == 2
    c_p4_h_edge = wl_graph.get_edge('C', 'H', 'P4', 0)
    assert c_p4_h_edge in wl_graph.edges[0]
    assert c_p4_h_edge.neighbor is c_node
    d_p4_h_edge = wl_graph.get_edge('D', 'H', 'P4', 0)
    assert d_p4_h_edge in wl_graph.edges[0]
    assert d_p4_h_edge.neighbor is d_node

    assert len(wl_graph.nodes[0]) == 1
    h_node = wl_graph.get_node('H', 0)
    assert h_node in wl_graph.nodes[0]
    assert c_p4_h_edge in h_node.neighbors
    assert d_p4_h_edge in h_node.neighbors
    assert len(h_node.neighbors) == 2


def test_graph_relabeling():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    wl_graph_a1 = wlkernel.WLRDFSubgraph('A1', rdf_graph, 4)
    wl_graph_b1 = wlkernel.WLRDFSubgraph('B1', rdf_graph, 4)
    a1_relabeled, b1_relabeled = wlkernel.relabel(wl_graph_a1, wl_graph_b1)

    assert (
        a1_relabeled.root == b1_relabeled.root
        == a1_relabeled.nodes[4][0] == b1_relabeled.nodes[4][0]
    )

    edge_labels = [
        e.label for e in chain(a1_relabeled.edges[3], b1_relabeled.edges[3])
    ]
    assert len(edge_labels) == 4
    assert len(set(edge_labels)) == 2
    node_labels = [
        n.label for n in chain(a1_relabeled.nodes[3], b1_relabeled.nodes[3])
    ]
    assert len(node_labels) == 4
    assert len(set(node_labels)) == 4

    edge_labels = [
        e.label for e in chain(a1_relabeled.edges[2], b1_relabeled.edges[2])
    ]
    assert len(edge_labels) == 4
    assert len(set(edge_labels)) == 4
    node_labels = [
        n.label for n in chain(a1_relabeled.nodes[2], b1_relabeled.nodes[2])
    ]
    assert len(node_labels) == 2
    assert len(set(node_labels)) == 2

    edge_labels = [
        e.label for e in chain(a1_relabeled.edges[1], b1_relabeled.edges[1])
    ]
    assert len(edge_labels) == 2
    assert len(set(edge_labels)) == 2
    node_labels = [
        n.label for n in chain(a1_relabeled.nodes[1], b1_relabeled.nodes[1])
    ]
    assert len(node_labels) == 2
    assert len(set(node_labels)) == 2

    edge_labels = [
        e.label for e in chain(a1_relabeled.edges[0], b1_relabeled.edges[0])
    ]
    assert len(edge_labels) == 4
    assert len(set(edge_labels)) == 4
    node_labels = [
        n.label for n in chain(a1_relabeled.nodes[0], b1_relabeled.nodes[0])
    ]
    assert len(node_labels) == 4
    assert len(set(node_labels)) == 3


def test_wl_kernel():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    wl_graph_a1 = wlkernel.WLRDFSubgraph('A1', rdf_graph, 4)
    wl_graph_b1 = wlkernel.WLRDFSubgraph('B1', rdf_graph, 4)
    assert wlkernel.wl_kernel(wl_graph_a1, wl_graph_b1) == 7

    a1_relabeled, b1_relabeled = wlkernel.relabel(wl_graph_a1, wl_graph_b1)
    assert wlkernel.wl_kernel(wl_graph_a1, wl_graph_b1) == 4


def test_compute_kernel():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    kernel = wlkernel.compute_kernel(rdf_graph, 'A1', 'B1', 4)
    assert kernel == 7

    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    kernel = wlkernel.compute_kernel(rdf_graph, 'A1', 'B1', 4, iterations=2)
    assert kernel == 7*1/2 + 4*2/2

    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    kernel = wlkernel.compute_kernel(rdf_graph, 'A1', 'B1', 4, iterations=3)
    assert kernel == 7*1/3 + 4*2/3 + 3*3/3
