from typing import Union
import pymcfunc.errors as errors

def coords(x: Union[Union[int, float], str], y: Union[Union[int, float], str], z: Union[Union[int, float], str]):
    """Translates values into coordinates, with extra validaton.
    More info: https://pymcfunc.rtfd.io/en/latest/reference.html#pymcfunc.coords"""
    result = f"{x} {y} {z}"
    
    if "^" in result and "~" in result:
        raise errors.CaretError(result, "tilde")
    elif "^" in result and not all("^" in str(i) for i in (x, y, z)):
        raise errors.CaretError(result, "notall")

    return result