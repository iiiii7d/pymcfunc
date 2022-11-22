try:
    from importlib import metadata
except ImportError:
    metadata = None
    pass

import tomlkit

import pkmc.nbt
import pkmc.world

try:
    __version__ = metadata.version(__package__)
except (metadata.PackageNotFoundError, AttributeError):
    try:
        with open("pyproject.toml", "r") as f:
            __version__ = tomlkit.load(f)["tool"]["poetry"]["version"]
    except FileNotFoundError:
        __version__ = "unknown"
