from copy import deepcopy

def deep_copy_arg(*copy_args: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            args = list(args)

            for copy_arg in copy_args:
                args[copy_arg] = deepcopy(args[copy_arg])

            if len(copy_args) == 0:
                args = deepcopy(args)

            return func(*args, **kwargs)
        return wrapper
    return decorator