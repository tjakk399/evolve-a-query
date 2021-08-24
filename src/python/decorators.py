import functools

def repeater(n=2):
    def repeater_inner(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper_repeat
    return repeater_inner

def sorter(key=lambda x: x, reverse=False):
    def sorter_inner(func):
        def wrapper(*args, **kwargs):
            return sorted(
                    func(*args, **kwargs),
                    key = key,
                    reverse = reverse,
                    )
        return wrapper
    return sorter_inner
