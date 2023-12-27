INPUT_FILE = 'input/2023_1.txt'

with open(INPUT_FILE) as fp:
    txt = fp.readlines()


def part1(txt):
    total = 0
    for line in txt:
        digits = list(filter(lambda x: '0' <=
                      x <= '9', line.strip()))
        total += int(digits[0] + digits[-1])
    print(total)


def part1_2(txt):
    print(sum(
        int(xs[0] + xs[-1])
        for xs in map(
            lambda line: [x for x in line.strip() if '0' <= x <= '9'], txt
        )
    ))


str_digits = ['zero', 'one', 'two', 'three',
              'four', 'five', 'six', 'seven', 'eight', 'nine']
digits = list(map(str, range(0, 10)))


def part2(txt):
    total = 0
    for line in txt:
        line = line.strip()
        first, last = None, None
        first_i, last_i = int(1e9), -1

        for digit_types in (digits, str_digits):
            for i, dig in enumerate(digit_types):
                idx = line.find(dig)
                last_idx = line.rfind(dig)
                if idx >= 0 and idx < first_i:
                    first = i
                    first_i = idx
                if last_idx >= 0 and last_idx > last_i:
                    last = i
                    last_i = last_idx

        total += 10 * first + last
    print(total)


part1(txt)
part1_2(txt)
part2(txt)
