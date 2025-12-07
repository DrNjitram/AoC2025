from functools import reduce
from operator import mul, add
from util import *


def part1_2(data: list[str]):
    ans1 = 0
    ans2 = 0

    max_len = max([len(line) for line in data])-2
    s = data[-1]

    cur = 0
    while s:
        fn = s[0]
        s = s[1:]
        if s:
           l = min(s.find("*") if "*" in s else 1E10, s.find("+") if "+" in s else 1E10)
        else:
            l = max_len

        nums: list[str] = []
        for line in data[:-1]:
            nums.append(line[cur:cur+l])

        if l == max_len:
            max_s = max([len(n) for n in nums])
            nums = [n.ljust(max_s) for n in nums]

        cur_nums = [int(s) for s in nums]
        ans1 += reduce(mul if fn == "*" else add, cur_nums)
        cur_nums = [int("".join([nums[j][i] for j in range(len(nums))])) for i in range(len(nums[0]))]
        ans2 += reduce(mul if fn == "*" else add, cur_nums)
        s = s[l:]
        cur += l+1

    print(ans1, ans2)
    return ans1, ans2


test(read_day(6, 1, strip=False), part1_2, (4277556, 3263827))
test(read_day(6, 0, strip=False), part1_2, (6209956042374, 12608160008022))