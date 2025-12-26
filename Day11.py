from functools import reduce
from operator import mul

from util import *
import networkx as nx
import matplotlib.pyplot as plt

def part1(data: list[str]):
    G = nx.DiGraph()
    for d in data:
        inp, outp = d.split(": ")
        outp = outp.split(" ")
        for o in outp:
            G.add_edge(inp, o)


    ans1= len(list(nx.all_simple_paths(G, 'you', 'out')))
    print(ans1)

    return ans1

def part2(data: list[str]):
    connections = defaultdict(list)
    G = nx.DiGraph()
    for d in data:
        inp, outp = d.split(": ")
        outp = outp.split(" ")
        for o in outp:
            G.add_edge(inp, o)
            connections[inp] += [o]


    depth = 0
    visited = {"svr": 0}
    to_check = connections["svr"]
    while to_check:
        check_next = set()
        depth += 1
        for n in to_check:
            visited[n] = depth
            check_next |= set(connections[n])
        to_check = check_next

    

    if False:
        top = {"svr", "fft", "dac", "out", "jlg", "laq", "qgn", "ifs", "ppm", "brg", "fbt", "sgu", "yql", "sta", "jmk", "txi", "knq", "xee", "igu", "xhk", "bsb", "lur", "fpb", "fnr", "ozd", "vrt", "you", "mwu"}
        labels = defaultdict(str)
        for n in top:
            labels[n] = n

        indices = []
        for i in range(max(visited.values())):
            indices.append([k for k,v in visited.items() if v == i])

        positions = {}
        for i, nodes in enumerate(indices):
            for j, n in enumerate(nodes):
                positions[n] = (i*4, j-len(nodes)//2)


        positions["out"] = (max(visited.values())*4+1, 0)
        plt.figure(dpi=400)
        nx.draw(G, pos=positions, labels=labels, node_size=40, with_labels=True, font_size=4, linewidths=0.1)
        plt.show()

    pairs = [
        (["svr"], ["laq", "laq", "qgn", "ifs", "ppm"]),
        (["laq", "qgn", "ifs", "ppm"], ["fft"]),
        (["fft"], ("brg", "fbt", "sgu", "yql")),
        (("brg", "fbt", "sgu", "yql"), ("sta", "jmk", "txi", "knq", "xee")),
        (("sta", "jmk", "txi", "knq", "xee"), ("igu", "xhk", "bsb", "lur", "fpb")),
        (("igu", "xhk", "bsb", "lur", "fpb"), ["dac"]),
        (["dac"], ("fnr", "ozd", "vrt", "you", "mwu")),
        (("fnr", "ozd", "vrt", "you", "mwu"), ["out"])
    ]
    G2 = nx.DiGraph()


    paths = {('svr', 'jlg'): 293, ('svr', 'laq'): 342, ('svr', 'qgn'): 186, ('svr', 'ifs'): 181, ('svr', 'ppm'): 187, ('jlg', 'fft'): 0, ('laq', 'fft'): 3, ('qgn', 'fft'): 4, ('ifs', 'fft'): 1, ('ppm', 'fft'): 3, ('fft', 'brg'): 5, ('fft', 'fbt'): 4, ('fft', 'sgu'): 5, ('fft', 'yql'): 3, ('brg', 'sta'): 75, ('brg', 'jmk'): 109, ('brg', 'txi'): 63, ('brg', 'knq'): 51, ('brg', 'xee'): 94, ('fbt', 'sta'): 111, ('fbt', 'jmk'): 181, ('fbt', 'txi'): 106, ('fbt', 'knq'): 116, ('fbt', 'xee'): 180, ('sgu', 'sta'): 122, ('sgu', 'jmk'): 195, ('sgu', 'txi'): 124, ('sgu', 'knq'): 164, ('sgu', 'xee'): 219, ('yql', 'sta'): 31, ('yql', 'jmk'): 65, ('yql', 'txi'): 42, ('yql', 'knq'): 64, ('yql', 'xee'): 77, ('sta', 'igu'): 145, ('sta', 'xhk'): 148, ('sta', 'bsb'): 157, ('sta', 'lur'): 95, ('sta', 'fpb'): 143, ('jmk', 'igu'): 151, ('jmk', 'xhk'): 154, ('jmk', 'bsb'): 166, ('jmk', 'lur'): 101, ('jmk', 'fpb'): 152, ('txi', 'igu'): 40, ('txi', 'xhk'): 50, ('txi', 'bsb'): 47, ('txi', 'lur'): 43, ('txi', 'fpb'): 22, ('knq', 'igu'): 56, ('knq', 'xhk'): 60, ('knq', 'bsb'): 62, ('knq', 'lur'): 46, ('knq', 'fpb'): 51, ('xee', 'igu'): 53, ('xee', 'xhk'): 53, ('xee', 'bsb'): 55, ('xee', 'lur'): 32, ('xee', 'fpb'): 46, ('igu', 'dac'): 2, ('xhk', 'dac'): 2, ('bsb', 'dac'): 2, ('lur', 'dac'): 3, ('fpb', 'dac'): 2, ('dac', 'fnr'): 3, ('dac', 'ozd'): 1, ('dac', 'vrt'): 3, ('dac', 'you'): 3, ('dac', 'mwu'): 2, ('fnr', 'out'): 1480, ('ozd', 'out'): 2068, ('vrt', 'out'): 1786, ('you', 'out'): 585, ('mwu', 'out'): 919}

    for a,b in pairs:
        for aa in a:
            for bb in b:
                #print(aa, bb)
                G2.add_edge(aa, bb)
                if (aa, bb) not in paths:
                    paths[(aa, bb)] = len(list(nx.all_simple_paths(G, aa, bb, cutoff=12)))



    ans2 = 1
    for a,b in [("svr", "fft"), ("fft", "dac"), ("dac", "out")]:
        cul1 = 0

        for p in nx.all_simple_paths(G2, a, b):
            cul = 1
            for i in range(len(p)-1):
                a = p[i]
                b = p[i+1]
                cul *= paths[(a,b)]
            cul1 += cul
        ans2 *= cul1

    print(ans2)
    return ans2

test(read_day(11, 1), part1, 5)
test(read_day(11), part1, 585)
# test(read_day(11, 2), part2, 2)
test(read_day(11), part2, 349322478796032)