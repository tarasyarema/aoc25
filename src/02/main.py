from typing import List, Literal
from json import dumps
from functools import cache
from collections import defaultdict

import aiofiles


async def main(fn: str = "in.txt", stage: int = 1):
    async with aiofiles.open(fn, mode='r') as f:
        f = await f.readlines()

    f = [
        [x for x in s.split('-')]
        for s in f[0].strip().split(',')
    ]

    print(f"debug: {len(f)} pairs found\n")

    # print(invalid_compute(1188511880, 1188511890))
    # print(invalid_compute(95, 115))
    # print(invalid_compute(11, 33))
    # print(invalid_compute(446443, 446449))

    # print(check_invalid_2(123123))
    # print(check_invalid_2(1))
    # print(check_invalid_2(11))
    # print(check_invalid_2(1111111111))
    # print(check_invalid_2(1212121212))
    # print(check_invalid_2(12121212121))

    # Edge case ffs
    for n in [
        # 107,
        # 1111111,
        # 112112,
        # 446446,
        1188511885,
        # 2121212124,
        # 111,
        # 824824824,
        # Edges
        # 565655,
        # 2121212122,
        # 212121,
        # 212122,
        # 22122212,
        # 1885518855,
    ]:
        if stage in [0, 1, 2]:
            continue

        print(n, "->>", check_invalid_2(n, debug=True), "\n---\n")

    # in.txt
    # 4174379265

    if stage == 1 or stage < 1:
        print(f"Part 1:\n{await p1(f)}")

    if stage == 2 or stage < 1:
        print(f"Part 2:\n{await p2(f)}")


def dig_count(n: int) -> int:
    return len(str(n))

def dig_parity(n: int) -> Literal["even", "odd"]:
    return "even" if dig_count(n) % 2 == 0 else "odd"

def get_parts(n: int):
    s = str(n)
    return s[:len(s)//2], s[len(s)//2:]

@cache
def check_invalid(x: int):
    if dig_parity(x) == "odd":
        return False

    a, b = get_parts(x)
    return a == b

def invalid_compute(x: int, y: int) -> int:
    """
    My try to compute the count in an effective way without
    iterating through all numbers, not finished but whatever...
    """

    lx = dig_count(x)
    ly = dig_count(y)

    t = 0

    xl, xr = get_parts(x)
    yl, yr = get_parts(y)

    for i in range(lx, ly + 1):
        # Even ones are gg
        if i % 2 == 1:
            continue

        i2 = i // 2

        if i > lx:
            xl = "1" + "0" * (i2 - 1)
            xr = "0" * i2

        diff = ly - lx
        print(f"Length: {i} (diff: {diff}) xl: {xl} xr: {xr} | yl: {yl} yr: {yr}")
        curr = 0

        if diff > 0:
            if lx == ly:
                _a = int(yl[0])

            else:
                _a = 9

            curr = abs(int(xr[0]) - _a) + 1
            print(f"Initial curr for diff>0: curr={curr} xl[0]={xl[0]} xr[0]={xr[0]}")

            for _x, _y in zip(xl[1:], xr[1:]):
                print(f"_x={_x}, _y={_y}")
                curr *= 10 * (9 - max(int(_x), int(_y)) + 1)

            print(f"diff ({diff}) > 0: curr={curr}")

        else:
            curr = abs(int(yr[0]) - int(xr[0])) + 1
            print(f"Initial curr for diff==0: curr={curr} yr[0]={yr[0]} xr[0]={xr[0]}")

            for _x, _y in zip(xr[1:], yr[1:]):
                print(f"_x={_x}, _y={_y}")
                curr *= 10 * (9 - max(int(_x), int(_y)) + 1)

            print(f"diff ({diff}) == 0: curr={curr}")

        t += curr

        print(
            dumps(
                {
                    "length": i,
                    "diff": diff,
                    "x": (xl, xr),
                    "y": (yl, yr),
                    "count": curr,
                    "total": t,
                }, 
                indent=2
            )
        )

    return t


async def p1(f: list[list[str]]) -> int:
    invalid = 0

    for a, b in f:
        for x in range(int(a), int(b) + 1):
            if check_invalid(x):
                # print(f"Invalid ({a}, {b}): {x}")
                invalid += x

    return invalid


@cache
def check_invalid_2(x: int, debug: bool = False) -> bool:
    xs = str(x)
    assert len(xs) > 0, "Number must have at least one digit"

    xs_len = len(xs)

    f = xs[0]

    freq: dict[str, int] = defaultdict(lambda: 0)
    words: dict[str, int] = defaultdict(lambda: 0)

    curr: List[str] = [""]

    for i, c in enumerate(xs):
        if c not in freq:
            freq[c] = 0

        freq[c] += 1

        # if i > xs_len // 2:
        #     for

        if i > 0:
            if c == f:
                for w in curr:
                    if len(w) > 0 and w[0] == c:
                        words[w] += 1

                        if debug:
                            print(f"Word completed: words[{w}] = {words[w]}")

                curr.append("")

        for j in range(len(curr)):
            curr[j] += c

        if debug:
            print(f"{xs}[{i}] = {c} -> {curr}\n")

    for w in curr:
        words[w] += 1

    freq = dict(freq)
    words = dict(words)

    if debug:
        for w in curr:
            print(f"Word completed: words[{w}] = {words[w]}\n")

        print(f"{x}\n words = {words}\n freq  = {freq}\n")

    found = None

    for k, v in words.items():
        if v <= 1:
            continue

        if k * v == xs:
            if debug:
                print(f"Found repeating word that makes up the whole number: {k} * {v} == {xs}\n")

            found = k
            break

    if debug:
        print(f"Found word: {found}\n")

    return found is not None

async def p2(f: list[list[str]]) -> int:
    invalid = 0

    for a, b in f:
        for x in range(int(a), int(b) + 1):
            if check_invalid_2(x):
                # print(f"Invalid #2 ({a}, {b}): {x}")
                invalid += x

    return invalid
