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


def test_wlgraph_depth_0():
    '''
    ######
    # A1 #
    ######
    '''
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wl_graph = wlkernel.WLGraph(triples, 'A1', 0)
    assert len(wl_graph.nodes) == 1
    assert len(wl_graph.edges) == 0
    assert len(wl_graph.labels) == 1
    assert len(wl_graph.labels[0]) == len(wl_graph.nodes) + len(wl_graph.edges)


def test_wlgraph_depth_1():
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
    wl_graph = wlkernel.WLGraph(triples, 'A1', 1)
    assert len(wl_graph.nodes) == 3
    assert len(wl_graph.edges) == 2
    assert len(wl_graph.labels) == 1
    assert len(wl_graph.labels[0]) == len(wl_graph.nodes) + len(wl_graph.edges)


def test_wlgraph_depth_2():
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
    wl_graph = wlkernel.WLGraph(triples, 'A1', 2)
    assert len(wl_graph.nodes) == 4
    assert len(wl_graph.edges) == 4
    assert len(wl_graph.labels) == 1
    assert len(wl_graph.labels[0]) == len(wl_graph.nodes) + len(wl_graph.edges)


def test_wlgraph_depth_4():
    r'''
          ######
          # A1 #
          ######
          /    \
      P2 /      \ P3
        /        \
    #####        #####
    # C #        # D #<----
    #####        #####    |
        \       /         |
      P4 \     / P4       |
          \   /           |
          #####           |
          # H #           | P2
          #####           |
            |             |
            | P6          |
            |             |
          ######          |
          # A2 #-----------
          ######
            |
            | P3
            |
          #####
          # E #
          #####
    '''
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wl_graph = wlkernel.WLGraph(triples, 'A1', 4)
    assert len(wl_graph.nodes) == 6
    assert len(wl_graph.edges) == 7
    assert len(wl_graph.labels) == 1
    assert len(wl_graph.labels[0]) == len(wl_graph.nodes) + len(wl_graph.edges)


def test_wl_relabel():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = [(str(s), str(p), str(o)) for s, p, o in rdf_graph]
    wl_graph_a1 = wlkernel.WLGraph(triples, 'A1', 4)
    wl_graph_b1 = wlkernel.WLGraph(triples, 'B1', 4)

    uniq_labels_a1_0 = set(wl_graph_a1.labels[0].values())
    uniq_labels_b1_0 = set(wl_graph_b1.labels[0].values())

    wlkernel.wl_relabel([wl_graph_a1, wl_graph_b1])
    uniq_labels_a1_1 = set(wl_graph_a1.labels[1].values())
    uniq_labels_b1_1 = set(wl_graph_b1.labels[1].values())
    assert len(wl_graph_a1.labels) == len(wl_graph_b1.labels) == 2
    assert len(uniq_labels_a1_0) < len(uniq_labels_a1_1)
    assert len(uniq_labels_b1_0) < len(uniq_labels_b1_1)

    wlkernel.wl_relabel([wl_graph_a1, wl_graph_b1])
    uniq_labels_a1_2 = set(wl_graph_a1.labels[2].values())
    uniq_labels_b1_2 = set(wl_graph_b1.labels[2].values())
    assert len(wl_graph_a1.labels) == len(wl_graph_b1.labels) == 3

    wlkernel.wl_relabel([wl_graph_a1, wl_graph_b1])
    uniq_labels_a1_3 = set(wl_graph_a1.labels[3].values())
    uniq_labels_b1_3 = set(wl_graph_b1.labels[3].values())
    assert len(wl_graph_a1.labels) == len(wl_graph_b1.labels) == 4


def test_wl_kernel():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = [(str(s), str(p), str(o)) for s, p, o in rdf_graph]
    wl_graph_a1 = wlkernel.WLGraph(triples, 'A1', 4)
    wl_graph_b1 = wlkernel.WLGraph(triples, 'B1', 4)

    assert wlkernel.wl_kernel(wl_graph_a1, wl_graph_b1) == 11*1
    assert wlkernel.wl_kernel(wl_graph_a1, wl_graph_b1, 1) == 11*0.5 + 4*1


