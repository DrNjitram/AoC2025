from util import *

def reduce_bank(bank: list[int], target=3):

    new_bank = []
    reduced_bank = bank[::]
    while len(new_bank) < target:
        to_add = target - len(new_bank)
        if to_add > 1:
            max_val = max(reduced_bank[:-to_add+1])
        else:
            max_val = max(reduced_bank)
        reduced_bank = reduced_bank[reduced_bank.index(max_val)+1:]
        new_bank.append(max_val)
        #print(new_bank, reduced_bank)
    return new_bank


def part1(data: list[list[int]]):
    ans1 = 0
    ans2 = 0
    for bank in data:
        ans1 += int("".join(str(v) for v in reduce_bank(bank, 2)))
        ans2 += int("".join(str(v) for v in reduce_bank(bank, 12)))


    #print(ans1)
    return ans1, ans2   

kwargs = {"regex": r"(\d)", "cast": int}
test(read_day(3,1, **kwargs), part1, (357, 3121910778619))
test(read_day(3, **kwargs), part1, (17493, 173685428989126))