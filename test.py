import pymcfunc as pmf

p = pmf.Pack()

@p.function
def diamond(f):
    f.say('a')
    f.tell('@p', 'b')
    f.setblock()

print(p.funcs)