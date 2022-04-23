from __future__ import annotations

# noinspection PyUnresolvedReferences
from typing import _LiteralGenericAlias, Any, _UnionGenericAlias, get_args, get_origin, _GenericAlias, Type, TypeVar, \
    Generic, TYPE_CHECKING

from pymcfunc.data_formats.nbt_path import TypedCompoundPath

if TYPE_CHECKING: from pymcfunc.functions import JavaFunctionHandler
from pymcfunc.data_formats.coord import BlockCoord
from pymcfunc.data_formats.nbt_tags import NBT, CompoundReprAsList, Compound, String, Byte

from pymcfunc.proxies.selectors import JavaSelector


def pascal_case_ify(var: str, is_potion_effect: bool = False) -> str:
    var = var.removesuffix("_")
    if var == 'uuid':
        return 'UUID'
    elif var == 'no_ai':
        return 'NoAI'
    elif var == 'id' and not is_potion_effect:
        return 'id'
    else:
        return ''.join(x.title() for x in var.split('_'))

class NBTFormat(Compound):
    def __init_subclass__(cls, do_pascal_case_ify: bool = True, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._do_pascal_case_ify = do_pascal_case_ify

    @classmethod
    def get_format(cls) -> dict[str, Type[NBT]]:
        return {k: v for c in cls.mro() if hasattr(c, '__annotations__') for k, v in c.__annotations__.items()}

    @property
    def py(self) -> dict:
        d = {}
        for var, anno in type(self).get_format().items():
            #if var not in self.NBT_FORMAT: continue
            if anno == CompoundReprAsList:
                d[var] = [v.as_json() for v in getattr(self, var)]
            else:
                if isinstance(getattr(self, var), NBT):
                    d[var] = getattr(self, var).py
                elif isinstance(getattr(self, var), list):
                    d[var] = [v.py for v in getattr(self, var)]
                elif isinstance(getattr(self, var), dict):
                    d[var] = {k: v.py for k, v in getattr(self, var).items()}
                else:
                    d[var] = getattr(self, var)
        return d

    def _convert_to_nbt(self, name: str,
                        val: Any,
                        py_type: type,
                        format_type: Type[NBT] | dict) -> NBT | None:
        if not isinstance(format_type, _LiteralGenericAlias) and not isinstance(val, py_type):
            raise TypeError(f"`{name}` must be of {py_type} (got {val})")
        if issubclass(format_type, NBTFormat) and isinstance(val, format_type):
            return val.as_nbt()
        elif issubclass(format_type, NBT) and isinstance(val, format_type):
            return val
        elif isinstance(format_type, _LiteralGenericAlias):
            if val not in get_args(format_type):
                raise ValueError(f"{val} is not in {get_args(format_type)}")
            return String(val)
        elif isinstance(format_type, dict):
            d = {}
            for subname, subformat_type in format_type.items():
                subval = getattr(self, subname, None)
                d[subname] = self._convert_to_nbt(subname, subval,
                                                  type(self).get_format()[subname], format_type)
            return Compound(d)
        elif isinstance(format_type, _UnionGenericAlias):
            if type(None) in get_args(format_type) and val is None: return None
            for format_subtype in get_args(format_type):
                try:
                    return self._convert_to_nbt(name, val, py_type, format_subtype)
                except Exception:
                    pass
            else:
                raise TypeError(
                    f"`{name}` is not one of types {', '.join(str(a) for a in get_args(format_type))} (got {val})")
        elif isinstance(format_type, _GenericAlias):
            if isinstance(get_origin(format_type), CompoundReprAsList):
                val: list
                ft, = get_args(format_type)
                pt, = get_args(py_type)
                return Compound({v.name: self._convert_to_nbt(name, v, pt, ft) for v in val})
            elif isinstance(get_origin(format_type), dict):
                val: dict
                kft, vft = get_args(format_type)
                _, vpt = get_args(py_type)
                if isinstance(kft, _LiteralGenericAlias):
                    for k in val.keys():
                        if not isinstance(k, kft):
                            raise TypeError(f"{k} is not of type {kft}")
                return Compound({k: self._convert_to_nbt(name, v, vpt, vft) for k, v in val.items()})
        else:
            return format_type(val)

    def as_nbt(self) -> Compound:
        d = {}
        for var, anno in type(self).get_format().items():
            if self._do_pascal_case_ify: var = pascal_case_ify(var, isinstance(anno, Byte))
            #if var not in self.NBT_FORMAT: continue
            #format_type = self.NBT_FORMAT[var]
            d[var] = self._convert_to_nbt(var, getattr(self, var), anno, anno)
            if d[var] is None: del d[var]
        return Compound(d)

    @classmethod
    def as_path(cls, *,
                fh: JavaFunctionHandler | None = None,
                sel: JavaSelector | None = None,
                block_pos: BlockCoord | None = None,
                rl: str | None = None) -> TypedCompoundPath:
        return TypedCompoundPath[cls](fh=fh, sel=sel, block_pos=block_pos, rl=rl)

class JsonFormat:
    @classmethod
    def _get_annotations(cls):
        return {k: v for c in cls.mro() if hasattr(c, '__annotations__') for k, v in c.__annotations__.items()}

    def _convert_to_json(self, name: str, val: Any, py_type: type, format_type: type) -> Any:
        if not isinstance(format_type, _LiteralGenericAlias) and not isinstance(val, py_type):
            raise TypeError(f"`{name}` must be of {py_type} (got {val})")
        if issubclass(format_type, dict):
            if isinstance(val, JsonFormat):
                return val.as_json()
            elif isinstance(val, NBT):
                return val.py
            else:
                return val
        elif issubclass(format_type, _LiteralGenericAlias):
            if val not in get_args(format_type):
                raise ValueError(f"{val} is not in {get_args(format_type)}")
            return val
        elif issubclass(format_type, _UnionGenericAlias):
            if type(None) in get_args(format_type) and val is None: return None
            for format_subtype in get_args(format_type):
                try:
                    return self._convert_to_json(name, val, py_type, format_subtype)
                except Exception:
                    pass
            else:
                raise TypeError(
                    f"`{name}` is not one of types {', '.join(str(a) for a in get_args(format_type))} (got {val})")
        elif isinstance(format_type, _GenericAlias):
            if isinstance(get_origin(format_type), CompoundReprAsList):
                val: list
                ft, = get_args(format_type)
                pt, = get_args(py_type)
                return {v.name: self._convert_to_json(name, v, pt, ft) for v in val}
            elif isinstance(get_origin(format_type), dict):
                val: dict
                kft, vft = get_args(format_type)
                _, vpt = get_args(py_type)
                if isinstance(kft, _LiteralGenericAlias):
                    for k in val.keys():
                        if not isinstance(k, kft):
                            raise TypeError(f"{k} is not of type {kft}")
                return {k: self._convert_to_json(name, v, vpt, vft) for k, v in val.items()}
        else:
            return format_type(val)

    def as_json(self) -> dict:
        d = {}
        for var, anno in type(self)._get_annotations().items():
            var = var.removesuffix("_")
            if var not in self.JSON_FORMAT: continue
            format_type = self.JSON_FORMAT[var]
            d[var] = self._convert_to_json(var, getattr(self, var), anno, format_type)
            if d[var] is None: del d[var]
        return d

    JSON_FORMAT: dict[str, type] | property = {}
