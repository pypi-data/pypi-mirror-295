import inspect
from typing import get_type_hints, Iterable, Union, Optional, Type, List, Dict
from collections.abc import Iterable as ABCIterable

class TypeException(Exception):
    pass

def rreplace(s, old, new):
    pos = s.rfind(old)

    if pos == -1:
        return s

    return s[:pos] + new + s[pos + len(old):]

def type_checker(func):
    type_hints = get_type_hints(func)

    def unwrap_optional(expected_type):
        """ Unwrap Optional type to get the type without None. """
        if hasattr(expected_type, '__origin__') and expected_type.__origin__ is Union:
            args = expected_type.__args__
            return [arg for arg in args]
        return [expected_type]

    def check_type(param_value, expected_type, param_name):
        if isinstance(expected_type, type):
            # Direct type check
            if not isinstance(param_value, expected_type):
                raise TypeException(f"[{param_name}] Expected type {expected_type.__name__}, but got {type(param_value).__name__}.")
        elif hasattr(expected_type, '__origin__'):
            # Handle generic types
            origin = expected_type.__origin__
            if origin in (list, tuple, set):
                if not isinstance(param_value, origin):
                    raise TypeException(f"[{param_name}] Expected type {expected_type.__name__}, but got {type(param_value).__name__}.")

                # Check the type of elements
                if hasattr(expected_type, '__args__') and len(expected_type.__args__) > 0:
                    element_type = expected_type.__args__[0]
                    if not all(isinstance(item, element_type) for item in param_value):
                        raise TypeException(f"[{param_name}] Expected all elements to be of type {element_type.__name__}, but got elements of type {[type(item).__name__ for item in param_value]}.")
            elif origin is dict:
                if not isinstance(param_value, dict):
                    raise TypeException(f"[{param_name}] Expected type {expected_type.__name__}, but got {type(param_value).__name__}.")
                
                if hasattr(expected_type, '__args__') and len(expected_type.__args__) == 2:
                    key_type, value_type = expected_type.__args__
                    if not all(isinstance(k, key_type) for k in param_value.keys()):
                        raise TypeException(f"[{param_name}] Expected all keys to be of type {key_type.__name__}, but got keys of type {[type(k).__name__ for k in param_value.keys()]}.")
                    if not all(isinstance(v, value_type) for v in param_value.values()):
                        raise TypeException(f"[{param_name}] Expected all values to be of type {value_type.__name__}, but got values of type {[type(v).__name__ for v in param_value.values()]}.")
            elif origin is Union:
                # Handle Union types
                possible_types = unwrap_optional(expected_type)
                matches = False
                for sub_type in possible_types:
                    try:
                        check_type(param_value, sub_type, param_name)
                        matches = True
                        break
                    except TypeException:
                        continue
                if not matches:
                    names = ", ".join([sub_type.__name__ for sub_type in possible_types])
                    names = rreplace(names, ", ", " or ")
                    raise TypeException(f"[{param_name}] Expected type {names}, but got {type(param_value).__name__}.")
            else:
                raise TypeException(f"[{param_name}] Unsupported generic type {expected_type}.")
        else:
            raise TypeException(f"[{param_name}] Unsupported type {expected_type}.")

    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        for param_name, param_value in bound_arguments.arguments.items():
            if param_name in type_hints:
                expected_type = type_hints[param_name]
                check_type(param_value, expected_type, param_name)

        result = func(*args, **kwargs)
        return result

    return wrapper


# from typing import List, Optional

# @type_checker
# def example_function(a: int, b: Optional[List[int]], c: Optional[str] = None):
#     print(a, b)

# example_function(10, [1, 2, 3])  # This should work
# example_function(10, None)       # This should also work
# try:
#     example_function(10, "string")   # This should raise a TypeException
# except TypeException:
#     print("Perfect")
# example_function(10, None, 1)
# from geometry.change_crs import CHANGE_CRS_OPTIONS
# def change_crs(item: CHANGE_CRS_OPTIONS,
#                src_crs: int,
#                dst_crs: int):
#     print(item)

# change_crs(None, 1, 1)