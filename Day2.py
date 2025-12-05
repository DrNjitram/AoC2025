from util import *

def part1_2(data: list[tuple[int, int]]):
    ans1 = 0
    ans2 = 0
    for a,b in data:
        #print(a,b)
        for i in range(a, b+1):
            si = str(i)
            for h in range(len(si)//2, 0, -1):
                if (len(si)/h)%1 == 0.0:
                    subs = si[:h]
                    if (cnt:=si.count(subs)) * len(subs) == len(si):
                        #print(cnt, h, subs, i)
                        if cnt == 2:
                            ans1 += i

                        ans2 += i
                        break


    #print(ans1, ans2)
    return ans1, ans2

kwargs = {"cast": [int, int], "regex": r"(\d+)-(\d+)"}
test(read_day(2, 1, **kwargs), part1_2, (1227775554, 4174379265))
test(read_day(2, **kwargs), part1_2, (44487518055, 53481866137))
