import logging
import functools
import time

# config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def log(level=logging.INFO):
    def decorator(obj):
        if isinstance(obj, type):  # for classes
            orig_init = obj.__init__

            @functools.wraps(orig_init)
            def new_init(self, *args, **kwargs):
                logging.log(level, f"Instantiating {obj.__name__} with args={args}, kwargs={kwargs}")
                start = time.time()
                orig_init(self, *args, **kwargs)
                end = time.time()
                logging.log(level, f"{obj.__name__} initialized in {end - start:.6f} s")
            obj.__init__ = new_init
            return obj

        elif callable(obj):  # for functions
            @functools.wraps(obj)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = obj(*args, **kwargs)
                duration = time.time() - start_time
                logging.log(level,
                            f"Called {obj.__name__}("
                            f"args={args}, kwargs={kwargs}) "
                            f">>> result: {result!r} "
                            f"[duration: {duration:.6f} s]")
                return result
            return wrapper
        else:
            raise TypeError("Unsupported type for log decorator")

    return decorator
