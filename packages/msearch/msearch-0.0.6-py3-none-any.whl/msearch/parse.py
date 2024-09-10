import functools
import pathlib
from typing import Dict


import functools
import pathlib
import shlex
from typing import Dict, List, Tuple

def mparse(arg_string, file_contents=None):
    """Parse arguments and keyword arguments from a string."""
    args = []
    kwargs = {}
    
    # Split the string into individual arguments
    arg_list = shlex.split(arg_string)
    
    for arg in arg_list:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key.strip()] = value.strip()
        else:
            args.append(arg.strip())
    
    return args, kwargs
