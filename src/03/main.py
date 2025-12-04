import aiofiles
from collections import defaultdict as dd

from src.utils.decs import timeit


PartType = list[list[int]]


async def main(fn: str = "in.txt", stage: int = 1, debug: bool = False):
    async with aiofiles.open(fn, mode='r') as f:
        f = await f.readlines()

    print("03: {} -> {} lines".format(fn, len(f)))

    # Pre-process input based on challenge
    f = [
        [int(c) for c in l.strip()]
        for l in f
    ]

    if stage == 1 or stage < 1:
        print(f"Part 1: {await p1(f, debug=debug)}")

    if stage == 2 or stage < 1:
        print(f"Part 2: {await p2(f, debug=debug)}")


@timeit
async def p1(f: PartType, debug: bool = False) -> int:
    t = 0

    for l in f:
        fr = dd(lambda: [])

        if debug:
            print(l)

        for ix, n in enumerate(l):
            fr[n].append(ix)

        if debug:
            print(f"fr = {dict(fr)}")

        # NOTE: It can only go from 99 to 11, so we just brute force it

        for i in range(9, 0, -1):
            if len(fr[i]) == 0:
                continue

            curr = str(i)
            found_j = False

            for j in range(9, 0, -1):
                if len(fr[j]) == 0:
                    continue

                for pos_i in fr[i]:
                    if found_j:
                        break

                    for pos_j in fr[j]:
                        if pos_j > pos_i:
                            if debug:
                                print(f"Found i:{i} at {pos_i} and j:{j} at {pos_j} -> {i}{j}")

                            curr += str(j)
                            found_j = True

                            break

                if found_j:
                    break

            if not found_j:
                continue

            t += int(curr)
            # print(curr)

            if debug:
                print(f"Adding {curr}, total now {t}")

            break

        if debug:
            print("---")

    return t


@timeit
async def p2(f: PartType, debug: bool = False) -> int:
    t = 0
    n = 12

    if debug:
        print(f"\n======\nTarget length: {n}")

    for li, l in enumerate(f):
        if debug:
            print(l)

        curr = ""
        s = 0

        for i in range(n):
            needed = n - i - 1
            search = len(l) - needed

            if debug:
                print(f"[{i}] curr: {curr}, s: {s}, need: {needed}, search: {search}")

            digits = [
                (l[pos], pos)
                for pos in range(s, search)
            ]

            max_digit, max_pos = max(digits, key=lambda x: x[0])

            if debug:
                print(f"[{i}] got {max_digit} at {max_pos} (search up to {search}) from {digits}")

            curr += str(max_digit)

            s = max_pos + 1

        # print(curr)

        if debug:
            print(f"Final cur at {li}: {curr}")
            print("---")

        assert len(curr) == n, f"Error: curr length {len(curr)} != {n} ({curr})"
        t += int(curr)

    return t
