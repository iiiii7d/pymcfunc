# pymcfunc

[![Build Status](https://travis-ci.com/iiiii7d/pymcfunc.svg?branch=main)](https://travis-ci.com/iiiii7d/pymcfunc)
[![Documentation Status](https://readthedocs.org/projects/pymcfunc/badge/?version=latest)](https://pymcfunc.readthedocs.io/en/latest/?badge=latest)
![PyPI version](https://img.shields.io/pypi/v/pymcfunc)
![Github Version](https://img.shields.io/github/v/release/iiiii7d/pymcfunc)
![Python Versions](https://img.shields.io/pypi/pyversions/pymcfunc)
![License](https://img.shields.io/github/license/iiiii7d/pymcfunc)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/iiiii7d/pymcfunc)
![GitHub repo size](https://img.shields.io/github/repo-size/iiiii7d/pymcfunc)
![GitHub last commit](https://img.shields.io/github/last-commit/iiiii7d/pymcfunc)
![GitHub Release Date](https://img.shields.io/github/release-date/iiiii7d/pymcfunc)
![Lines of code](https://img.shields.io/tokei/lines/github/iiiii7d/pymcfunc)
[![Codecov](https://codecov.io/gh/iiiii7d/pymcfunc/branch/main/graph/badge.svg?token=BS3UCSBO41)](https://codecov.io/gh/iiiii7d/pymcfunc)
[![CodeFactor](https://www.codefactor.io/repository/github/iiiii7d/pymcfunc/badge)](https://www.codefactor.io/repository/github/iiiii7d/pymcfunc)

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