import time 

def run_time(f):
    """
    A decorator that prints the runtime of a function.

    Args:
        f (function): The function for which the runtime is measured.

    Returns:
        function : The decorated function that prints the runtime.
    """
    def wrapper(* args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        stop_time = time.time()
        dt = stop_time - start_time
        print(f'Runtime {dt}s')
        return result
    return wrapper
