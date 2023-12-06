# fmt: off
# isort: skip_file
# ruff: noqa
import math, pathlib

def ints(s):         return [int(x) for x in s.split()[1:]]
def join(l):         return ''.join(map(str, l))
def is_win(c, t, d): return c * (t - c) > d
def n_wins(t, d):    return sum(is_win(c, t, d) for c in range(1, t))

data = (pathlib.Path(__file__).parent.parent/'inputs'/'input_06').read_text().splitlines()
print(math.prod(n_wins(t, d) for t, d in zip(ints(data[0]), ints(data[1]))))
print(n_wins(int(join(ints(data[0]))),  int(join(ints(data[1])))))
