import aiofiles


async def main(fn: str, stage: int = 1, debug: bool = False):
    async with aiofiles.open(fn, mode='r') as f:
        f = await f.readlines()

    d = [
        (x[0], int(x[1:]))
        for x in f
    ]

    print(f"1: {await p1(d)}")
    print(f"2: {await p2(d)}")


async def p1(l: list[tuple[str, int]]):
    p = 50
    zero = 0

    for d, v in l:
        match d:
            case "L":
                p = (p - v) % 100

            case "R":
                p = (p + v) % 100

        if p == 0:
            zero += 1

    return p, zero


async def p2(l: list[tuple[str, int]]):
    p = 50
    zero = 0

    for d, v in l:
        pp = p

        match d:
            case "L":
                p = p - v

                if p <= 0:
                    # The pp check is key for when you started at 0 :/
                    # to not count it twice...
                    zero += ((p * -1) // 100) + (1 if pp != 0 else 0)

                p = p % 100

            case "R":
                p = p + v

                if p >= 100:
                    zero += p // 100

                p = p % 100

    return p, zero
