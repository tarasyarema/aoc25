import aiofiles

from src.utils.decs import timeit


PartType = list[list[bool]]


async def main(fn: str = "in.txt", stage: int = 1, debug: bool = False):
    async with aiofiles.open(fn, mode='r') as f:
        f = await f.readlines()

    print("04: {} -> {} lines".format(fn, len(f)))

    # Pre-process input based on challenge
    f = [
        [
            True if char == "@" else False for char in line.strip()
        ]
        for line in f
    ]

    if stage == 1 or stage < 1:
        print(f"Part 1:\n{await p1(f, debug=debug)}")

    if stage == 2 or stage < 1:
        print(f"Part 2:\n{await p2(f, debug=debug)}")


def get_forks(f: PartType) -> list[tuple[int, int]]:
    found = []

    for i, row in enumerate(f):
        for j, val in enumerate(row):
            if not val:
                continue

            d = 0

            for di in range(-1, 2):
                ii = i + di

                if ii < 0 or ii >= len(f):
                    continue

                for dj in range(-1, 2):
                    if di == 0 and dj == 0:
                        continue

                    jj = j + dj

                    if jj < 0 or jj >= len(row):
                        continue

                    if f[ii][jj]:
                        d += 1

            if d < 4:
                found.append((i, j))

    return found

@timeit
async def p1(f: PartType, debug: bool = False) -> int:
    return len(get_forks(f))


@timeit
async def p2(f: PartType, debug: bool = False) -> int:
    t = 0

    while True:
        forks = get_forks(f)

        if not forks:
            break

        t += len(forks)

        for i, j in forks:
            f[i][j] = False

    return t

