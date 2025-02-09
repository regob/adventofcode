from aoc_utils.load_input import read_input_lines

# part 1 ######################################################################
# Iterate all edges (pairs of connected vertices), and calculate the intersection
# of the neighbors of the two nodes: O(E * V)


class UGraph:
    "Undirected graph."

    edges: dict[str, set[str]]

    def __init__(self):
        self.edges = {}

    @property
    def nodes(self):
        return self.edges.keys()

    def add_node(self, node: str):
        self.edges[node] = set()

    def add_edge(self, start: str, end: str):
        self.edges.setdefault(start, set()).add(end)
        self.edges.setdefault(end, set()).add(start)

    def neighbors_of(self, node: str):
        yield from self.edges[node]


def parse_edges(rows: list[str]):
    g = UGraph()
    for st, end in (x.strip().split('-') for x in rows):
        g.add_edge(st, end)
    return g


def all_triangles_brute(g: UGraph):
    for nd in g.nodes:
        for nd2 in g.neighbors_of(nd):
            for nd3 in g.edges[nd] & g.edges[nd2]:
                if nd2 > nd and nd3 > nd2:
                    yield (nd, nd2, nd3)


def num_triangles_with_node_t_brute(g: UGraph):
    return sum(
        1 for tri in all_triangles_brute(g) if any(x.startswith('t') for x in tri)
    )


rows = read_input_lines(23, 2024, postfix="")
g = parse_edges(rows)

triangles = num_triangles_with_node_t_brute(g)
print('part 1:', triangles)


# part 2 ######################################################################
# The largest clique problem is NP-complete.
# 1. Take all triangles, and try to extend them by one node at a time, always storing
#    the set of candidate nodes that all current nodes have an edge to.
# 2. Do the same with optimized data structures (bitset instead of hashset)
# 3. maybe add coloring as described in https://en.wikipedia.org/wiki/MaxCliqueDyn_algorithm


def largest_clique_including(
    g: UGraph,
    nodes: tuple[str, ...],
    candidates: set[str] | None = None,
    best_found: int = 0,
):
    "Largest clique in the graph including a set of nodes (assumed to form a clique already)."
    if candidates is None:
        candidates = set.intersection(*(g.edges[nd] for nd in nodes))
    if best_found >= len(nodes) + len(candidates):
        return tuple()
    if candidates:
        mx = nodes
        for nd in candidates:
            clique_nodes = largest_clique_including(
                g,
                nodes + (nd,),
                candidates & g.edges[nd],
                best_found=max(best_found, len(mx)),
            )
            if len(clique_nodes) > len(mx):
                mx = clique_nodes
        return mx
    return nodes


def largest_clique_triangle_brute(g: UGraph):
    mx_clique = tuple()
    for i, nodes in enumerate(all_triangles_brute(g)):
        clique = largest_clique_including(g, nodes, best_found=len(mx_clique))
        if len(clique) > len(mx_clique):
            mx_clique = clique
    return mx_clique


clique = largest_clique_triangle_brute(g)
ans = ','.join(sorted(clique))
print('part 2:', ans)
