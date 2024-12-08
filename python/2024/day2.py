from collections import Counter
from aoc_utils.load_input import read_input_lines

lines = read_input_lines(2)
reports = [tuple(map(int, r.split())) for r in lines]

def is_report_safe(report):
    diffs = [(report[i + 1] - report[i]) for i in range(len(report) - 1)]
    is_asc = min(diffs) > 0
    is_desc = max(diffs) < 0
    diff_max_3 = max(abs(x) for x in diffs) <= 3
    return (is_asc or is_desc) and diff_max_3

total_safe = sum(is_report_safe(report) for report in reports)
print('part 1', total_safe)

total_almost_safe = 0
for report in reports:
    for i in range(len(report)):
        if is_report_safe(report[:i] + report[i+1:]):
            total_almost_safe += 1
            break
print('part 2', total_almost_safe)
