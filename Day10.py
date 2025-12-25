import pulp
from util import *

def part1(data: list[str]):
    ans1 = []
    ans2 = []
    for s in data:
        target = []
        buttons = []
        joltage = []
        for t in s.split(" "):
            if t.startswith("["):
                target = ["0" if c == "." else "1" for c in t[1:-1]]
            elif t.startswith("("):
                buttons.append(["1" if str(i) in t else "0" for i in range(len(target))])
            else:
                joltage = [int(v) for v in t[1:-1].split(",")]

        array_buttons = np.array([[int(l) for l in b] for b in buttons]).T

        prob = pulp.LpProblem("Pressing_buttons", pulp.LpMinimize)
        b = pulp.LpVariable.dicts('b', range(len(buttons)), 0, None, pulp.LpInteger)
        pulp_joltage = list(b.values()) * array_buttons

        prob += pulp.lpSum(list(b.values()))
        for i in range(len(joltage)):
            prob += joltage[i]==pulp.lpSum(pulp_joltage[i])

        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        presses = [int(v.varValue) for v in prob.variables()]
        ans2.append(sum(presses))

        buttons = [int("".join(b), 2) for b in buttons]
        target = int("".join(target), 2)

        successes = []
        for i in range(2**len(buttons)):
            state = 0
            for j, b in enumerate(buttons):
                if (1 << j) & i:
                    state ^= b
            if state == target:
                successes.append(i.bit_count())

        ans1.append(min(successes))

    print(sum(ans1))
    print(sum(ans2))

    return sum(ans1), sum(ans2)



test(read_day(10, 1), part1, (7, 33))
test(read_day(10), part1, (428, 16613))