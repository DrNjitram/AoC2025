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

def valid_edge(edge1, edge2):
    t, u = line_intersect(*edge1, *edge2)
    if 0 <= t<= 1 and 0 <= u <= 1:
        return True
    return False

    # if x1 == x2 and ((y1 < y and y2 < y) or (y1 > y and y2 > y)):
    #     return False
    # elif y1 == y2 and ((x1 <= x and x2 <= x) or (x1 > x and x2 > x)):
    #     return False
    # else:
    #     return True

def check_inside(t: tuple[int, int], edges: list[tuple]):
    edge_count = 0
    now_on_edge = False
    x_end, y_end = t

    if True or x_end < y_end: #and max_x-x_end < max_y-y_end:
        filtered_edges = [e for e in edges if valid_edge(e, ((0, y_end), t))]
        return len(filtered_edges)%2==1
        # p0 = 0, y_end
        # p1 = x_end, y_end



        if x_end < max_x/2:
            l = range(x_end+1)
        else:
            l = range(x_end+1) #= range(max_x+1, x_end-1, -1)
        for x in l:
            for edge in filtered_edges:
                if on_edge(x, y_end, *edge):
                    if not now_on_edge:
                        now_on_edge = True
                        edge_count += 1
                    break
            else:
                if now_on_edge:
                    now_on_edge = False
    # else:
    #     if y_end < max_y/2:
    #         l = range(y_end+1)
    #     else:
    #         l = range(y_end+1)#range(max_y+1, y_end-1, -1)
    #     for y in l:
    #         for edge in edges:
    #             if on_edge(x_end, y, *edge):
    #                 if not now_on_edge:
    #                     now_on_edge = True
    #                     edge_count += 1
    #                 break
    #         else:
    #             if now_on_edge:
    #                 now_on_edge = False


    return edge_count%2==1

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

    all_x, all_y = [list(set(coords)) for coords in zip(*data)]
    all_x.sort()
    all_y.sort()


    max_x = len(all_x * 2)
    max_y = len(all_y * 2)

    rescaled_data = {(x,y): ((all_x.index(x)+1)*2,(all_y.index(y))+1*2) for x,y in data}
    temp_scale = [((all_x.index(x)+1)*2,(all_y.index(y))+1*2) for x,y in data]
    rescaled_edges = [(temp_scale[i], temp_scale[i - 1]) for i in range(len(data))]

    answer2 = 0

    for i in range(len(ds)):
        p1, p2, s = ds[i]
        print(p1, p2, s)
        x1, y1 = rescaled_data[p1]
        x2, y2 = rescaled_data[p2]
        p3 = (x1, y2)
        p4 = (x2, y1)
        #print("\t", x1, y2, check_inside((x1, y2), edges))
        #print("\t", x2, y1, check_inside((x2, y1), edges))
        if check_inside((x1, y2), rescaled_edges) and check_inside((x2, y1), rescaled_edges):
            check_edges = [(p1, p3), (p1, p4), (p2, p3), (p2, p4)]
            inside = True
            for (xa, ya), (xb, yb) in check_edges:
                if ya == yb:
                    for dx in range(xa, xb+1, 1 if xa<xb else -1):
                        if not check_inside((dx, ya), rescaled_edges):
                            inside = False
                            break
                else:
                    for dy in range(ya, yb+1, 1 if ya<yb else -1):
                        if not check_inside((xa, dy), rescaled_edges):
                            inside = False
                            break
                if not inside:
                    break
            if inside:
                print("\t", p1, p2, s)
                answer2 = s
                break

    print(ds[0][2], answer2)
    return ds[0][2], answer2

test(read_day(9, 1, delim=",", cast=int, split=True), part1, (50, 24))
#test(read_day(9, delim=",", cast=int, split=True), part1, 50)