from aoc_utils.load_input import read_input_lines

g = read_input_lines(5, postfix="")
come_after = {}
i_line = 0
for i_line, line in enumerate(g):
    if '|' not in line:
        break
    x, y = map(int,line.split('|'))
    come_after.setdefault(x, []).append(y)

prints = [tuple(map(int, line.strip().split(','))) for line in g[i_line+1:]]

def print_is_in_order(nums, come_after):
    num_seen = set()
    for x in nums:
        for x_dep in come_after.get(x, []):
            if x_dep in num_seen:
                return False
        num_seen.add(x)
    return True

total = 0
for pr in prints:
    if print_is_in_order(pr, come_after):
        total += pr[len(pr) // 2]
print('part 1', total)

def topological_order(nums, come_after):
    "Get the topological order of some nodes in a graph."
    all_nums = set(nums)
    seen = set()
    toposort = []
    stack = []
    stack_ptr = []

    def add_node(x):
        seen.add(x)
        stack.append(x)
        stack_ptr.append(0)

    def pop_node():
        stack.pop()
        stack_ptr.pop()

    # run a dfs starting from each node not visited yet
    for x in nums:
        if x in seen:
            continue
        add_node(x)
        
        while len(stack):
            top = stack[-1]
            for ptr in range(stack_ptr[-1], len(come_after.get(top, []))):
                nxt = come_after[top][ptr]
                if nxt not in all_nums:
                    continue
                if nxt not in seen:
                    stack_ptr[-1] = ptr + 1
                    add_node(nxt)
                    break
            else:
                toposort.append(top)
                pop_node()
    toposort.reverse()
    return toposort
                
    
total = 0
for pr in prints:
    if not print_is_in_order(pr, come_after):
        topo = topological_order(pr, come_after)
        total += topo[len(topo) // 2]
print('part 2', total)
