import numpy as np

from util import *


def manhattan_distance(p1, p2):
    return sum([abs(a-b) for a,b in zip(p1, p2)])

def distance(p1, p2):
    return sum([np.power(a-b, 2) for a,b in zip(p1, p2)])

def part1(data: list[tuple[int, int, int]], connections=10):
    data = [tuple(p) for p in data]
    distances = {}
    for p1 in data:
        for p2 in data:
            if p1 != p2 and (p1,p2) not in distances and (p2, p1) not in distances:
                distances[(p1,p2)] = distance(p1, p2)

    ds = [(p1, p2, d) for (p1, p2), d in distances.items()]
    ds.sort(key=lambda x: x[2])

    graph = defaultdict(list)
    graph_inv = {}

    for i,p in enumerate(data):
        graph[i].append(p)
        graph_inv[p] = i

    ans1 = p1 = p2 = new_id = 0
    for i,(p1, p2, _) in enumerate(ds):
        if graph_inv[p1] != graph_inv[p2]:
            new_id = graph_inv[p1]
            old_id =  graph_inv[p2]
            for p in graph[old_id]:
                graph_inv[p] = new_id
            graph[new_id] += graph[old_id]
            graph[old_id] = []

        if i == connections-1:
            sizes = [len(n) for n in graph.values()]
            sizes.sort(reverse=True)
            ans1 = sizes[0] * sizes[1] * sizes[2]
        if len(graph[new_id]) == len(data):
            break


    print(ans1, p1[0]*p2[0])
    return ans1, p1[0]*p2[0]


test(read_day(8, 1, delim=",", cast=int, split=True), part1, (40, 25272))
test(read_day(8, delim=",", cast=int, split=True), part1, (175500, 6934702555), connections=1000)