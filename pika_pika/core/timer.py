import time


def timeit(foo):
    """
    Only add to the class methods and functions.
    """

    def timed(*args, **kwargs):
        start_time = time.time()
        bar = foo(*args, **kwargs)
        end_time = time.time()
        try:
            print(
                f"{args[0].__class__.__name__}.{foo.__name__}(): took {round(end_time - start_time, 2)} seconds"
            )
        except IndexError:
            print(
                f"{foo.__class__.__name__} {foo.__name__}(): took {round(end_time - start_time, 2)} seconds"
            )
        return bar

    return timed


def async_timeit(foo):
    """
    For the Async/Await world!
    """

    async def timed(*args, **kwargs):
        start_time = time.time()
        bar = await foo(*args, **kwargs)
        end_time = time.time()

        try:
            print(
                f"{args[0].__class__.__name__}.{foo.__name__}(): took {round(end_time - start_time, 2)} seconds"
            )
        except IndexError:
            print(
                f"{foo.__class__.__name__} {foo.__name__}(): took {round(end_time - start_time, 2)} seconds"
            )

        return bar

    return timed
