import aiofiles
from pydantic import BaseModel

from collections import defaultdict

from src.utils.decs import timeit


class PartType(BaseModel):
    ranges: list[tuple[int, int]]

    min_r: int
    max_r: int

    i: list[int]



async def main(fn: str = "in.txt", stage: int = 1, debug: bool = False):
    async with aiofiles.open(fn, mode='r') as f:
        ff = await f.readlines()

    print("05: {} -> {} lines".format(fn, len(ff)))

    # Pre-process input based on challenge
    f = PartType(
        ranges=[],
        min_r=1<<31,
        max_r=0,
        i=[]
    )

    ranges_done = False

    for line in ff:
        line = line.strip()

        if line == "":
            ranges_done = True

            if debug:
                print("Finished loading ranges")

            continue

        if ranges_done:
            f.i.append(int(line))

        else:
            l, r = line.split("-")

            a = int(l)
            b = int(r)

            f.ranges.append((a, b))

            if a < f.min_r:
                f.min_r = a

            if b > f.max_r:
                f.max_r = b

    # Sort ranges asc by first value
    f.ranges.sort(key=lambda x: x[0])

    if debug:
        print(f"Loaded ranges: {len(f.ranges)} and {len(f.i)} items")

    if stage == 1 or stage < 1:
        print(f"Part 1:\n{await p1(f, debug=debug)}")

    if stage == 2 or stage < 1:
        print(f"Part 2:\n{await p2(f, debug=debug)}")


@timeit
async def p1(f: PartType, debug: bool = False) -> int:
    t = 0

    for i in f.i:
        found = False

        for r in f.ranges:
            if r[0] <= i <= r[1]:
                found = True

                if debug:
                    print(f"Item {i} found in range {r}")

                break

        if found:
            t += 1

            if debug:
                print(f"Item {i} not found in any range, adding to total")

    return t


@timeit
async def p2(f: PartType, debug: bool = False) -> int:
    (x, y) = f.ranges[0]

    final: list[tuple[int, int]] = []

    for a, b in f.ranges[1:]:
        if debug:
            print(f"a, b = {a}, {b}")
            print(f"x, y = {x}, {y}")

        if a > y:
            final.append((x, y))
            x, y = a, b

        else:
            y = max(y, b)

        if debug:
            print(f"final = {final}\n")

    final.append((x, y))

    if debug:
        print(f"final = {final}\n")

    return sum(
        (b - a) + 1
        for a, b in final
    )
