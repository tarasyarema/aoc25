import time


def timeit(func):
    import functools

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"\ndebug: {func.__name__} took {end_time - start_time:.4f} s\n")
        return result

    return wrapper
