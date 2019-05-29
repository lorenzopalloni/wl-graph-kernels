from os.path import abspath
from pkg_resources import resource_filename

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
    wl_graph = wlkernel.WLRDFGraph('A1', rdf_graph, 0)

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
    wl_graph = wlkernel.WLRDFGraph('A1', rdf_graph, 1)

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
    wl_graph = wlkernel.WLRDFGraph('A1', rdf_graph, 2)

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


#def test_wlrdfgraph_init():
#    graph = rdflib.Graph().parse('./example.ttl', format='turtle')
#
#    max_depth = 4
#    g = wlkernel.WLRDFGraph(
#        instance='A1', graph=graph, max_depth=max_depth
#    )
#    assert wlkernel.WLRDFNode('A1', depth=max_depth) not in g.nodes[0]
#
#    root = wlkernel.WLRDFNode(label='', depth=max_depth)
#    # depth 4
#    assert root in g.nodes[max_depth]
#    assert len(g.nodes[4]) == 1
#    assert len(g.edges[4]) == 0
#    # depth 3
#    assert wlkernel.WLRDFNode(label='C', depth=3) in g.nodes[3]
#    assert wlkernel.WLRDFNode(label='D', depth=3) in g.nodes[3]
#    assert len(g.nodes[3]) == 2
#    assert wlkernel.WLRDFEdge(root, wlkernel.WLRDFNode('C', 3), 'P2', 3) in g.edges[3]
#    assert wlkernel.WLRDFEdge(root, wlkernel.WLRDFNode('D', 3), 'P3', 3) in g.edges[3]
#    assert len(g.edges[3]) == 2
#    # depth 2
#    assert wlkernel.WLRDFNode(label='H', depth=2) in g.nodes[2]
#    assert len(g.nodes[2]) == 1
#    assert (
#            wlkernel.WLRDFEdge(wlkernel.WLRDFNode('C', 3),
#                          wlkernel.WLRDFNode('H', 2), 'P4', 2) in g.edges[2]
#    )
#    assert (
#            wlkernel.WLRDFEdge(wlkernel.WLRDFNode('D', 3),
#                          wlkernel.WLRDFNode('H', 2), 'P4', 2) in g.edges[2]
#    )
#    assert len(g.edges[2]) == 2
#    # depth 1
#    assert wlkernel.WLRDFNode(label='A2', depth=1) in g.nodes[1]
#    assert len(g.nodes[1]) == 1
#    assert (
#            wlkernel.WLRDFEdge(wlkernel.WLRDFNode('H', 2),
#                          wlkernel.WLRDFNode('A2', 1), 'P6', 1) in g.edges[1]
#    )
#    assert len(g.edges[1]) == 1
#    # depth 0
#    assert wlkernel.WLRDFNode(label='D', depth=0) in g.nodes[0]
#    assert wlkernel.WLRDFNode(label='E', depth=0) in g.nodes[0]
#    assert len(g.nodes[0]) == 2
#    assert (
#            wlkernel.WLRDFEdge(wlkernel.WLRDFNode('A2', 1),
#                          wlkernel.WLRDFNode('D', 0), 'P2', 0) in g.edges[0]
#    )
#    assert (
#            wlkernel.WLRDFEdge(wlkernel.WLRDFNode('A2', 1),
#                          wlkernel.WLRDFNode('E', 0), 'P3', 0) in g.edges[0]
#    )
#    assert len(g.edges[0]) == 2


#def test_wlrdfgraph_repr():
#    graph = rdflib.Graph().parse('./example.ttl', format='turtle')
#
#    max_depth = 1
#    root = wlkernel.WLRDFNode(label='', depth=max_depth)
#    wl_rdf_graph = wlkernel.WLRDFGraph('B1', graph, max_depth)
#    assert root in wl_rdf_graph.nodes[max_depth]
#    assert (
#        "defaultdict(<class 'list'>, {0: [WLRDFEdge(source=WLRDFNode(label='', "
#        "depth=1), dest=WLRDFNode(label='F', depth=0), label='P3', "
#        "depth=0), WLRDFEdge(source=WLRDFNode(label='', depth=1), dest=WLRDFNode(label='G', "
#        "depth=0), label='P2', depth=0)]})" == repr(wl_rdf_graph) or
#        "defaultdict(<class 'list'>, {0: [WLRDFEdge(source=WLRDFNode(label='', depth=1),"
#        " dest=WLRDFNode(label='G', depth=0), label='P2', depth=0), "
#        "WLRDFEdge(source=WLRDFNode(label='', depth=1), dest=WLRDFNode(label='F', depth=0), "
#        "label='P3', depth=0)]})" == repr(wl_rdf_graph)
#    )
