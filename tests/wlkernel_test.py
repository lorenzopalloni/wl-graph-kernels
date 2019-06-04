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


def test_relabel():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wlrdf_graph = wlkernel.WLRDFGraph(triples, ['A1', 'B1'], 4)
    uniq_labels_0 = set(wlrdf_graph.labels[0].values())
    wlrdf_graph.relabel()
    uniq_labels_1 = set(wlrdf_graph.labels[1].values())
    wlrdf_graph.relabel()
    uniq_labels_2 = set(wlrdf_graph.labels[1].values())
    assert len(uniq_labels_0) < len(uniq_labels_1)
    assert len(uniq_labels_1) == len(uniq_labels_2)


def test_kernel():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wlrdf_graph = wlkernel.WLRDFGraph(triples, ['A1', 'B1'], 4)
    assert wlkernel.wlrdf_kernel(wlrdf_graph, 'A1', 'B1') == 10*1
    assert wlkernel.wlrdf_kernel(wlrdf_graph, 'A1', 'B1', 1) == 10*0.5 + 3
