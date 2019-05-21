class Node:
    'A node of a Weisfeiler-Lehman RDF graph'

    def __init__(self, label: str, depth: int):
        self.label = label
        self.depth = depth
        self.neighbors = []

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

    def __repr__(self):
        return (
            f'Edge(source={repr(self.source)}, dest={repr(self.dest)}, '
            f'label={self.label}, depth={self.depth})'
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
    'Weisfeiler-Lehman RDF graph'

    def __init__(self):
        self.nodes = []
        self.edges = []

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __eq__(self):
        pass
