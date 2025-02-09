import queue


class UGraph:
    "Undirected graph."

    edges: dict[str, list[str]]

    def __init__(self):
        self.edges = {}

    @property
    def nodes(self):
        return self.edges.keys()

    def add_node(self, node: str):
        self.edges[node] = []

    def add_edge(self, start: str, end: str):
        self.edges.setdefault(start, []).append(end)
        self.edges.setdefault(end, []).append(start)

    def neighbors_of(self, node: str):
        yield from self.edges[node]


class DiGraph:
    "Directed graph."

    edges: dict[str, list[str]]

    def __init__(self):
        self.edges = {}

    @property
    def nodes(self):
        return self.edges.keys()

    def add_node(self, node: str):
        if node not in self.edges:
            self.edges[node] = []

    def add_edge(self, start: str, end: str):
        self.edges.setdefault(start, []).append(end)
        self.add_node(end)

    def neighbors_of(self, node: str):
        yield from self.edges[node]

    def toposort(self):
        "Return a topological sort of nodes."

        order = []
        num_inbound_edges = {}
        for v, out_edges in self.edges.items():
            for nd in out_edges:
                num_inbound_edges[nd] = num_inbound_edges.get(nd, 0) + 1

        queue = list(self.edges.keys() - num_inbound_edges.keys())
        while len(queue):
            nd = queue.pop()
            for neigh in self.edges[nd]:
                num_inbound_edges[neigh] -= 1
                if num_inbound_edges[neigh] == 0:
                    queue.append(neigh)
            order.append(nd)

        assert len(order) == len(self.edges)
        return order

    def render(
        self,
        filename: str,
        directory: str | None = None,
        node_shapes: dict | None = None,
    ):
        "Render the graph with graphviz to a png file."

        try:
            import graphviz
        except ImportError:
            print('To render graph install the graphviz package.')
            return

        dot = graphviz.Digraph(comment='Directed Graph')

        if node_shapes is None:
            node_shapes = {node: 'ellipse' for node in self.edges}

        for node, shape in node_shapes.items():
            dot.node(node, shape=shape)  # Set the shape of the node

        for start in self.edges:
            for end in self.edges[start]:
                dot.edge(start, end)
        dot.render(
            filename or 'graph_output', directory=directory, format='png', cleanup=True
        )
