import copy
import hashlib
import inspect
import os

import psutil

from . import profiler_output_pb2 as profiler_output


def get_function_name(func):
    return func.__name__


def get_func_params(args, func):
    result = []
    sig = inspect.signature(func)
    params = sig.parameters
    for i, arg in enumerate(args):
        arg_name = list(params.keys())[i] if i < len(params) else 'N/A'
        result.append(profiler_output.FuncParams(
            arg=str(arg),
            arg_name=arg_name,
            type=type(arg).__name__
        ))
    return result


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def get_cpu_usage():
    process = psutil.Process(os.getpid())
    return process.cpu_percent()


def deep_copy_args(args):
    result = []
    for arg in args:
        try:
            result.append(copy.deepcopy(arg))
        except Exception:
            result.append(copy.copy(arg))
    return result


def hash_function(func):
    try:
        source_code = inspect.getsource(func)
    except TypeError:
        raise ValueError("The provided argument is not a function.")

    source_hash = hashlib.sha256(source_code.encode('utf-8')).hexdigest()
    return source_hash