def test_wl_kernel_matrix():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = [(str(s), str(p), str(o)) for s, p, o in rdf_graph]
    wl_graph_a1 = wlkernel.WLGraph(triples, 'A1', 4)
    wl_graph_b1 = wlkernel.WLGraph(triples, 'B1', 4)
    wl_graph_a2 = wlkernel.WLGraph(triples, 'A2', 4)

    kernel_matrix = wlkernel.wl_kernel_matrix(
        [wl_graph_a1, wl_graph_b1, wl_graph_a2], iterations=1
    )

    assert len(kernel_matrix) == len(kernel_matrix[0]) == 3
    assert kernel_matrix[0][1] == wlkernel.wl_kernel(
        wl_graph_a1, wl_graph_b1, iterations=1
    )
    assert kernel_matrix[0][2] == wlkernel.wl_kernel(
        wl_graph_a1, wl_graph_a2, iterations=1
    )
    assert kernel_matrix[1][0] == wlkernel.wl_kernel(
        wl_graph_a1, wl_graph_b1, iterations=1
    )


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


def test_wlrdfgraph_depth_4():
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
            |
            | P6
            |
          ######
          # A2 #
          ######
          /    \
      P3 /      \ P2
        /        \
     #####     #####
     # E #     # D #
     #####     #####
    '''
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wlrdf_graph = wlkernel.WLRDFGraph(triples, ['A1'], 4)
    assert len(wlrdf_graph.nodes) == 6
    assert len(wlrdf_graph.edges) == 7
    assert len(wlrdf_graph.labels) == 1
    assert len(wlrdf_graph.labels[0]) == 14
    assert len(wlrdf_graph.instance_nodes) == 1
    assert len(wlrdf_graph.instance_nodes['A1']) == 5
    assert len(wlrdf_graph.instance_edges) == 1
    assert len(wlrdf_graph.instance_edges['A1']) == 7


def test_wlrdf_relabel():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wlrdf_graph = wlkernel.WLRDFGraph(triples, ['A1', 'B1'], 4)

    uniq_labels_0 = set(wlrdf_graph.labels[0].values())

    wlrdf_graph.relabel()
    uniq_labels_1 = set(wlrdf_graph.labels[1].values())

    wlrdf_graph.relabel()
    uniq_labels_2 = set(wlrdf_graph.labels[1].values())

    assert len(wlrdf_graph.labels) == 3
    assert len(uniq_labels_0) < len(uniq_labels_1)
    assert len(uniq_labels_1) == len(uniq_labels_2)


def test_wlrdf_kernel():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wlrdf_graph = wlkernel.WLRDFGraph(triples, ['A1', 'B1'], 4)
    assert wlkernel.wlrdf_kernel(wlrdf_graph, 'A1', 'B1') == 10*1
    assert wlkernel.wlrdf_kernel(wlrdf_graph, 'A1', 'B1', 1) == 10*0.5 + 3


def test_wlrdf_kernel_matrix():
    rdf_graph = rdflib.Graph().parse(example_data, format='turtle')
    triples = ((str(s), str(p), str(o)) for s, p, o in rdf_graph)
    wlrdf_graph = wlkernel.WLRDFGraph(triples, ['A1', 'B1'], 4)

    kernel_matrix = wlkernel.wlrdf_kernel_matrix(wlrdf_graph, ['A1', 'B1'])

    assert len(kernel_matrix) == len(kernel_matrix[0]) == 2
    assert kernel_matrix[0][1] == wlkernel.wlrdf_kernel(
        wlrdf_graph, 'A1', 'B1'
    )
    assert kernel_matrix[1][0] == wlkernel.wlrdf_kernel(
        wlrdf_graph, 'A1', 'B1'
    )
