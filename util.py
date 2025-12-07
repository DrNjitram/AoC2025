import re
import time
from collections import defaultdict
from multiprocessing import Pool
from typing import List, Callable, Any, Tuple, Iterable
from tqdm import tqdm

direction_dict = {
    -1j: "^",
    1j: "v",
    1: ">",
    -1: "<"
}

inv_direction_dict = {
    "^": -1j,
    "v": 1j,
    ">":1,
    "<": -1
}

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

adj4 = [
    [-1, 0],
    [1, 0],
    [0, 1],
    [0, -1]
]
adj8 = [
    [-1, 0],
    [1, 0],
    [0, 1],
    [0, -1],
    [-1, -1],
    [1, 1],
    [-1, 1],
    [1, -1]
]


def cast_ray(internal_data: dict[complex, int], p: tuple[complex, complex]) -> int | None:
    p_pos, p_dir = p
    coords = [k for k,v in internal_data.items() if v == 1 and k.imag == p_pos.imag or k.real == p_pos.real]
    deltas = []

    if not coords:
        return None

    for coord in coords:
        delta = (coord-p_pos)/p_dir
        if delta.imag == 0 and delta.real >0:
            deltas.append(int(delta.real))

    if len(deltas) > 0:
        return min(deltas)

    return None


def read_day(day: int, test_part=0, **kwargs) -> list | dict:
    return read_lines(rf"Inputs\Day{day}" + (f"_Test{test_part}" if test_part else ""), **kwargs)


def read_lines(filename: str, split=False, cast=None, delim=None, regex=None, read_as_map=None, strip=True) -> list | dict:
    if not filename.startswith("Inputs"):
        filename = "Inputs/" + filename
    if strip:
        lines = [line.strip() for line in open(filename).read().strip().split("\n")]
    else:
        lines = [line for line in open(filename).read().split("\n")]

    if read_as_map:
        data = defaultdict(int)
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                c = lines[y][x]
                if c in read_as_map:
                    data[(x,y)] = read_as_map[c]
        return data

    if split and cast and type(cast) not in [list, tuple]:
        lines = [[cast(i) for i in line.split(sep=delim)] for line in lines]
    elif split:
        lines = [line.split(sep=delim) for line in lines]
    elif regex:
        if cast and type(cast) not in [list, tuple]:
            lines = [[cast(i) for i in re.findall(regex, line)] for line in lines]
        else:
            lines = [re.findall(regex, line) for line in lines]
    elif cast and type(cast) not in [list, tuple]:
        lines = [cast(line) for line in lines]
    if type(lines[0]) in [list, tuple] and len(lines[0]) == 1:
        lines = [line[0] for line in lines]
    if len(lines) == 1:
        lines = lines[0]
    if type(cast) in [list, tuple]:
        lines = [[cast[i](v) for i,v in enumerate(line)] for line in lines]

    return lines

def print_map(data: list[str|list[int]]):
    for line in data:
        if type(line) == str:
            print(line)
        else:
            print("".join([str(v) for v in line]))
    print("")

def print_sparse_map(data: dict[Any, Any], keys=None, unique=None, background = ".") -> None:
    complex_map = False
    if [type(k) for k in data.keys()][0] == complex:
        complex_map = True
        x_s, y_s = zip(*[(int(p.real), int(p.imag)) for p in data.keys()])
    else:
        x_s, y_s = zip(*[p for p in data.keys()])
    if keys is not None:
        print_keys = {v: k for k, v in keys.items()}
    else:
        print_keys = {v: v for k, v in data.items()}
    pos_p = None

    if unique is not None:
        p, icon = unique
        if type(p) == complex:
            pos_p = p
            pos_d = None
        else:
            pos_p, pos_d = p
    for y in range(min(y_s), max(y_s) + 1):
        line = ""
        for x in range(min(x_s), max(x_s) + 1):
            if complex_map:
                pos = complex(x,y)
            else:
                pos = (x,y)
            if unique is not None and pos == pos_p:
                if pos_d is not None:
                    line += direction_dict[pos_d]
                else:
                    line += icon
            else:
                line += print_keys.get(data[pos], background)
        print(line)
    print("")

def inbounds_c(data: list|dict, p: complex) -> bool:
    return inbounds(data, int(p.real), int(p.imag))

def inbounds(data: list|dict, x:int, y:int) -> bool:
    if type(data) in [dict, defaultdict]:
        x_s, y_s = zip(*[(int(p.real), int(p.imag)) for p,v in data.items() if v == 1])
        return min(x_s) <= x <= max(x_s) and min(y_s) <= y <= max(y_s)
    else:
        return 0 <= x < len(data[0]) and 0 <= y < len(data)

def flatten_linearly_nested(lst):
    a, b = lst
    if type(b) == int:
        return [a, b]
    flat_list = [a]
    while True:
        if len(b) == 1:
            flat_list += b
            break
        else:
            a, b = b
            flat_list.append(a)
        if type(b) == int:
            flat_list += [b]
            break
    return flat_list

def test(data, fn: Callable, result: Any, **kwargs):
    start_time = time.perf_counter_ns()

    try:
        t = fn(data, **kwargs)
        if t == result:
            print(f"{Colors.OKCYAN}SUCCESS Time: {(time.perf_counter_ns() - start_time)/1E6:.2f}ms{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}FAILURE Time: {(time.perf_counter_ns() - start_time) / 1E6:.2f}ms{Colors.ENDC}")
    except Exception as e:
        raise e


def bench(data, fn: Callable, result: Any, iters=1000, **kwargs):
    total_time = 0
    i = 0
    try:
        while i < iters:
            start_time = time.perf_counter_ns()

            t = fn(data, **kwargs)
            total_time += time.perf_counter_ns() - start_time
            if t != result:
                print(f"{Colors.FAIL}FAILURE")
            i += 1


        print(f"{Colors.OKCYAN}SUCCESS\nTotal Time: {total_time/1E6:.2f}ms\nIters {i}\nTime per Iter: {total_time/1E6/iters:.2f}ms{Colors.ENDC}")

    except Exception as e:
        raise e

def sparse_map(data: list[str], keys: dict, background = ".", unique=None, direction = None) -> tuple[defaultdict[Any, complex], None | complex | list[complex | Any]]:
    result = defaultdict(complex)
    unique_position = None
    for y in range(len(data)):
        for x in range(len(data[y])):
            c = data[y][x]
            if c == unique:
                if direction is None:
                    unique_position = complex(x, y)
                else:
                    unique_position = [complex(x, y), direction]
            elif c != background:
                result[complex(x, y)] = keys[c]
    return result, unique_position

def run_multiprocessing(fn: Callable, args: Iterable) -> list:
    with Pool() as pool:
        results = list(
            tqdm(
                pool.imap_unordered(
                    fn,
                    args
                ),
                total=len(args)))
    return results

global_master_list = []
def flatten_list(lst):
    flatten_list_v2(lst)
    return global_master_list

def flatten_list_v2(lst: list | Any):
    global global_master_list
    if type(lst) == list:
        if len(lst) == 1:
            return flatten_list_v2(lst[0])
        else:
            return [flatten_list_v2(l) for l in lst]
    else:
        global_master_list.append(lst)
    return None


