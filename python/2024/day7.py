# pyright: reportOperatorIssue=false
import itertools
import operator
from aoc_utils.load_input import read_input_lines

g = read_input_lines(7, postfix="")


def parse_line(line):
    target, nums = line.split(':')
    return (int(target), list(map(int, nums.strip().split())))


# part 1 ######################################################################

OP_MAP = {
    '*': operator.mul,
    '+': operator.add,
}


def eval_expr_left_to_right(tokens):
    total = tokens[0]
    for i in range(1, len(tokens), 2):
        total = OP_MAP[tokens[i]](total, tokens[i + 1])
    return total


def all_operation_variants(nums):
    for ops in itertools.product(*[list(OP_MAP.keys()) for _ in range(len(nums) - 1)]):
        tokens = [nums[0]]
        for op, num in zip(ops, nums[1:]):
            tokens.append(op)
            tokens.append(num)
        yield tokens


def can_satisfy(total, nums):
    for tokens in all_operation_variants(nums):
        if eval_expr_left_to_right(tokens) == total:
            return True
    return False


rows = [parse_line(line) for line in g]
total = 0
for s, nums in rows:
    if can_satisfy(s, nums):
        total += s
print('part 1', total)

# part 2 ######################################################################

OP_MAP['||'] = lambda x, y: int(str(x) + str(y))
total = 0
for s, nums in rows:
    if can_satisfy(s, nums):
        total += s
print('part 2', total)
