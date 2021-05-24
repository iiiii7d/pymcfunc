# pymcfunc
Minecraft functions, pythonised. Made by 7d

**Current version: v0.0**

**Documentation: https://pymcfunc.readthedocs.io/en/latest/**

## Why pymcfunc?
It would seem pretty obvious to program directly with Minecraft commands into functions;
however things start to get complicated when you try to do things that are simple in regular
programming but are cumbersome in Minecraft commands.

Hence pymcfunc, which translates Python code into Minecraft commands. The code is aimed to be
short, brief and concise so that it does not become another troublesome job.

I'm writing code for the raw commands first - that being ordinary Minecraft commands.
After the raw commands, shortcuts will be written to shorten and clarify several tasks.
A datapack constructor will be made too :)

## Usage
```python
import pymcfunc as pmf
p = pmf.Pack()

@p.function
def diamond(f: pmf.JavaFuncHandler):
    f.tell("@s", "Enjoy your free diamonds! :D")
    f.give("@s", "diamond", 64)

print(p.funcs)
```