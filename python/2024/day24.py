from copy import deepcopy
from dataclasses import dataclass
import random
import re
import networkx as nx
from aoc_utils.load_input import read_input
from aoc_utils.graph import DiGraph

# part 1 ######################################################################
# Build a graph of input gates, then simulate the network.


@dataclass
class NetworkNode:
    var: str

    @property
    def output(self):
        raise NotImplementedError("Output method must be implemented.")


@dataclass(repr=False)
class Input(NetworkNode):
    value: bool

    @property
    def output(self):
        return self.value

    def __repr__(self) -> str:
        return f"Input({self.var})"


@dataclass(repr=False)
class BinaryGate(NetworkNode):
    input1: NetworkNode
    input2: NetworkNode

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.var},{self.input1.var},{self.input2.var})"


@dataclass(repr=False)
class AndGate(BinaryGate):
    @property
    def output(self):
        return self.input1.output and self.input2.output


@dataclass(repr=False)
class OrGate(BinaryGate):
    @property
    def output(self):
        return self.input1.output or self.input2.output


@dataclass(repr=False)
class XorGate(BinaryGate):
    @property
    def output(self):
        return self.input1.output ^ self.input2.output


class Network:
    """A network of inputs and binary gates."""

    gates: dict[str, NetworkNode]
    inputs: list[Input]
    outputs: list[str]

    def __init__(self, gates: list[NetworkNode], inputs: list[str], outputs: list[str]):
        self.gates = {g.var: g for g in gates}
        self.inputs = [self.gates[v] for v in inputs]
        self.outputs = list(outputs)

    def output(self, input_values: list[bool]) -> list[bool]:
        if len(input_values) != len(self.inputs):
            raise ValueError('Number of inputs passed != inputs in the network.')

        for input_, value in zip(self.inputs, input_values):
            input_.value = value

        out = [self.gates[v].output for v in self.outputs]
        return out


def parse_input(text: str) -> tuple[Network, DiGraph]:
    "Parse the list of input and gate specs into a gate network."
    chunks = text.strip().split('\n\n')
    gate_pattern = re.compile(r'(\w+) ([A-Z]+) (\w+) -> (\w+)')
    assert len(chunks) == 2

    inputs = []
    gates = {}

    for line in chunks[0].split('\n'):
        var, val = line.split(': ')
        inputs.append(var)
        gates[var] = Input(var, (val == '1'))

    # graph of gates/inputs for creating a topological sort
    graph = DiGraph()

    for line in chunks[1].split('\n'):
        g = gate_pattern.match(line).groups()

        gates[g[3]] = g
        graph.add_edge(g[0], g[3])
        graph.add_edge(g[2], g[3])

    # parse gate tuples into gate objects in topological order
    order = graph.toposort()
    outputs = set(order)
    for nd in order:
        if isinstance(gates[nd], Input):
            continue
        g = gates[nd]
        outputs.discard(g[0])
        outputs.discard(g[2])

        g_left = gates[g[0]]
        g_right = gates[g[2]]
        if g[1] == 'AND':
            gate = AndGate(g[3], g_left, g_right)
        elif g[1] == 'OR':
            gate = OrGate(g[3], g_left, g_right)
        elif g[1] == 'XOR':
            gate = XorGate(g[3], g_left, g_right)
        else:
            raise ValueError(f'Invalid gate type: {g[1]}')
        gates[nd] = gate

    n = Network(list(gates.values()), sorted(inputs), sorted(outputs))
    return n, graph


input_txt = read_input(24, 2024, postfix="")
network, graph = parse_input(input_txt)
input_values = [x.value for x in network.inputs]
ans_bin = ''.join(map(lambda x: str(int(x)), reversed(network.output(input_values))))
ans = int(ans_bin, 2)
print('part 1:', ans)


# part 2 ######################################################################
# I simulate random inputs and check how many errors each bit position has.
# This allows the detection of errors one-by-one. The biggest help was
# plotting the circuit with the graphviz package which makes it very easy to inspect
# the erroneous gates.


