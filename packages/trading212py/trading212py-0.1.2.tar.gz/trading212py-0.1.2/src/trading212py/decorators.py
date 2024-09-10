from functools import wraps
import json
from typing import Optional
# ...

def debug(func):
    """Print the function signature and return value"""
    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__}() returned {repr(value)}")
        return value
    return wrapper_debug

def unpacker(cls:object=None,clsList:Optional[bool]=False):
    '''Unpack items to a class
    '''
    def decorator(f):    
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Do something before the function
            data = f(*args, **kwargs)
            # Do something after the function
            if data is None: return None
            else:
                if type(data) is not str:
                    if (cls is None and clsList is None) : return data
                    else:
                        if clsList is not False: return [cls(**item) for item in data]
                        else: return cls(**data)
                else: return data
        return wrapper
    return decorator

def jsondump(func):
    '''Dump the data as json
    '''
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        out_file = open("jsondump1.json", "w")
        json.dump(obj=data,fp=out_file)
        out_file.close()
        return data
    return wrapper