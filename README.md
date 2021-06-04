# pymcfunc

[![Build Status](https://travis-ci.com/iiiii7d/pymcfunc.svg?branch=main)](https://travis-ci.com/iiiii7d/pymcfunc)
[![Documentation Status](https://readthedocs.org/projects/pymcfunc/badge/?version=latest)](https://pymcfunc.readthedocs.io/en/latest/?badge=latest)
![PyPI version](https://img.shields.io/pypi/v/pymcfunc)
![Github Version](https://img.shields.io/github/v/release/iiiii7d/pymcfunc?include_prereleases)
![Python Versions](https://img.shields.io/pypi/pyversions/pymcfunc)
![License](https://img.shields.io/github/license/iiiii7d/pymcfunc)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/iiiii7d/pymcfunc)
![GitHub repo size](https://img.shields.io/github/repo-size/iiiii7d/pymcfunc)
![GitHub last commit](https://img.shields.io/github/last-commit/iiiii7d/pymcfunc)
![GitHub Release Date](https://img.shields.io/github/release-date-pre/iiiii7d/pymcfunc)
![Lines of code](https://img.shields.io/tokei/lines/github/iiiii7d/pymcfunc)
[![Codecov](https://codecov.io/gh/iiiii7d/pymcfunc/branch/main/graph/badge.svg?token=BS3UCSBO41)](https://codecov.io/gh/iiiii7d/pymcfunc)
[![CodeFactor](https://www.codefactor.io/repository/github/iiiii7d/pymcfunc/badge)](https://www.codefactor.io/repository/github/iiiii7d/pymcfunc)

Minecraft functions, pythonised. Made by 7d

**Latest release version: v0.3**
Changelogs: https://pymcfunc.readthedocs.io/en/latest/changelog.html

**Documentation: https://pymcfunc.readthedocs.io/en/latest/**

## Why pymcfunc?
It would seem pretty obvious to program directly with Minecraft commands into functions;
however things start to get complicated when you try to do things that are simple in regular
programming but are cumbersome in Minecraft commands.

Hence pymcfunc, which translates Python code into Minecraft commands. The code is aimed to be
short, brief and concise so that it does not become another troublesome job.

Progress: Raw commands are complete, currently working on features to make programming functions easier,
and tools to build datapacks :)

## Usage
```python
import pymcfunc as pmf
p = pmf.Pack()

@p.function
def diamond(f: pmf.JavaFuncHandler):
    f.r.tell("@s", "Enjoy your free diamonds! :D")
    f.r.give("@s", "diamond", 64)

@p.function
def make_sheep_jump(f: pmf.JavaFuncHandler):
    f.r.execute(
      as_="@e[type=sheep]",
      run=lambda sf: [
        sf.r.tp(destxyz="~ ~1 ~"),
        sf.r.say("boingg")
      ]
    )

@p.function
def addition(f: pmf.JavaFuncHandler):
    val1 = f.v('val1', '@s')
    val1.set(10)
    val2 = f.v('val2', '@s')
    val2.set(20)
    val1 += val2
    f.r.tellraw('@s', pmf.rt.java("§aThe value is now ¶s[val1|@s]"))

@p.function
@p.t.repeat_every(6000)
def five_min_alert(f: pmf.JavaFuncHandler):
    f.r.tellraw('@a', pmf.rt.java("§c§l§w[This is 6000 ticks]5 minutes§xw have passed!"))

print(p.funcs)
```