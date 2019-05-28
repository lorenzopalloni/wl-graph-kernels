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
        "Edge(source=Node(label='A', depth=3), dest=Node(label='B', depth=2), "
        "label='P1', depth=2)" == repr(edge)
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
    graph = rdflib.Graph().parse('./example.ttl', format='turtle')

    max_depth = 4
    g = wlkernel.WLRDFGraph(
        instance='A1', graph=graph, max_depth=max_depth
    )
    assert wlkernel.Node('A1', depth=max_depth) not in g.nodes[0]

    root = wlkernel.Node(label='', depth=max_depth)
    # depth 4
    assert root in g.nodes[max_depth]
    assert len(g.nodes[4]) == 1
    assert len(g.edges[4]) == 0
    # depth 3
    assert wlkernel.Node(label='C', depth=3) in g.nodes[3]
    assert wlkernel.Node(label='D', depth=3) in g.nodes[3]
    assert len(g.nodes[3]) == 2
    assert wlkernel.Edge(root, wlkernel.Node('C', 3), 'P2', 3) in g.edges[3]
    assert wlkernel.Edge(root, wlkernel.Node('D', 3), 'P3', 3) in g.edges[3]
    assert len(g.edges[3]) == 2
    # depth 2
    assert wlkernel.Node(label='H', depth=2) in g.nodes[2]
    assert len(g.nodes[2]) == 1
    assert (
            wlkernel.Edge(wlkernel.Node('C', 3),
                          wlkernel.Node('H', 2), 'P4', 2) in g.edges[2]
    )
    assert (
            wlkernel.Edge(wlkernel.Node('D', 3),
                          wlkernel.Node('H', 2), 'P4', 2) in g.edges[2]
    )
    assert len(g.edges[2]) == 2
    # depth 1
    assert wlkernel.Node(label='A2', depth=1) in g.nodes[1]
    assert len(g.nodes[1]) == 1
    assert (
            wlkernel.Edge(wlkernel.Node('H', 2),
                          wlkernel.Node('A2', 1), 'P6', 1) in g.edges[1]
    )
    assert len(g.edges[1]) == 1
    # depth 0
    assert wlkernel.Node(label='D', depth=0) in g.nodes[0]
    assert wlkernel.Node(label='E', depth=0) in g.nodes[0]
    assert len(g.nodes[0]) == 2
    assert (
            wlkernel.Edge(wlkernel.Node('A2', 1),
                          wlkernel.Node('D', 0), 'P2', 0) in g.edges[0]
    )
    assert (
            wlkernel.Edge(wlkernel.Node('A2', 1),
                          wlkernel.Node('E', 0), 'P3', 0) in g.edges[0]
    )
    assert len(g.edges[0]) == 2


def test_wlrdfgraph_repr():
    graph = rdflib.Graph().parse('./example.ttl', format='turtle')
    
    max_depth = 1
    root = wlkernel.Node(label='', depth=max_depth)
    wl_rdf_graph = wlkernel.WLRDFGraph('B1', graph, max_depth)
    assert root in wl_rdf_graph.nodes[max_depth]
    assert (
        "defaultdict(<class 'list'>, {0: [Edge(source=Node(label='', "
        "depth=1), dest=Node(label='F', depth=0), label='P3', "
        "depth=0), Edge(source=Node(label='', depth=1), dest=Node(label='G', "
        "depth=0), label='P2', depth=0)]})" == repr(wl_rdf_graph) or
        "defaultdict(<class 'list'>, {0: [Edge(source=Node(label='', depth=1),"
        " dest=Node(label='G', depth=0), label='P2', depth=0), "
        "Edge(source=Node(label='', depth=1), dest=Node(label='F', depth=0), "
        "label='P3', depth=0)]})" == repr(wl_rdf_graph)
    )


def test_wlrdfgraph_relabel():
    graph = rdflib.Graph().parse('./example.ttl', format='turtle')
    max_depth = 1
