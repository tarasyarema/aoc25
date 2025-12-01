import asyncio
import importlib
import sys
from time import time
from pathlib import Path

import click


MAIN_TEMPLATE = '''
import aiofiles

async def main(fn: str = "in.txt", stage: int = 1):
    async with aiofiles.open(fn, mode='r') as f:
        f = await f.readlines()

    print("{day}: {{}} -> {{}} lines".format(fn, len(f)))
'''.strip()


@click.group()
def main():
    pass


@main.command()
@click.argument("n", type=int)
@click.option("--fn", "-f", type=str, default="in.txt", help="Input file name", show_default=True)
@click.option("--stage", "-s", type=int, default=0, help="Stage number (1 or 2)", show_default=True)
def run(n: int, fn: str = "in.txt", stage: int = 1):
    day = f"{n:02d}"
    module_name = f"src.{day}.main"

    try:
        module = importlib.import_module(module_name)

    except ModuleNotFoundError:
        print(f"Error: Module {module_name} not found")
        sys.exit(1)

    if stage == 1:
        fn = "in1.txt"

    elif stage == 2:
        fn = "in2.txt"

    # Make the path relative to the module
    fn_p = Path(__file__).parent / "src" / day / fn

    t = time()
    asyncio.run(
        module.main(
            fn=fn_p.as_posix(),
            stage=stage,
        )
    )

    print(f"\n---\n{n:02d}.{stage}: {time() - t:.4f} s")


@main.command()
@click.argument("n", type=int)
def new(n: int):
    day = f"{n:02d}"
    day_dir = Path(__file__).parent / "src" / day

    if day_dir.exists():
        print(f"Error: {day_dir} already exists")
        sys.exit(1)

    day_dir.mkdir(parents=True)
    (day_dir / "__init__.py").touch()
    (day_dir / "main.py").write_text(MAIN_TEMPLATE.format(day=day))
    (day_dir / "in.txt").touch()
    (day_dir / "in1.txt").touch()
    (day_dir / "in2.txt").touch()
    print(f"Created {day_dir}")


if __name__ == "__main__":
    main()
