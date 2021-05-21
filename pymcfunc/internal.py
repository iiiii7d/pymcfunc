import pymcfunc.errors as errors

def defaults(*vals: tuple):
    args = ""
    not_default_detected = False
    for v, dv in reversed(vals):
        if not_default_detected:
            args = v+" "+args
        elif v != dv:
            not_default_detected = True
            args + v+" "+args
    return args.strip()

def options(var, options):
    if not var in options:
        raise errors.OptionError(options, var)