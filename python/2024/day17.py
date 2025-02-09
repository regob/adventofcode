"""Advent of code 2024 day 17, 8-bit machine instruction decoding problem."""

from dataclasses import dataclass
from typing import Iterable
from aoc_utils.load_input import read_input

# part 1 ######################################################################
# Simulate the machine on the input. I added cycle detection by tracking execution
# states and expected output matching, which help reducing execution time for part 2
# (but brute force does not work there anyway ...)


@dataclass
class ExecutionState:
    "Immutable state of the machine for cycle detection."

    ipr: int
    reg: tuple[int, ...]

    def __hash__(self) -> int:
        return hash((self.ipr, self.reg))


class CycleError(Exception):
    pass


class OutputNoMatch(Exception):
    pass


class Machine:
    program: tuple[int, ...] | None = None
    ipr: int = 0
    reg: list[int]
    output: list[int] = []
    states: set[ExecutionState] | None = None

    def __init__(self, reg: list[int]):
        self.reg = list(reg)

    def _combo(self, op: int):
        if op == 7:
            raise ValueError('Invalid combo operand: 7')
        return self.reg[op - 4] if op >= 4 else op

    def _xdv(self, op: int, register: int):
        self.reg[register] = self.reg[0] // (1 << self._combo(op))

    def _jnz(self, op: int):
        if self.reg[0] == 0:
            return
        self.ipr = op

    def _bst(self, op: int):
        self.reg[1] = self._combo(op) % 8

    def _bxl(self, op: int):
        self.reg[1] = op ^ self.reg[1]

    def _bxc(self, op: int):
        self.reg[1] = self.reg[1] ^ self.reg[2]

    def _out(self, op: int):
        self.output.append(self._combo(op) % 8)

    def _state(self):
        return ExecutionState(self.ipr, tuple(self.reg))

    def run_program(
        self,
        program: tuple[int, ...],
        ipr: int = 0,
        expected_output: list[int] | None = None,
    ):
        "Reset state and run a program, possibly watching if the output matches the expected."
        self.program = program
        self.ipr = ipr
        self.states = set()
        self.output = []

        while self.ipr < len(self.program) - 1:
            s = self._state()
            if s in self.states:
                raise CycleError()
            self.states.add(s)

            opcode, op = self.program[self.ipr : self.ipr + 2]
            self.ipr += 2

            match opcode:
                case 0:
                    self._xdv(op, 0)
                case 1:
                    self._bxl(op)
                case 2:
                    self._bst(op)
                case 3:
                    self._jnz(op)
                case 4:
                    self._bxc(op)
                case 5:
                    self._out(op)
                    if expected_output is not None and (
                        len(self.output) > len(expected_output)
                        or self.output[-1] != expected_output[len(self.output) - 1]
                    ):
                        raise OutputNoMatch()
                case 6:
                    self._xdv(op, 1)
                case 7:
                    self._xdv(op, 2)
        return ','.join(str(x) for x in self.output)


def parse_input(s: str):
    s_regs, program = s.strip().split('\n\n')
    reg = [int(r.split(':')[-1].strip()) for r in s_regs.split('\n')]
    p = tuple(int(x) for x in program.split(':')[-1].split(','))
    assert len(p) % 2 == 0
    return reg, p


reg, program = parse_input(read_input(17, 2024, postfix=""))
machine = Machine(reg)
ans = machine.run_program(program)
print('part 1:', ans)

