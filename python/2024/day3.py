from aoc_utils.load_input import read_input_lines
import re

lines = read_input_lines(3)
pattern = re.compile(r"mul\((\d+),(\d+)\)")

total = 0
for line in lines:
    for m in pattern.findall(line):
        x1, x2 = map(int, m)
        print(x1, x2)
        total += x1 * x2
print('part1', total)

pattern = re.compile(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))")
enabled = True
total = 0
for line in lines:
    for m in pattern.findall(line):
        x1, x2, do, dont = m
        if do:
            enabled = True
        elif dont:
            enabled = False
        else:
            if enabled:
                total += int(x1) * int(x2)
print('part2', total)
