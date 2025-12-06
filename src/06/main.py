from typing import Literal
import aiofiles
from pydantic import BaseModel

from src.utils.decs import timeit


class PartType(BaseModel):
    problems: list[list[int]]
    problems_2: list[list[list[int]]]

    ops: list[Literal["+", "*"]]


def clean_line(line: str) -> str:
    line = line.strip()

    # Keep only 1 space when multiple spaces exist
    while "  " in line:
        line = line.replace("  ", " ")

    return line


def apply_op(a: list[int], op: Literal["+", "*"]):
    t = 0 if op == "+" else 1

    for v in a:
        if op == "+":
            t += v
        elif op == "*":
            t *= v

    return t

# Because yes
MAX_N = 5

async def main(fn: str = "in.txt", stage: int = 1, debug: bool = False):
    async with aiofiles.open(fn, mode='r') as f:
        ff = await f.readlines()

    print("06: {} -> {} lines".format(fn, len(ff)))

    # Pre-process input based on challenge
    f = PartType(
        problems=[],
        problems_2=[],
        ops=[]
    )

    _c = 0
    _ca: list[int] = []

    for i, c in enumerate(ff[-1].rstrip("\n")):
        if c in ["+", "*"]:
            if _c > 0:
                _ca.append(_c - 1)

            _c = 1

        else:
            _c += 1

    _ca.append(_c)

    if debug:
        print(f"_ca = {_ca}")

    for i, line2 in enumerate(ff[:-1]):
        line2 = line2.rstrip("\n")

        line = clean_line(line2)
        lines = line.split(" ")

        parts = [
            int(x)
            for x in lines
        ]

        if i == 0:
            for p in parts:
                f.problems.append([p])

        else:
            for j, p in enumerate(parts):
                f.problems[j].append(p)

        l = 0
        a = []

        for _, cc in enumerate(_ca):
            r = l + cc

            _l = [
                int(x) if x.isdigit() else 0
                for x in line2[l:r]
            ]

            a.append(_l)
            l = r + 1

        f.problems_2.append(a)

    f.ops = [ # type: ignore
        x
        for x in clean_line(ff[-1]).split(" ")
    ]

    if debug:
        print(f.model_dump_json(indent=1))

    if stage == 1 or stage < 1:
        print(f"Part 1:\n{await p1(f, debug=debug)}")

    if stage == 2 or stage < 1:
        print(f"Part 2:\n{await p2(f, debug=debug)}")


@timeit
async def p1(f: PartType, debug: bool = False) -> int:
    return sum(
        apply_op(f.problems[i], f.ops[i])
        for i in range(len(f.problems))
    )


@timeit
async def p2(f: PartType, debug: bool = False) -> int:
    t = 0

    for l in range(len(f.ops)):
        a = []
        op_len = len(f.problems_2[0][l])

        for i in range(op_len):
            s = ""

            for j in range(len(f.problems_2)):
                if f.problems_2[j][l][i] > 0:
                    s += str(f.problems_2[j][l][i])

            if debug:
                print(f"Number of problem {i}, line {l}: '{s}'\n")

            a.append(int(s))

        if debug:
            print(f"Applying op {f.ops[l]} to values: {a}")

        t += apply_op(a, f.ops[l])

    return t