# part 2 ######################################################################
# Since the program is pretty short, we can reverse engineer what A produces the result.
# Brute force does not work, since in each iteration the content of register A is
# reduced by 3 bits, and the output is 16 numbers, which means the number is around 2^48.
#
# Decoding the instructions:
#
# | instruction | A      | B                | C            | comment             |
# |-------------+--------+------------------+--------------+---------------------|
# | bst(4)      | x      | x % 8            | 0            |                     |
# | bxl(1)      | x      | b1 = (x % 8) ^ 1 | 0            |                     |
# | cdv(5)      | x      | b1               | c1 = x >> b1 |                     |
# | bxl(5)      | x      | b2 = b1 ^ 5      | c1           |                     |
# | bxc(5)      | x      | b2 ^ c1          | c1           |                     |
# | adv(3)      | x >> 3 | b2 ^ c1          | c1           |                     |
# | out(5)      | x >> 3 | b2 ^ c1          | c1           | outputs B % 8       |
# | jnz(0)      | x >> 3 | b2 ^ c1          | c1           | jumps to 0 if A > 0 |
#
# Each iteration we slice off the last 3 bits of A into B. Solving for the output (o):
#     b2 ^ c1 = o               <--- drop the % 8 here, we only care about the last 3 bits
#     (b1 ^ 5) ^ (x >> b1 % 8) = o
#     b1 ^ (x >> b1) = o ^ 5
#     x >> b1 = o ^ 5 ^ b1
#
# This gives constraints on the last 3 bits of x (which give b1),
# and the bits (head) b1 to b1 + 2 (possibly zero), which remain after the shift.
# This is tricky, since b1 also depends on x. There are three cases:
# - b1 <= bits(x) - 3: Shifted head completely fits into x, the 3 bits have to match
# - bits(x) - 3 < b1 < bits(x): 1 or 2 bits overlap, the overlapping bits have to match
# - bits(x) <= b1: no overlap, any bits in between the head and tail have to be brute forced


# this does not work for the real input, only for the sample
def brute_force_register(reg, program, exp_output, n_iter=1000000):
    reg = list(reg)

    for i in range(0, n_iter):
        reg[0] = i
        m = Machine(reg)
        try:
            out = m.run_program(program, expected_output=exp_output)
        except (CycleError, OutputNoMatch):
            continue

        if exp_output != tuple(m.output):
            continue
        return i


def all_a_satisfying(
    dig_tail: int, tail_length: int, dig_shr_tail_three: int, shr_bits: int
):
    """Return all numbers that satisfy bitwise conditions.

    - The last `tail_length` bits are the same as `dig_tail`.
    - Three bits match `dig_shr_tail_three` between 2^shr_bits and 2^{shr_bits + 2}.
    """
    sh_tail = dig_shr_tail_three << shr_bits

    # All bits of head are inside the tail
    if shr_bits <= tail_length - 3:
        # shifted tail is within the current tail
        x = dig_tail ^ sh_tail
        # all three bits match
        if (x >> shr_bits) % 8 == 0:
            yield dig_tail
        return

    # There is 1 or 2 overlapping bits between the head and tail, they have to match
    if shr_bits < tail_length:
        x = dig_tail ^ sh_tail
        if (x >> shr_bits) % (1 << (tail_length - shr_bits)) == 0:
            yield dig_tail | sh_tail
        return

    # no overlapping bits, and no bits between
    if shr_bits == tail_length:
        yield dig_tail | sh_tail
        return

    # no overlapping bits, brute force bits in between
    n_bits = shr_bits - tail_length
    for i in range(1 << n_bits):
        yield sh_tail | (i << tail_length) | dig_tail


assert list(all_a_satisfying(7, 3, 7, 0)) == [7]
assert list(all_a_satisfying(5, 3, 6, 1)) == [13]
assert list(all_a_satisfying(9, 5, 5, 3)) == [41]
assert list(all_a_satisfying(6, 3, 5, 5)) == [166, 174, 182, 190]


def backtrack_register(
    a_tail: int, tail_length: int, output: tuple[int, ...]
) -> Iterable[int]:
    """Find all register values that have a certain tail and produce the output."""
    o = output[0] ^ 5

    # Generate all possible last 3 bits (if a_tail has less than 3 bits specified)
    tails = []
    if tail_length < 3:
        gen_bits = 3 - tail_length
        for x in range(1 << gen_bits):
            tails.append((x << tail_length) | a_tail)
        tail_length = 3
    else:
        tails.append(a_tail)

    for tail in tails:
        b1 = (tail % 8) ^ 1
        a_head = o ^ b1

        next_a_bits = max(tail_length - 3, b1)
        for a in all_a_satisfying(tail, tail_length, a_head % 8, b1):
            if len(output) > 1:
                xs = backtrack_register(a >> 3, next_a_bits, output[1:])
                for x in xs:
                    yield (x << 3) | tail
            elif a >> 3 == 0:
                yield a
    return


a_registers = list(backtrack_register(0, 0, program))
ans = min(a_registers)
print('part 2:', ans)
