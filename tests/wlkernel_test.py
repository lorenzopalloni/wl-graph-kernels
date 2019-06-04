from os.path import abspath
from pkg_resources import resource_filename

import pytest
import rdflib

import wlkernel


example_data = abspath(resource_filename('tests.resources', 'example.ttl'))


def test_node_hash():
    n1 = wlkernel.Node()
    n1_bis = n1
    n2 = wlkernel.Node()
    n2_bis = n2
    assert hash(n1) != hash(n2)
    assert hash(n1) == hash(n1_bis)
    assert hash(n2) == hash(n2_bis)


def test_edge_hash():
    e1 = wlkernel.Edge()
    e1_bis = e1
    e2 = wlkernel.Edge()
    e2_bis = e2
    assert hash(e1) != hash(e2)
    assert hash(e1) == hash(e1_bis)
    assert hash(e2) == hash(e2_bis)


def test_wlrdfgraph_depth_0():
    '''
    ######
    # A1 #
    ######
    '''
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wlrdf_graph = wlkernel.WLRDFGraph(triples, ['A1'], 0)
    assert len(wlrdf_graph.nodes) == 1
    assert len(wlrdf_graph.edges) == 0
    assert len(wlrdf_graph.labels) == 1
    assert len(wlrdf_graph.labels[0]) == 1
    assert len(wlrdf_graph.instance_nodes) == 1
    assert len(wlrdf_graph.instance_nodes['A1']) == 0
    assert len(wlrdf_graph.instance_edges) == 1
    assert len(wlrdf_graph.instance_edges['A1']) == 0


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
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wlrdf_graph = wlkernel.WLRDFGraph(triples, ['A1'], 1)
    assert len(wlrdf_graph.nodes) == 3
    assert len(wlrdf_graph.edges) == 2
    assert len(wlrdf_graph.labels) == 1
    assert len(wlrdf_graph.labels[0]) == 5
    assert len(wlrdf_graph.instance_nodes) == 1
    assert len(wlrdf_graph.instance_nodes['A1']) == 2
    assert len(wlrdf_graph.instance_edges) == 1
    assert len(wlrdf_graph.instance_edges['A1']) == 2


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
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wlrdf_graph = wlkernel.WLRDFGraph(triples, ['A1'], 2)
    assert len(wlrdf_graph.nodes) == 4
    assert len(wlrdf_graph.edges) == 4
    assert len(wlrdf_graph.labels) == 1
    assert len(wlrdf_graph.labels[0]) == 8
    assert len(wlrdf_graph.instance_nodes) == 1
    assert len(wlrdf_graph.instance_nodes['A1']) == 3
    assert len(wlrdf_graph.instance_edges) == 1
    assert len(wlrdf_graph.instance_edges['A1']) == 4
#
#
#def test_graph_relabeling():
#    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
#    wl_graph_a1 = wlkernel.WLRDFSubgraph('A1', rdf_graph, 4)
#    wl_graph_b1 = wlkernel.WLRDFSubgraph('B1', rdf_graph, 4)
#    a1_relabeled, b1_relabeled = wlkernel.relabel(wl_graph_a1, wl_graph_b1)
#
#    assert (
#        a1_relabeled.root == b1_relabeled.root
#        == a1_relabeled.nodes[4][0] == b1_relabeled.nodes[4][0]
#    )
#
#    edge_labels = [
#        e.label for e in chain(a1_relabeled.edges[3], b1_relabeled.edges[3])
#    ]
#    assert len(edge_labels) == 4
#    assert len(set(edge_labels)) == 2
#    node_labels = [
#        n.label for n in chain(a1_relabeled.nodes[3], b1_relabeled.nodes[3])
#    ]
#    assert len(node_labels) == 4
#    assert len(set(node_labels)) == 4
#
#    edge_labels = [
#        e.label for e in chain(a1_relabeled.edges[2], b1_relabeled.edges[2])
#    ]
#    assert len(edge_labels) == 4
#    assert len(set(edge_labels)) == 4
#    node_labels = [
#        n.label for n in chain(a1_relabeled.nodes[2], b1_relabeled.nodes[2])
#    ]
#    assert len(node_labels) == 2
#    assert len(set(node_labels)) == 2
#
#    edge_labels = [
#        e.label for e in chain(a1_relabeled.edges[1], b1_relabeled.edges[1])
#    ]
#    assert len(edge_labels) == 2
#    assert len(set(edge_labels)) == 2
#    node_labels = [
#        n.label for n in chain(a1_relabeled.nodes[1], b1_relabeled.nodes[1])
#    ]
#    assert len(node_labels) == 2
#    assert len(set(node_labels)) == 2
#
#    edge_labels = [
#        e.label for e in chain(a1_relabeled.edges[0], b1_relabeled.edges[0])
#    ]
#    assert len(edge_labels) == 4
#    assert len(set(edge_labels)) == 4
#    node_labels = [
#        n.label for n in chain(a1_relabeled.nodes[0], b1_relabeled.nodes[0])
#    ]
#    assert len(node_labels) == 4
#    assert len(set(node_labels)) == 3
#
#
#def test_wl_kernel():
#    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
#    wl_graph_a1 = wlkernel.WLRDFSubgraph('A1', rdf_graph, 4)
#    wl_graph_b1 = wlkernel.WLRDFSubgraph('B1', rdf_graph, 4)
#    assert wlkernel.wl_kernel(wl_graph_a1, wl_graph_b1) == 7
#
#    a1_relabeled, b1_relabeled = wlkernel.relabel(wl_graph_a1, wl_graph_b1)
#    assert wlkernel.wl_kernel(wl_graph_a1, wl_graph_b1) == 4
#
#
#def test_compute_kernel():
#    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
#    kernel = wlkernel.compute_kernel(rdf_graph, 'A1', 'B1', 4)
#    assert kernel == 7
#
#    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
#    kernel = wlkernel.compute_kernel(rdf_graph, 'A1', 'B1', 4, iterations=2)
#    assert kernel == 7*1/2 + 4*2/2
#
#    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
#    kernel = wlkernel.compute_kernel(rdf_graph, 'A1', 'B1', 4, iterations=3)
#    assert kernel == 7*1/3 + 4*2/3 + 3*3/3
