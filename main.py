import asyncio
import importlib
import sys
from time import time
from pathlib import Path
import tracemalloc
import threading

import click


MAIN_TEMPLATE = '''
import aiofiles

from src.utils.decs import timeit


PartType = list[str]


async def main(fn: str = "in.txt", stage: int = 1, debug: bool = False):
    async with aiofiles.open(fn, mode='r') as f:
        f = await f.readlines()

    print("{day}: {{}} -> {{}} lines".format(fn, len(f)))

    # Pre-process input based on challenge
    # f = ...

    if stage == 1 or stage < 1:
        print(f"Part 1:\\n{{await p1(f, debug=debug)}}")

    if stage == 2 or stage < 1:
        print(f"Part 2:\\n{{await p2(f, debug=debug)}}")


@timeit
async def p1(f: PartType, debug: bool = False) -> int:
    return 0


@timeit
async def p2(f: PartType, debug: bool = False) -> int:
    return 0
'''.strip()


def print_memory_graph(samples, width=60, height=10):
    """Print an ASCII graph of memory usage over time."""
    if len(samples) < 2:
        print("\nMemory Usage Over Time:")
        print("Not enough samples collected (execution too fast)")
        return

    max_mem = max(samples)
    min_mem = min(samples)
    mem_range = max_mem - min_mem if max_mem > min_mem else max_mem * 0.1  # At least 10% range for visualization

    print("\nMemory Usage Over Time:")
    print(f"Samples: {len(samples)} | Peak: {max_mem / 1024 / 1024:.2f} MB | Min: {min_mem / 1024 / 1024:.2f} MB | Avg: {sum(samples) / len(samples) / 1024 / 1024:.2f} MB\n")

    line = ""

    # Resample to fit width
    if len(samples) <= width:
        # Interpolate to fill width for better visualization
        display_samples = []
        for i in range(width):
            idx = min(int(i * len(samples) / width), len(samples) - 1)
            display_samples.append(samples[idx])
    else:
        # Downsample
        step = len(samples) / width
        display_samples = [samples[int(i * step)] for i in range(width)]

    # Print the graph (from top to bottom)
    for row in range(height, -1, -1):
        line = ""
        for sample in display_samples:
            # Normalize sample to 0-height range
            sample_height = (sample - min_mem) / mem_range * height
            if sample_height > row:
                line += "█"
            elif sample_height > row - 0.5:
                line += "▄"
            else:
                line += " "

        # Calculate the memory value for this row (this row represents values AT this height)
        row_mem = min_mem + (mem_range * row / height)

        if row == height:
            print(f"{row_mem / 1024 / 1024:6.2f} MB   |{line}|")
        elif row == 0:
            print(f"{row_mem / 1024 / 1024:6.2f} MB   |{line}|")
        elif row == height // 2:
            # Show mid-point label
            print(f"{row_mem / 1024 / 1024:6.2f} MB   |{line}|")
        else:
            print(f"            |{line}|")

    print(f"            └{'─' * len(line)}┘")
    print(f"             Start{' ' * (len(line) - 11)}End")


@click.group()
def main():
    pass


@main.command()
@click.argument("n", type=int)
@click.option("--fn", "-f", type=str, default=None, help="Input file name", show_default=True)
@click.option("--stage", "-s", type=int, default=0, help="Stage number (1 or 2)", show_default=True)
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
@click.option("--mem-graph", "-m", is_flag=True, help="Show memory usage graph")
def run(n: int, fn: str | None = None, stage: int = 1, debug: bool = False, mem_graph: bool = False):
    day = f"{n:02d}"
    module_name = f"src.{day}.main"

    try:
        module = importlib.import_module(module_name)

    except ModuleNotFoundError:
        print(f"Error: Module {module_name} not found")
        sys.exit(1)

    if not fn:
        if stage == 1 or stage == 2:
            fn = "in1.txt"

        else:
            fn = "in.txt"

    print(f"debug: Running day {n:02d}, stage {stage}, file: {fn}, debug: {debug}")

    # Make the path relative to the module
    fn_p = Path(__file__).parent / "src" / day / fn

    tracemalloc.start()

    # Memory sampling for graph
    memory_samples = []
    stop_sampling = threading.Event()

    def sample_memory():
        while not stop_sampling.is_set():
            current, _ = tracemalloc.get_traced_memory()
            memory_samples.append(current)
            stop_sampling.wait(0.001)  # Sample every 1ms

    if mem_graph:
        sampler = threading.Thread(target=sample_memory, daemon=True)
        sampler.start()

    t = time()
    asyncio.run(
        module.main(
            fn=fn_p.as_posix(),
            stage=stage,
            debug=debug
        )
    )
    elapsed_time = time() - t

    stop_sampling.set()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\n---\n{n:02d}.{stage}: {elapsed_time:.4f} s | Memory: {peak / 1024 / 1024:.2f} MB (peak)")

    if mem_graph and memory_samples:
        print_memory_graph(memory_samples)


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
