import os
from aoc_utils.graph import DiGraph

def test_viz():
    graph = DiGraph()
    graph.add_node('A')
    graph.add_node('B')
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')

    # Generate and render the graph.
    graph.render(filename='test_graph', directory='/tmp')
    assert os.path.isfile('/tmp/test_graph.png')
