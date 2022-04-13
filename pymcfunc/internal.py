import functools
from typing import Tuple, Any, Sequence
import pymcfunc.errors as errors

def defaults(*vals: Tuple[Any, Any]):
    """(v, dv)"""
    args = ""
    not_default_detected = False
    for v, dv in reversed(vals):
        if not_default_detected:
            args = str(v)+" "+args
        elif v != dv:
            not_default_detected = True
            args = str(v)+" "+args
    return args.strip()

def options(var: Any, opts: Sequence):
    if var not in opts:
        raise errors.OptionError(opts, var)

def pick_one_arg(*vars_: Tuple[Any, Any, str], optional: bool=True):
    """(v, dv, varname)"""
    sameCount = 0
    diffFound = False
    diff = None
    diffname = None
    defaultNotNone = None
    for v, dv, varname in vars_:
        if v == dv:
            sameCount += 1
            if dv is not None:
                defaultNotNone = dv
        elif v != dv and diffFound:
            raise errors.OnlyOneAllowed([i[2] for i in vars_], f"'{varname}' and '{diffname}'")
        elif v != dv:
            diffFound = True
            diff = v
            diffname = varname

    if diff is None and not optional:
        raise errors.OptionError([i[2] for i in vars_], None)
    elif diff is None:
        diff = defaultNotNone

    return diff

def reliant(indep_name: str, indep_value: Any, indep_default: Any, dep_name: str, dep_value: Any, dep_default: Any):
    # only when both are optional params, and the default value of the indep param is None
    if dep_value != dep_default and indep_value == indep_default:
        raise errors.ReliantError(indep_name, dep_name)

def check_invalid_params(allowed_val: Any, other_param_name: str, other_val: Any, *params: Tuple[str, Any, Any], dep_mandatory: bool=False):
    """(name, val, default)"""
    for name, val, default in params:
        if other_val != allowed_val and val != default:
            raise errors.InvalidParameterError(allowed_val, other_param_name, other_val, name)
        # only when default is None
        if dep_mandatory and other_val == allowed_val and val == default:
            raise errors.MissingError(name, other_param_name, other_val)

def multi_check_invalid_params(allowed_vals: Sequence[Any], other_param_name: str, other_val: Any, *params: Tuple[str, Any, Any], dep_mandatory: bool=False):
    """(name, val, default)"""
    for name, val, default in params:
        for allowed_val in allowed_vals:
            if (other_val == allowed_val and val != default) or (other_val != allowed_val and val == default):
                break
        else:
            raise errors.InvalidParameterError(", ".join(allowed_vals), other_param_name, other_val, name)
        for allowed_val in allowed_vals:
            # only when default is None
            if dep_mandatory and other_val == allowed_val and val == default:
                raise errors.MissingError(name, other_param_name, other_val)


def check_spaces(name: str, val: str):
    if " " in val:
        raise errors.SpaceError(name, val)

def unspace(val: str):
    if val is not None and " " in val:
        return "\""+val+"\""
    else:
        return val

def unstated(indep_name: str, indep_value: Any, indep_reqvals: Sequence[Any], dep_name: str, dep_value: Any, dep_default: Any):
    # only when the dep is mandatory due to the indep, and the dep's default is None
    for indep_reqval in indep_reqvals:
        if indep_value == indep_reqval and dep_value != dep_default:
            break
    else:
        raise errors.MissingError(dep_name, indep_name, indep_value)

def check_range(r: dict):
    if isinstance(r, dict):
        for k, v in r:
            if k not in ['min', 'max']:
                raise KeyError(f"Invalid key: {k}; only 'min' and 'max' allowed")

def immutable(cls):
    @functools.wraps(cls, updated=())
    class Immutable(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            def _immutable_lock(*_):
                raise AttributeError(f"{type(self).__name__} is immutable")
            self.__setattr__ = _immutable_lock
    return Immutable

def base_class(cls):
    @functools.wraps(cls, updated=())
    class BaseClass(cls):
        def __init__(self, *args, **kwargs):
            if type(self) == BaseClass:
                raise TypeError("Base classes are not allowed to be instantiated. Use the Java or Bedrock classes instead.")

            super().__init__(*args, **kwargs)