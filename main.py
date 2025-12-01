import asyncio
import importlib
import sys
from pathlib import Path

import click


@click.group()
def main():
    pass


@main.command()
@click.argument("n", type=int)
def run(n: int):
    day = f"{n:02d}"
    module_name = f"src.{day}.main"

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Error: Module {module_name} not found")
        sys.exit(1)

    asyncio.run(module.main())


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
    (day_dir / "main.py").write_text(f'''async def main():
    print("Hello from aoc25 Day #{day}!")
''')
    (day_dir / "in.txt").touch()
    (day_dir / "in1.txt").touch()
    (day_dir / "in2.txt").touch()
    print(f"Created {day_dir}")


if __name__ == "__main__":
    main()
