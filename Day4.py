from util import *

def part1(data: dict[tuple[int, int], int]):
    ans1 = 0
    new_map = defaultdict(int)
    for x,y in list(data.keys()):
        if data[x,y]:
            adj = 0
            for dx, dy in adj8:
                if data[(x+dx, y+dy)]:
                    adj += 1
            if adj < 4:
                ans1 += 1
            else:
                new_map[(x,y)] = 1

    ans2 = ans1
    can_change = True
    while can_change:
        can_change = False
        next_map = defaultdict(int)
        for x, y in list(new_map.keys()):
            if new_map[x, y]:
                adj = 0
                for dx, dy in adj8:
                    if new_map[(x + dx, y + dy)]:
                        adj += 1
                if adj < 4:
                    ans2 += 1
                    can_change = True
                else:
                    next_map[(x, y)] = 1
        new_map = next_map

    return ans1, ans2

kwargs = {"read_as_map": {"@": 1, "X": 2}}
test(read_day(4, 1, **kwargs), part1, (13, 43))
test(read_day(4, **kwargs), part1, (1320, 8354))