from util import *

def part1(data: list[str]):
    fresh_ranges = []
    ans1 = 0
    ans2 = 0
    for line in data:
        if "-" in line:
            a,b = line.split("-")
            fresh_ranges.append((int(a), int(b)))
        elif line == "":
            changed = True
            while changed:
                changed = False
                c_ranges = [fresh_ranges[0]]

                for a, b in fresh_ranges[1:]:
                    appended = False
                    for i, (x, y) in enumerate(c_ranges):
                        n_range = None
                        if x >= a and y <= b:
                            n_range = a, b
                        elif x <= a and y >= b:
                            n_range = x, y
                        elif x <= b + 1 and y > b:
                            n_range = a, y
                        elif y >= a - 1 and a > x:
                            n_range = x, b

                        if n_range:
                            c_ranges[i] = n_range
                            appended = True
                            changed = True
                            break
                    if not appended:
                        c_ranges.append((a, b))

                fresh_ranges = c_ranges

        elif line != "":
            ing = int(line)
            for a,b in fresh_ranges:
                if a<= ing <= b:
                    ans1 += 1
                    break




    for a,b in fresh_ranges:
        ans2 += b - a + 1

    print(ans1, ans2)
    return ans1, ans2


# 297536195236428 low
test(read_day(5, 1), part1, (3, 14))
test(read_day(5), part1, (737, 357485433193284))