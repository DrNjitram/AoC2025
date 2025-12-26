from functools import reduce
from operator import mul

from util import *

def part1(data: list[str]):
    gifts = [(5, 9),
             (6, 9),
             (7, 9),
             (7, 9),
             (7, 9),
             (7, 9)]
    works = 0
    for d in data:
        if "x" not in d:
            continue
        a,b = d.split(": ")
        s = reduce(mul, [int(v) for v in a.split("x")])
        g = [int(v) for v in b.split(" ")]
        lower = 0
        upper = 0
        for i in range(len(gifts)):
            lower += g[i] * gifts[i][0]
            upper += g[i] * gifts[i][1]

        if s >= upper:
            works += 1
        elif lower < s< upper:
            raise Exception("Real work time")

    print(works)
    return works

test(read_day(12), part1, 528)