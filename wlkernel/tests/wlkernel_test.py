import pytest

# to import correctly the module
import sys, os
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

import wlkernel
import rdflib


def test_node_repr():
    node = wlkernel.Node(label='A', depth=2)
    assert "Node(label='A', depth=2)" == repr(node)


def test_node_str():
    n = wlkernel.Node(label='A', depth=2)
    assert "A-2" == str(n)


def test_node_eq():
    n1 = wlkernel.Node(label='A', depth=2)
    n2 = wlkernel.Node(label='A', depth=2)
    assert n1 == n2

    n2 = wlkernel.Node(label='B', depth=2)
    assert n1 != n2

    n2 = wlkernel.Node(label='A', depth=3)
    assert n1 != n2


def test_edge_repr():
    source = wlkernel.Node(label='A', depth=3)
    dest = wlkernel.Node(label='B', depth=2)
    edge = wlkernel.Edge(source, dest, label='P1', depth=2)
    assert (
        "Edge(source=Node(label='A', 3), dest=Node(label='B', depth=2), "
        "label='P1', depth=2)"
    )


def test_edge_str():
    source = wlkernel.Node(label='A', depth=3)
    dest = wlkernel.Node(label='B', depth=2)
    edge = wlkernel.Edge(source, dest, label='P1', depth=2)
    assert '(A-3)--(P1-2)-->(B-2)' == str(edge)


def test_edge_eq():
    source = wlkernel.Node(label='A', depth=3)
    dest = wlkernel.Node(label='B', depth=2)
    edge1 = wlkernel.Edge(source, dest, label='P1', depth=2)
    source = wlkernel.Node(label='A', depth=3)
    dest = wlkernel.Node(label='B', depth=2)
    edge2 = wlkernel.Edge(source, dest, label='P1', depth=2)
    assert edge1 == edge2

    source = wlkernel.Node(label='C', depth=3)
    dest = wlkernel.Node(label='B', depth=2)
    edge2 = wlkernel.Edge(source, dest, label='P1', depth=2)
    assert edge1 != edge2

    source = wlkernel.Node(label='A', depth=5)
    dest = wlkernel.Node(label='B', depth=4)
    edge2 = wlkernel.Edge(source, dest, label='P1', depth=2)
    assert edge1 != edge2

    source = wlkernel.Node(label='A', depth=5)
    dest = wlkernel.Node(label='B', depth=4)
    edge2 = wlkernel.Edge(source, dest, label='P2', depth=2)
    assert edge1 != edge2


def test_wlrdfgraph_init():
    graph = rdflib.Graph().parse('./example.nt', format='nt')

    max_depth = 0
    wl_rdf_graph = wlkernel.WLRDFGraph(
        instance='_:B1', graph=graph, max_depth=max_depth
    )
    root = wlkernel.Node(label='', depth=max_depth)

    assert root in wl_rdf_graph.nodes[max_depth]
    assert len(wl_rdf_graph.nodes) == 1
    assert len(wl_rdf_graph.nodes[max_depth]) == 1
    assert len(wl_rdf_graph.edges) == 1
    assert len(wl_rdf_graph.edges[max_depth - 1]) == 0
    # assert d_0 in wl_rdf_graph.nodes[max_depth - 1]

    # b1_p2_d = wlkernel.Edge(root, d_0, '_:P2', depth=max_depth - 1)

def test_wlrdfgraph_repr():
