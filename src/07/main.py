from time import sleep
from typing import Any
import aiofiles

from src.utils.decs import timeit


PartType = list[list[str]]

def print_f(f: list[list[Any]], first: bool = False):
    if not first:
        print(f"\033[{len(f) + 1}A", end="")

    for row in f:
        for c in row:
            if c is None:
                print("   ", end="")

            else:
                match c:
                    case int():
                        print(f"({c})", end="")

                    case str():
                        print(c, end="")

                    case bool():
                        print("Y" if c else "N", end="")


        print()

    print()

async def main(fn: str = "in.txt", stage: int = 1, debug: bool = False):
    async with aiofiles.open(fn, mode='r') as f:
        f = await f.readlines()

    print("07: {} -> {} lines".format(fn, len(f)))

    # Pre-process input based on challenge
    f = [
        list(line.rstrip("\n"))
        for line in f
    ]

    if stage == 1 or stage < 1:
        print(f"Part 1:\n{await p1(f, debug=debug)}")

    if stage == 2 or stage < 1:
        print(f"Part 2:\n{await p2(f, debug=debug)}")

def solve(f: PartType, debug: bool = False) -> tuple[PartType, int]:
    s = 0

    for i in range(len(f)):
        for j in range(len(f[i])):
            if f[i-1][j] == "S":
                f[i][j] = "|"

            elif f[i-1][j] == "|":
                    match f[i][j]:
                        case ".":
                            f[i][j] = "|"

                        case "^":
                            s += 1

                            if j - 1 >= 0 and f[i][j-1] == ".":
                                f[i][j-1] = "|"

                            if j + 1 < len(f[i]) and f[i][j+1] == ".":
                                f[i][j+1] = "|"

        if debug:
            print_f(f, first=(i==0))
            sleep(0.05)

    return f, s

@timeit
async def p1(_f: PartType, debug: bool = False) -> int:
    f = [row.copy() for row in _f]
    _, s = solve(f, debug=debug)
    return s


@timeit
async def p2(_f: PartType, debug: bool = False) -> int:
    f = [row.copy() for row in _f]
    ff, _ = solve(f, debug=debug)

    l: list[list[int | None]] = []

    for i in range(len(ff)):
        l.append([None] * len(ff[i]))

        for j in range(len(ff[i])):
            match ff[i][j]:
                case "|" | "S":
                    l[i][j] = 0

                case _:
                    l[i][j] = None

    for i in range(len(ff)):
        for j in range(len(ff[i])):
            if l[i][j] is None:
                continue

            if i == 0:
                l[i][j] += 1 # type: ignore
                continue

            if l[i-1][j] is not None:
                l[i][j] += l[i-1][j] # type: ignore

            if j - 1 >= 0 and l[i-1][j-1] is not None and ff[i][j-1] == "^":
                l[i][j] += l[i-1][j-1] # type: ignore

            if j + 1 < len(ff[i]) and l[i-1][j+1] is not None and ff[i][j+1] == "^":
                l[i][j] += l[i-1][j+1] # type: ignore

        if debug:
            print_f(l, first=(i==0))
            sleep(0.05)

    s = sum(
        x if x else 0
        for x in l[-1]
    )

    return s
