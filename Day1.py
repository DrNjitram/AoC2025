from util import *

def part1_2(data: list[str]):
    ans1 = 0
    ans2 = 0
    dial = 50
    for d,v in data:
        for i in range(v):
            dial += 1 if d=="R" else -1
            if dial == -1:
                dial = 99
            elif dial == 100:
                dial = 0
            if dial == 0:
                ans2 += 1
        if dial == 0:
            ans1 += 1

    return ans1, ans2


kwargs = {"cast": [str, int], "regex": r"([L|R])(\d+)"}
test(read_day(1, 1, **kwargs), part1_2, (3, 6))
test(read_day(1, **kwargs), part1_2, (1105, 6599))
#part1_2(read_day(1, **kwargs))
