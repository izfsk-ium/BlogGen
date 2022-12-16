#!/bin/python3

import os
import time


class BlogUtils:
    @staticmethod
    def find_file(base: str, ext: str):
        for root, _, fs in os.walk(base):
            for f in fs:
                if f.endswith(ext):
                    fullname = os.path.join(root, f)
                    yield (fullname, root)

    @staticmethod
    def timeit(f):
        def func(*args, **kwargs):
            time_start = time.perf_counter()
            result = f(*args, **kwargs)
            print(f"{f.__name__} used {time.perf_counter()-time_start:.5f} seconds.")
            return result

        return func
