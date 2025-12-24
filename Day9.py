from util import *

def size(t1: tuple[int, int], t2: tuple[int, int]):
    return abs(t1[0]-t2[0]+1)*abs(t1[1]-t2[1]+1)

def on_edge(x, y, e1, e2):
    x1, y1 = e1
    x2, y2 = e2
    if x1 == x2 == x:
        if y1 < y2:
            return y1 <= y <= y2
        else:
            return y1 >= y >= y2
    if y1 == y2 == y:
        if x1 < x2:
            return x1 <= x <= x2
        else:
            return x1 >= x >= x2
    return False


def check_inside(t: tuple[int, int], edges: list[tuple]):
    edge_count = 0
    now_on_edge = False
    x_end, y = t
    for x in range(x_end+1):
        for edge in edges:
            if on_edge(x, y, *edge):
                if not now_on_edge:
                    now_on_edge = True
                    edge_count += 1
                break
        else:
            if now_on_edge:
                now_on_edge = False

    return edge_count%2==1

def part1(data: list[list[int]]):
    data = [tuple(p) for p in data]
    edges = [(data[i], data[i-1]) for i in range(len(data))]

    sizes1 = {}



    for i in range(len(data)):
        for j in range(i+1, len(data)):

            p1 = x1, y1 = data[i]
            p2 = x2, y2 = data[j]
            p3 = (x1, y2)
            p4 = (x2, y1)
            s = size(p1, p2)
            sizes1[(p1, p2)] = s
            #print(data[i], data[j], s)

    ds = [(p1, p2, d) for (p1, p2), d in sizes1.items()]
    ds.sort(key=lambda x: x[2], reverse=True)

    answer2= 0
    for p1, p2, s in ds:
        print(p1, p2, s)
        x1, y1 = p1
        x2, y2 = p2
        p3 = (x1, y2)
        p4 = (x2, y1)
        #print("\t", x1, y2, check_inside((x1, y2), edges))
        #print("\t", x2, y1, check_inside((x2, y1), edges))
        if check_inside((x1, y2), edges) and check_inside((x2, y1), edges):
            check_edges = [(p1, p3), (p1, p4), (p2, p3), (p2, p4)]
            inside = True
            for (xa, ya), (xb, yb) in check_edges:
                if ya == yb:
                    for dx in range(xa, xb+1, 1 if xa<xb else -1):
                        if not check_inside((dx, ya), edges):
                            inside = False
                            break
                else:
                    for dy in range(ya, yb+1, 1 if ya<yb else -1):
                        if not check_inside((xa, dy), edges):
                            inside = False
                            break
                if not inside:
                    break
            if inside:
                answer2 = s
                break




    print(ds[0][2], answer2)
    return ds[0][2], answer2

test(read_day(9, 1, delim=",", cast=int, split=True), part1, (50, 24))
test(read_day(9, delim=",", cast=int, split=True), part1, 50)