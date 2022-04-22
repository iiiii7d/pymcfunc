from __future__ import annotations

# noinspection PyUnresolvedReferences
from typing import _LiteralGenericAlias, Any, _UnionGenericAlias, get_args, get_origin, _GenericAlias, Type, TypeVar, \
    Generic

from pymcfunc import JavaFunctionHandler, ExecutedCommand
from pymcfunc.data_formats.coord import BlockCoord
from pymcfunc.data_formats.nbt import NBT, DictReprAsList, Compound, String, Path
from pymcfunc.data_formats.raw_json import JNBTValues, JavaTextComponent
from pymcfunc.proxies.selectors import JavaSelector

_T = TypeVar('_T')
def pascal_case_ify(var: str):
    var = var.removesuffix("_")
    if var == 'uuid':
        return 'UUID'
    elif var != 'id':
        return ''.join(x.title() for x in var.split('_'))
    else:
        return var

class NBTFormatPath(Path, Generic[_T]):
    def __init__(self, root: str | None,
                 fh: JavaFunctionHandler | None = None,
                 sel: JavaSelector | None = None,
                 block_pos: BlockCoord | None = None,
                 rl: str | None = None):
        super().__init__(root)
        self.fh = fh
        self.sel = sel
        self.block_pos = block_pos
        self.rl = rl

    @property
    def _target(self):
        return {'entity': self.sel} if self.sel \
            else {'block': self.block_pos} if self.block_pos \
            else {'storage': self.rl} if self.rl \
            else {}

    @property
    def _target_with_prefix_target(self):
        return {'target_entity': self.sel} if self.sel \
            else {'target_block': self.block_pos} if self.block_pos \
            else {'target_storage': self.rl} if self.rl \
            else {}

    @property
    def _target_with_prefix_source(self):
        return {'source_entity': self.sel} if self.sel \
            else {'source_block': self.block_pos} if self.block_pos \
            else {'source_storage': self.rl} if self.rl \
            else {}

    def raw_json(self, interpret: bool | None = None,
                 separator: JavaTextComponent | None = None) -> JNBTValues:
        return JNBTValues(nbt=self,
                          entity=self.sel,
                          interpret=interpret,
                          separator=separator)

    def get(self, scale: float | None = None) -> ExecutedCommand:
        return self.fh.r.data_get(**self._target,
                                  path=self.root,
                                  scale=scale)

    def append(self, *,
               value: _T | None = None,
               from_: NBTFormatPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='append',
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def insert(self, index: int, *,
               value: _T | None = None,
               from_: NBTFormatPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='insert', index=index,
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def merge(self, *,
              value: _T | None = None,
              from_: NBTFormatPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='merge',
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def prepend(self, *,
                value: _T | None = None,
                from_: NBTFormatPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='prepend',
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def set(self, *,
            value: _T | None = None,
            from_: NBTFormatPath | None = None) -> ExecutedCommand:
        return self.fh.r.data_modify(**self._target_with_prefix_target,
                                     target_path=self,
                                     mode='set',
                                     value=value,
                                     **from_._target_with_prefix_source if from_ else {},
                                     source_path=from_)

    def remove(self):
        return self.fh.r.data_remove(entity=self.sel, path=self)

    # TODO type checking for data modify
    # TODO change value into NBTTag
    
class NBTFormat(Compound):
    @classmethod
    def _get_annotations(cls):
        return {k: v for c in cls.mro() if hasattr(c, '__annotations__') for k, v in c.__annotations__.items()}

    @property
    def py(self) -> dict:
        d = {}
        for var, anno in type(self)._get_annotations().items():
            #if var not in self.NBT_FORMAT: continue
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
                                                  type(self)._get_annotations()[subname], format_type)
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
        for var, anno in type(self)._get_annotations().items():
            var = pascal_case_ify(var)
            #if var not in self.NBT_FORMAT: continue
            #format_type = self.NBT_FORMAT[var]
            d[var] = self._convert_to_nbt(var, getattr(self, var), anno, anno)
        return Compound(d)

    #NBT_FORMAT: dict[str, Type[NBT] | dict[str, Type[NBT]]] | property = {}

class RuntimeNBTFormat(Compound):
    def __init__(self, *,
                 fh: JavaFunctionHandler | None = None,
                 sel: JavaSelector | None = None,
                 block_pos: BlockCoord | None = None,
                 rl: str | None = None):
        self.fh = fh
        self.sel = sel
        self.block_pos = block_pos
        self.rl = rl
        super().__init__(self._get_annotations())

    NBT_FORMAT = {}
    _get_annotations = lambda self: self.NBT_FORMAT

    attr_as_path = lambda self, item: \
        self.NBTFormatPath[self._get_annotations()[item]](pascal_case_ify(item),
                                                          self.fh, self.sel, self.block_pos, self.rl)

    def __getattr__(self, item) -> NBTFormatPath:
        if item not in self._get_annotations():
            return super().__getattribute__(self, item)
        return self.attr_as_path(item)

    def __setattr__(self, item, value):
        if item not in self._get_annotations():
            super().__setattr__(item, value)
        self.attr_as_path(item).set(value=value)

    def __delattr__(self, item):
        if item not in self._get_annotations():
            super().__delattr__(item)
        self.attr_as_path(item).remove()


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
        for var, anno in type(self)._get_annotations().items():
            var = var.removesuffix("_")
            if var not in self.JSON_FORMAT: continue
            format_type = self.JSON_FORMAT[var]
            d[var] = self._convert_to_json(var, getattr(self, var), anno, format_type)
        return d

    JSON_FORMAT: dict[str, type] | property = {}