def bitarray_to_bitstring(bits: list[bool]) -> str:
    return ''.join(list(map(lambda x: str(int(x)), bits)))


def bitarray_sum(x1: list[bool], x2: list[bool]) -> list[bool]:
    "Add two big-endian bitarrays."
    s1 = bitarray_to_bitstring(x1)
    s2 = bitarray_to_bitstring(x2)
    n = int(s1, 2) + int(s2, 2)
    # convert integer to boolean bit array
    bits = [(x == '1') for x in format(n, 'b')]
    return [False] * (len(s1) + 1 - len(bits)) + bits


def simulate_gate_errors(n: Network, n_repeat: int = 100):
    "Run the network repeatedly and check the number of errors in each output bit."
    bit_width = len(n.inputs) // 2
    swap_errors = [0] * bit_width

    for _ in range(n_repeat):
        input1 = [(random.random() > 0.5) for _ in range(bit_width)]
        input2 = [(random.random() > 0.5) for _ in range(bit_width)]
        exp_output = list(
            reversed(bitarray_sum(list(reversed(input1)), list(reversed(input2))))
        )
        assert exp_output[0] == input1[0] ^ input2[0]
        output = n.output(input1 + input2)
        assert len(exp_output) == len(output), f'{len(exp_output)},{len(output)}'
        for i in range(bit_width):
            if exp_output[i] != output[i]:
                swap_errors[i] += 1

    return swap_errors


def swap_input_gates(input_txt: str, gate_pairs: list[tuple[str, str]]) -> str:
    "Swap a number of gates in the input string of gate specs."
    gate_pattern = re.compile(r'.* -> (\w+)')
    gate_swaps = {}
    for var1, var2 in gate_pairs:
        gate_swaps[var1] = var2
        gate_swaps[var2] = var1

    lines = input_txt.split('\n')
    for i in range(len(lines)):
        m = gate_pattern.match(lines[i])
        if m and m.groups()[0] in gate_swaps:
            var = m.groups()[0]
            lines[i] = lines[i].replace(var, gate_swaps[var])
    return '\n'.join(lines)


def plot_circuit(network: Network, graph: DiGraph):
    "Plot the circuit's graph with graphviz."
    SHAPE_MAP = {
        OrGate: 'ellipse',
        XorGate: 'diamond',
        AndGate: 'box',
        Input: 'circle',
    }

    shapes = {var: SHAPE_MAP[gate.__class__] for var, gate in network.gates.items()}  # pyright: ignore
    graph.render('graph', node_shapes=shapes)


swaps = [('z23', 'rmj'), ('z17', 'cmv'), ('z30', 'rdg'), ('mwp', 'btb')]
input_fixed = swap_input_gates(input_txt, swaps)
network_fixed, graph_fixed = parse_input(input_fixed)
# plot_circuit(network_fixed, graph_fixed)

# errors = simulate_gate_errors(network, 10000)
# for i in range(len(errors)):
#     print(f'z{i}', errors[i])

sorted_res = sorted([x for pair in swaps for x in pair])
print('part 2:', ','.join(sorted_res))

# other attempts #######################################################################


def swap_gates(n: Network, var1: str, var2: str):
    gate1 = n.gates[var1]
    gate2 = n.gates[var2]

    if not isinstance(gate1, BinaryGate) or not isinstance(gate2, BinaryGate):
        raise TypeError('Can only swap gates and not inputs.')

    assert gate2 not in [gate1.input1, gate1.input2]
    assert gate1 not in [gate2.input1, gate2.input2]

    gate1 = gate2.__class__(var1, gate2.input1, gate2.input2)
    gate2 = gate1.__class__(var2, gate1.input1, gate1.input2)
    network.gates[var1] = gate1
    network.gates[var2] = gate2

    for var, g in n.gates.items():
        if not isinstance(g, BinaryGate):
            continue
        if g.input1.var == var1:
            g.input1 = gate1
        if g.input1.var == var2:
            g.input1 = gate2
        if g.input2.var == var1:
            g.input2 = gate1
        if g.input2.var == var2:
            g.input2 = gate2
