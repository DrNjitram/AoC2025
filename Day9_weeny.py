import math

import shapely
from shapely.plotting import plot_polygon

from util import *
from shapely import Polygon
import matplotlib.pyplot as plt

def size(t1: tuple[int, int], t2: tuple[int, int]):
    return (abs(t1[0]-t2[0])+1)*(abs(t1[1]-t2[1])+1)


def part1(data: list[list[int]]):
    data = [tuple(p) for p in data]

    sizes1 = {}

    for i in range(len(data)):
        for j in range(i+1, len(data)):
            p1 = data[i]
            p2 = data[j]
            s = size(p1, p2)
            sizes1[(p1, p2)] = s


    ds = [(p1, p2, d) for (p1, p2), d in sizes1.items()]
    ds.sort(key=lambda x: x[2], reverse=True)

    answer2 = 0

    tiles = Polygon(data)
    tiles2 = tiles.buffer(0.6)

    for p1, p2, s in ds:
        print(p1, p2, s)
        x1, y1 = p1
        x2, y2 = p2
        p3 = (x1, y2)
        p4 = (x2, y1)
        #plt.figure()
        #ax = plt.subplot(111)
        #plot_polygon(tiles2, ax=ax)
        #plot_polygon(tiles, ax=ax, color="black")
        square = Polygon([p1, p3, p2, p4])
        #plot_polygon(square, color="red", ax=ax)
        d = shapely.difference(square, tiles2)
        # plt.title(f"{p1}, {p2}, {s}, {d.area}")
        # plt.show()
        if d.area == 0.0:
            answer2 = s

            break

    # 1473518601 too low
    print(ds[0][2], answer2)
    return ds[0][2], answer2

test(read_day(9, 1, delim=",", cast=int, split=True), part1, (50, 24))
test(read_day(9, 2, delim=",", cast=int, split=True), part1, (70, 54))
test(read_day(9, delim=",", cast=int, split=True), part1, 50)