def merge(a: dict, b: dict, path=[]):
    """Merge two dictionaries recursively."""
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] != b[key]:
                raise Exception("Conflict at " + ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def backfill(base: dict, overlay: dict):
    """Deep merge two dictionaries, with the second dictionary taking precedence, back-filling with the first."""
    return merge(base, overlay)


def filternulls(d: dict):
    """Filter out null values from a dictionary, recursively"""

    for k, v in list(d.items()):
        if v is None:
            del d[k]
        elif isinstance(v, dict):
            filternulls(v)
    return d


import functools


def non_recursive(decorator):
    @functools.wraps(decorator)
    def wrapper(func):
        # Create an attribute to track recursion state
        func._is_decorating = False

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if func._is_decorating:
                return func(*args, **kwargs)  # Bypass decoration if already decorating

            func._is_decorating = True  # Set recursion flag
            try:
                return decorator(func)(*args, **kwargs)  # Apply decorator
            finally:
                func._is_decorating = False  # Reset flag after execution

        return wrapped_func

    return wrapper
