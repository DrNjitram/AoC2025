from functools import cache

import numpy as np

from util import *
map_keys = {"S": 1, "^": 2, "|": 3}

@cache
def step_timeline(active_beam, lower_range) -> int:

    new_beams = []
    x,y = active_beam
    if y == lower_range:
        return 1
    if data[(x, y + 1)] == 0:
        new_beams.append((x, y + 1))
    elif data[(x, y + 1)] == 2:
        new_beams.append((x - 1, y + 1))
        new_beams.append((x + 1, y + 1))

    return sum([step_timeline( beam, lower_range) for beam in new_beams])


def part2(inp):
    global data
    data = inp

    start = [k for k, v in data.items() if v == 1][0]

    lower_range = max([y for x,y in data.keys()])+1
    timelines = step_timeline(start, lower_range)
    step_timeline.cache_clear()
    #print(timelines)
    return timelines

def part1(inp):
    global data
    data = inp
    start = [k for k, v in data.items() if v == 1][0]
    data[start] = 3

    lower_range = max([y for x,y in data.keys()])+1

    active_beams = [start]
    splits = 0
    while active_beams:

        new_beams = []
        for x,y in active_beams:
            if y == lower_range:
                continue
            if data[(x, y+1)] == 0:
                if data[(x, y + 1)] != 3:
                    new_beams.append((x, y+1))
                    data[(x, y+1)] = 3
            elif data[(x, y+1)] == 2:
                splits += 1
                if data[(x - 1, y + 1)] != 3:
                    data[(x - 1, y + 1)] = 3
                    new_beams.append((x - 1, y + 1))

                if data[(x + 1, y + 1)] != 3:
                    data[(x + 1, y + 1)] = 3
                    new_beams.append((x + 1, y + 1))

        active_beams = new_beams

    #print(splits)
    return splits

def hamster(data):

    lines = [list(line.replace('S', '1').replace('.', '0')) for line in data]

    split_count1 = split_count2 = 0
    for y in range(1, len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] != '^':
                if lines[y - 1][x] != '^':
                    lines[y][x] = str(int(lines[y][x]) + int(lines[y - 1][x]))
            else:
                if lines[y - 1][x] != '0':
                    split_count1 += 1
                    lines[y][x - 1] = str(int(lines[y][x - 1]) + int(lines[y - 1][x]))
                    lines[y][x + 1] = str(int(lines[y][x + 1]) + int(lines[y - 1][x]))
        if y == len(lines) - 1:
            for x in range(len(lines[y])):
                split_count2 += int(lines[y][x])

    #print(split_count1, split_count2)
    return split_count1, split_count2

# test(read_day(7, 1, read_as_map=map_keys), part1,  21)
# test(read_day(7, 1, read_as_map=map_keys), part2,  40)
test(read_day(7, read_as_map=map_keys), part1, 1609)
test(read_day(7, read_as_map=map_keys), part2, 12472142047197)
# test(read_day(7, 1), hamster, (21, 40))
test(read_day(7), hamster, (1609, 12472142047197))

bench(read_day(7, read_as_map=map_keys), part2, 12472142047197)
bench(read_day(7), hamster, (1609, 12472142047197))