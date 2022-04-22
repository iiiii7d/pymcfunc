from __future__ import annotations

# noinspection PyUnresolvedReferences
from typing import _LiteralGenericAlias, Any, _UnionGenericAlias, get_args, get_origin, _GenericAlias, Type

from pymcfunc.data_formats.nbt import NBT, DictReprAsList, Compound, String


class NBTFormat(NBT):
    @property
    def py(self) -> dict:
        d = {}
        for var, anno in type(self).__annotations__.items():
            if var not in self.NBT_FORMAT: continue
            if anno == DictReprAsList:
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
                                                  type(self).__annotations__[subname], format_type)
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
            if isinstance(get_origin(format_type), DictReprAsList):
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
        for var, anno in type(self).__annotations__.items():
            var = var.removesuffix("_")
            if var not in self.NBT_FORMAT: continue
            format_type = self.NBT_FORMAT[var]
            d[var] = self._convert_to_nbt(var, getattr(self, var), anno, format_type)
        return Compound(d)

    NBT_FORMAT: dict[str, Type[NBT] | dict[str, Type[NBT]]] | property = {}

class JsonFormat:
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
            if isinstance(get_origin(format_type), DictReprAsList):
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
        for var, anno in type(self).__annotations__.items():
            var = var.removesuffix("_")
            if var not in self.JSON_FORMAT: continue
            format_type = self.JSON_FORMAT[var]
            d[var] = self._convert_to_json(var, getattr(self, var), anno, format_type)
        return d

    JSON_FORMAT: dict[str, type] | property = {}