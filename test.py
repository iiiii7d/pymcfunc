import pymcfunc as pmf

p = pmf.Pack()

@p.function
def mcfuncjava(f: pmf.JavaFuncHandler):
    f.say('a')
    f.tell('@p', 'b')
    f.help()
    f.setblock("1 2 3", "assefsdaf")
    f.fill('1 2 3', '4 5 6', "assefsdaf")
    f.clone('1 2 3', '4 5 6', '7 8 9')
    f.kill("@p")

b = pmf.Pack('b')

@b.function
def mcfuncbedrock(f: pmf.BedrockFuncHandler):
    f.say('a')
    f.tell('@p', 'b')
    f.setblock("1 2 3", "assefsdaf")
    f.fill('1 2 3', '4 5 6', "assefsdaf")
    f.clone('1 2 3', '4 5 6', '7 8 9')
    f.kill("@p")

print(p.funcs)
print(b.funcs)
