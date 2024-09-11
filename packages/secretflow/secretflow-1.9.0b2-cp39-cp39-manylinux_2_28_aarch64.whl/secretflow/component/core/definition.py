# Copyright 2024 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import importlib
import inspect
import re
from dataclasses import MISSING
from dataclasses import Field as DField
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Type, get_args, get_origin

import cleantext
from google.protobuf import json_format
from google.protobuf.message import Message as PbMessage

from secretflow.spec.v1.component_pb2 import (
    Attribute,
    AttributeDef,
    AttrType,
    ComponentDef,
    IoDef,
)
from secretflow.spec.v1.data_pb2 import DistData
from secretflow.spec.v1.evaluation_pb2 import NodeEvalParam

from .checkpoint import Checkpoint
from .common.types import Input, Output, UnionGroup
from .component import Component
from .dist_data.base import DistDataType


class CompDeclError(Exception): ...


class Interval:
    def __init__(
        self,
        lower: float = None,
        upper: float = None,
        lower_closed: bool = False,
        upper_closed: bool = False,
    ):
        self.lower = lower
        self.upper = upper
        self.lower_closed = lower_closed
        self.upper_closed = upper_closed

    @staticmethod
    def open(lower: float, upper: float) -> 'Interval':
        return Interval(
            lower=lower, upper=upper, lower_closed=False, upper_closed=False
        )

    @staticmethod
    def closed(lower: float, upper: float) -> 'Interval':
        return Interval(lower=lower, upper=upper, lower_closed=True, upper_closed=True)

    def enforce_closed(self):
        if self.lower != None and not self.lower_closed:
            if not self.lower.is_integer():
                raise ValueError(f"Lower bound must be an integer, {self.lower}")
            self.lower += 1
            self.lower_closed = True

        if self.upper != None and not self.upper_closed:
            if not self.upper.is_integer():
                raise ValueError(f"Upper bound must be an integer, {self.upper}")
            self.upper -= 1
            self.upper_closed = True

    def check(self, v: Any) -> tuple[bool, str]:
        fv = float(v)
        if self.upper is not None:
            if self.upper_closed:
                if fv > self.upper:
                    return (
                        False,
                        f"should be less than or equal {self.upper}, but got {v}",
                    )
            else:
                if fv >= self.upper:
                    return (
                        False,
                        f"should be less than {self.upper}, but got {v}",
                    )
        if self.lower is not None:
            if self.lower_closed:
                if fv < self.lower:
                    return (
                        False,
                        f"should be greater than or equal {self.lower}, but got {v}",
                    )
            else:
                if fv <= self.lower:
                    return (
                        False,
                        f"should be greater than {self.lower}, but got {v}",
                    )
        return True, ""


class FieldKind(Enum):
    BasicAttr = auto()
    PartyAttr = auto()
    CustomAttr = auto()
    StructAttr = auto()
    UnionAttr = auto()
    SelectionAttr = auto()
    TableColumnAttr = auto()
    Input = auto()
    Output = auto()


@dataclass
class _Metadata:
    prefixes: list = None
    fullname: str = ""
    name: str = ""
    type: Type = None
    kind: FieldKind = None
    desc: str = None
    is_optional: bool = False
    choices: list = None
    bound_limit: Interval = None
    list_limit: Interval = None
    default: Any = None
    input_name: str = None  # only used in table_column_attr
    custom_pb_cls: str = None  # only used in custom attr
    is_checkpoint: bool = False  # if true it will be save when dump checkpoint
    types: list[str] = None  # only used in input/output
    minor_min: int = 0  # the first supported minor version
    minor_max: int = -1  # the last supported minor version

    @property
    def is_deprecated(self) -> bool:
        return self.minor_max != -1

    def is_deprecated_minor(self, v: int) -> bool:
        return self.minor_max != -1 and v > self.minor_max


class Field:
    @staticmethod
    def _field(
        kind: FieldKind,
        minor_min: int,
        minor_max: int,
        desc: str,
        md: _Metadata = None,
        default: Any = None,
        init=True,
    ):
        if minor_max is None:
            minor_max = -1
        assert (
            minor_max == -1 or minor_min <= minor_max
        ), f"invalid minor version, {minor_min}, {minor_max}"
        if md is None:
            md = _Metadata()
        md.kind = kind
        md.desc = _clean_text(desc)
        md.minor_min = minor_min
        md.minor_max = minor_max

        if isinstance(default, list):
            default = MISSING
            default_factory = lambda: default
        else:
            default_factory = MISSING
        return field(
            default=default,
            default_factory=default_factory,
            init=init,
            kw_only=True,
            metadata={"md": md},
        )

    @staticmethod
    def attr(
        desc: str = "",
        is_optional: bool = None,
        default: Any = None,
        choices: list = None,
        bound_limit: Interval = None,
        list_limit: Interval = None,
        is_checkpoint: bool = False,
        minor_min: int = 0,
        minor_max: int = None,
    ):
        if is_optional is None:
            is_optional = default != MISSING and default is not None

        md = _Metadata(
            is_optional=is_optional,
            choices=choices,
            bound_limit=bound_limit,
            list_limit=list_limit,
            is_checkpoint=is_checkpoint,
            default=default if default != MISSING else None,
        )
        return Field._field(
            FieldKind.BasicAttr, minor_min, minor_max, desc, md, default
        )

    @staticmethod
    def party_attr(
        desc: str = "",
        list_limit: Interval = None,
        minor_min: int = 0,
        minor_max: int = None,
    ):
        md = _Metadata(list_limit=list_limit)
        return Field._field(FieldKind.PartyAttr, minor_min, minor_max, desc, md)

    @staticmethod
    def struct_attr(desc: str = "", minor_min: int = 0, minor_max: int = None):
        return Field._field(FieldKind.StructAttr, minor_min, minor_max, desc)

    @staticmethod
    def union_attr(
        desc: str = "", default: str = "", minor_min: int = 0, minor_max: int = None
    ):
        md = _Metadata(default=default)
        return Field._field(FieldKind.UnionAttr, minor_min, minor_max, desc, md)

    @staticmethod
    def selection_attr(desc: str = "", minor_min: int = 0, minor_max: int = None):
        return Field._field(FieldKind.SelectionAttr, minor_min, minor_max, desc)

    @staticmethod
    def custom_attr(
        pb_cls: type[PbMessage],
        desc: str = "",
        minor_min: int = 0,
        minor_max: int = None,
    ):
        assert inspect.isclass(pb_cls) and issubclass(
            pb_cls, PbMessage
        ), f"support protobuf class only, got {pb_cls}"

        extend_path = "secretflow.spec.extend."
        assert pb_cls.__module__.startswith(
            extend_path
        ), f"only support protobuf defined under {extend_path} path, got {pb_cls.__module__}"

        cls_name = ".".join(
            pb_cls.__module__[len(extend_path) :].split(".") + [pb_cls.__name__]
        )
        md = _Metadata(custom_pb_cls=cls_name)
        return Field._field(FieldKind.CustomAttr, minor_min, minor_max, desc, md)

    @staticmethod
    def table_column_attr(
        input_name: str,
        desc: str = "",
        limit: Interval = None,
        is_checkpoint: bool = False,
        minor_min: int = 0,
        minor_max: int = None,
    ):
        assert input_name != "", "input_name cannot be empty"
        md = _Metadata(
            input_name=input_name,
            list_limit=limit,
            is_checkpoint=is_checkpoint,
        )
        return Field._field(FieldKind.TableColumnAttr, minor_min, minor_max, desc, md)

    @staticmethod
    def input(
        desc: str = "",
        types: list[str] = None,
        minor_min: int = 0,
        minor_max: int = None,
    ):
        if types is not None:
            types = [str(s) for s in types]
        md = _Metadata(types=types)
        return Field._field(FieldKind.Input, minor_min, minor_max, desc, md)

    @staticmethod
    def output(
        desc: str = "",
        types: list[str] = None,
        minor_min: int = 0,
        minor_max: int = None,
    ):
        if types is not None:
            types = [str(s) for s in types]
        md = _Metadata(types=types)
        return Field._field(FieldKind.Output, minor_min, minor_max, desc, md)


def _clean_text(x: str, no_line_breaks: bool = True) -> str:
    return cleantext.clean(x.strip(), lower=False, no_line_breaks=no_line_breaks)


class Creator:
    def __init__(self, check_exist: bool) -> None:
        self._check_exist = check_exist

    def make(self, cls: Type, kwargs: dict, minor: int):
        args = {}
        for name, field in cls.__dataclass_fields__.items():
            if name == MINOR_NAME:
                continue
            args[name] = self._make_field(field, kwargs, minor)
        if len(kwargs) > 0:
            raise ValueError(f"unused fields {kwargs}")

        args[MINOR_NAME] = minor
        ins = cls(**args)
        setattr(ins, MINOR_NAME, minor)
        return ins

    def _make_field(self, field: DField, kwargs: dict, minor: int):
        md: _Metadata = field.metadata['md']
        if md.is_deprecated_minor(minor):
            return None

        if md.kind == FieldKind.StructAttr:
            return self._make_struct(md, kwargs, minor)
        elif md.kind == FieldKind.UnionAttr:
            return self._make_union(md, kwargs, minor)

        if minor < md.minor_min:
            return md.default

        if md.fullname not in kwargs:
            if self._check_exist and not md.is_optional:
                raise ValueError(f"{md.fullname} is required")
            else:
                return md.default

        value = kwargs.pop(md.fullname, md.default)

        if md.kind == FieldKind.Input:
            assert isinstance(value, DistData), f"type of {md.name} should be DistData"
            if md.types is not None:
                assert (
                    str(value.type) in md.types
                ), f"type of {md.name} must be in {md.types}"
            return value
        elif md.kind == FieldKind.Output:
            assert isinstance(
                value, (Output, str)
            ), f"type of {md.name} should be str or Output, but got {type(value)}"
            return value if isinstance(value, Output) else Output(uri=value, data=None)
        elif md.kind == FieldKind.TableColumnAttr:
            return self._make_str_or_list(md, value)
        elif md.kind == FieldKind.PartyAttr:
            return self._make_str_or_list(md, value)
        elif md.kind == FieldKind.CustomAttr:
            pb_cls = importlib.import_module("secretflow.spec.extend")
            for name in md.custom_pb_cls.split("."):
                pb_cls = getattr(pb_cls, name)
            return json_format.Parse(value, pb_cls())
        elif md.kind == FieldKind.BasicAttr:
            return self._make_basic(md, value)
        else:
            raise ValueError(f"invalid field kind, {md.fullname}, {md.kind}")

    def _make_struct(self, md: _Metadata, kwargs: dict, minor: int):
        cls = md.type
        args = {}
        for name, field in cls.__dataclass_fields__.items():
            args[name] = self._make_field(field, kwargs, minor)

        return cls(**args)

    def _make_union(self, md: _Metadata, kwargs: dict, minor: int):
        union_type = md.type
        if minor < md.minor_min:
            selected_key = md.default
        else:
            selected_key = kwargs.pop(md.fullname, md.default)

        if not isinstance(selected_key, str):
            raise ValueError(
                f"{md.fullname} should be a str, but got {type(selected_key)}"
            )
        choices = union_type.__dataclass_fields__.keys()
        if selected_key not in choices:
            raise ValueError(f"{selected_key} should be one of {choices}")

        selected_field = md.type.__dataclass_fields__[selected_key]
        selected_md: _Metadata = selected_field.metadata["md"]
        if selected_md.is_deprecated_minor(minor):
            raise ValueError(f"{selected_key} is deprecated")

        args = {}
        if selected_md.kind != FieldKind.SelectionAttr:
            value = self._make_field(selected_field, kwargs, minor)
            args = {selected_key: value}
        res: UnionGroup = md.type(**args)
        res.set_selected(selected_key)
        return res

    def _make_basic(self, md: _Metadata, value):
        is_list = isinstance(value, list)
        if is_list and md.list_limit:
            is_valid, err_str = md.list_limit.check(len(value))
            if not is_valid:
                raise ValueError(f"length of {md.fullname} is valid, {err_str}")

        check_list = value if is_list else [value]
        if md.bound_limit is not None:
            for v in check_list:
                is_valid, err_str = md.bound_limit.check(v)
                if not is_valid:
                    raise ValueError(f"value of {md.fullname} is valid, {err_str}")
        if md.choices is not None:
            for v in check_list:
                if v not in md.choices:
                    raise ValueError(
                        f"value {v} must be in {md.choices}, name is {md.fullname}"
                    )
        return value

    def _make_str_or_list(self, md: _Metadata, value):
        assert value is not None, f"{md.name} can not be none"
        is_list = get_origin(md.type) is list
        if not is_list:
            if isinstance(value, list):
                assert len(value) == 1, f"{md.name} can only have one element"
                value = value[0]
            assert isinstance(
                value, str
            ), f"{md.name} must be str, but got {type(value)}"
            return value
        else:
            assert isinstance(
                value, list
            ), f"{md.name} must be list[str], but got {type(value)}"
            if md.list_limit is not None:
                is_valid, err_str = md.list_limit.check(len(value))
                if not is_valid:
                    raise ValueError(f"length of {md.name} is invalid, {err_str}")

            return value


MINOR_NAME = "_minor"
RESERVED = ["input", "output"]


@dataclass
class _IoDef:
    io: IoDef  # type: ignore
    minor_min: int
    minor_max: int

    @property
    def name(self) -> str:
        return self.io.name

    @property
    def is_deprecated(self) -> bool:
        return self.minor_max != -1


@dataclass
class _AttrDef:
    attr: AttributeDef  # type: ignore
    minor_min: int
    minor_max: int

    @property
    def is_deprecated(self) -> bool:
        return self.minor_max != -1


class Reflector:
    def __init__(self, cls, name: str, minor: int):
        self._name = name
        self._minor = minor
        self._inputs: list[_IoDef] = []
        self._outputs: list[_IoDef] = []
        self._attrs: list[_AttrDef] = []
        self._attr_types: dict[str, AttrType] = {}  # type: ignore
        self.reflect(cls)

    def reflect(self, cls):  # type: ignore
        """
        Reflect dataclass to ComponentDef.
        """
        self._force_dataclass(cls)

        attrs: list[_Metadata] = []
        for field in cls.__dataclass_fields__.values():
            if field.name == MINOR_NAME:
                continue
            md = self._build_metadata(field, [])
            if md.kind == FieldKind.Input:
                io_def = self._reflect_io(md, Input)
                self._inputs.append(io_def)
            elif md.kind == FieldKind.Output:
                io_def = self._reflect_io(md, Output)
                self._outputs.append(io_def)
            else:
                attrs.append(md)

        for md in attrs:
            self._reflect_attr_field(md)

    def build_inputs(self) -> list[IoDef]:  # type: ignore
        return self._build_comp_io_defs(self._inputs, "input")

    def build_outputs(self) -> list[IoDef]:  # type: ignore
        return self._build_comp_io_defs(self._outputs, "output")

    def build_attrs(self) -> list[AttributeDef]:  # type: ignore
        return self._build_comp_attr_defs(self._attrs)

    def _build_comp_io_defs(self, io_defs: list[_IoDef], io_name: str) -> list[IoDef]:  # type: ignore
        if len(io_defs) == 0:
            return None

        return [d.io for d in io_defs if not d.is_deprecated]

    def _build_comp_attr_defs(self, attrs: list[_AttrDef]):
        result = []
        for attr in attrs:
            raw = attr.attr
            if attr.is_deprecated:
                assert (
                    attr.minor_max < self._minor
                ), f"minor_max of {raw.name} should be less than {self._minor}"
                continue
            if raw.type == AttrType.AT_COL_PARAMS and self._build_col_params_attr(raw):
                continue
            result.append(raw)

        return result

    def _build_col_params_attr(self, attr: AttributeDef) -> bool:  # type: ignore
        input_name = attr.col_params_binded_table
        io_def = next((io.io for io in self._inputs if io.name == input_name), None)
        if io_def is None:
            raise CompDeclError(f"cannot find input io, {input_name}")
        for t in io_def.types:
            if t not in [
                str(DistDataType.VERTICAL_TABLE),
                str(DistDataType.INDIVIDUAL_TABLE),
            ]:
                raise CompDeclError(f"{input_name} is not defined correctly in input.")
        if attr.prefixes is None or len(attr.prefixes) == 0:
            atomic = attr.atomic
            tbl_attr = IoDef.TableAttrDef(
                name=attr.name,
                desc=attr.desc,
                col_min_cnt_inclusive=atomic.list_min_length_inclusive,
                col_max_cnt_inclusive=atomic.list_max_length_inclusive,
            )
            io_def.attrs.append(tbl_attr)
            return True
        return False

    def _reflect_io(self, md: _Metadata, excepted_type: type):
        if md.type != excepted_type:
            raise CompDeclError(f"type of {md.name} must be {excepted_type}")
        return _IoDef(
            io=IoDef(name=md.name, desc=md.desc, types=md.types),
            minor_min=md.minor_min,
            minor_max=md.minor_max,
        )

    def _reflect_party_attr(self, md: _Metadata):
        is_list, org_tpye = self._check_list(md.type)
        assert org_tpye == str, f"the type of party attr should be str or list[str]"
        list_min_length_inclusive, list_max_length_inclusive = self._build_list_limit(
            is_list, md.list_limit
        )
        atomic = AttributeDef.AtomicAttrDesc(
            list_min_length_inclusive=list_min_length_inclusive,
            list_max_length_inclusive=list_max_length_inclusive,
        )
        self._append_attr(AttrType.AT_PARTY, md, atomic=atomic)

    def _reflect_table_column_attr(self, md: _Metadata):
        is_list, prim_type = self._check_list(md.type)
        if prim_type != str:
            raise CompDeclError(
                f"input_table_attr's type must be str or list[str], but got {md.type}]"
            )

        col_min_cnt_inclusive, col_max_cnt_inclusive = self._build_list_limit(
            is_list, md.list_limit
        )

        atomic = AttributeDef.AtomicAttrDesc(
            list_min_length_inclusive=col_min_cnt_inclusive,
            list_max_length_inclusive=col_max_cnt_inclusive,
        )
        self._append_attr(
            AttrType.AT_COL_PARAMS,
            md,
            atomic=atomic,
            col_params_binded_table=md.input_name,
        )

    def _reflect_attr_field(self, md: _Metadata):
        if md.kind == FieldKind.StructAttr:
            self._reflect_struct(md)
        elif md.kind == FieldKind.UnionAttr:
            self._reflect_union(md)
        elif md.kind == FieldKind.BasicAttr:
            self._reflect_basic(md)
        elif md.kind == FieldKind.CustomAttr:
            self._append_attr(AttrType.AT_CUSTOM, md, pb_cls=md.custom_pb_cls)
        elif md.kind == FieldKind.TableColumnAttr:
            self._reflect_table_column_attr(md)
        elif md.kind == FieldKind.PartyAttr:
            self._reflect_party_attr(md)
        else:
            raise CompDeclError(f"{md.kind} not supported, metadata={md}.")

    def _reflect_struct(self, md: _Metadata):
        self._force_dataclass(md.type)

        self._append_attr(AttrType.AT_STRUCT_GROUP, md)

        prefixes = md.prefixes + [md.name]
        for field in md.type.__dataclass_fields__.values():
            sub_md = self._build_metadata(field, prefixes, md)
            self._reflect_attr_field(sub_md)

    def _reflect_union(self, md: _Metadata):
        assert issubclass(
            md.type, UnionGroup
        ), f"type of {md.name} must be subclass of UnionGroup."

        self._force_dataclass(md.type)

        md.choices = []
        sub_mds = []
        prefixes = md.prefixes + [md.name]
        for field in md.type.__dataclass_fields__.values():
            sub_md: _Metadata = self._build_metadata(field, prefixes, parent=md)
            if not sub_md.is_deprecated:
                md.choices.append(sub_md.name)
            sub_mds.append(sub_md)

        if len(md.choices) == 0:
            raise CompDeclError(f"union {md.name} must have at least one choice.")

        if md.default == "":
            md.default = md.choices[0]
        elif md.default not in md.choices:
            raise CompDeclError(
                f"{md.default} not in {md.choices}, union name is {md.name}"
            )

        union_desc = AttributeDef.UnionAttrGroupDesc(default_selection=md.default)
        self._append_attr(AttrType.AT_UNION_GROUP, md, union=union_desc)

        for sub_md in sub_mds:
            if sub_md.kind == FieldKind.SelectionAttr:
                self._append_attr(AttrType.ATTR_TYPE_UNSPECIFIED, sub_md)
            else:
                self._reflect_attr_field(sub_md)

    def _reflect_basic(self, md: _Metadata):
        is_list, prim_type = self._check_list(md.type)
        attr_type = self._to_attr_type(prim_type, is_list)
        if attr_type == AttrType.ATTR_TYPE_UNSPECIFIED:
            raise CompDeclError(
                f"invalid primative type {prim_type}, name is {md.name}."
            )

        if is_list:
            list_min_length_inclusive, list_max_length_inclusive = (
                self._build_list_limit(True, md.list_limit)
            )
        else:
            list_min_length_inclusive, list_max_length_inclusive = None, None

        # check bound
        lower_bound_enabled = False
        lower_bound_inclusive = False
        lower_bound = None
        upper_bound_enabled = False
        upper_bound_inclusive = False
        upper_bound = None

        if md.bound_limit is not None:
            if prim_type not in [int, float]:
                raise CompDeclError(
                    f"bound limit is not supported for {prim_type}, name is {md.name}."
                )
            if md.choices is not None:
                for v in md.choices:
                    is_valid, err_str = md.bound_limit.check(v)
                    if not is_valid:
                        raise CompDeclError(
                            f"choices of {md.fullname} is valid, {err_str}"
                        )
            if md.bound_limit.lower is not None:
                lower_bound_enabled = True
                lower_bound_inclusive = md.bound_limit.lower_closed
                lower_bound = self._to_attr(md.type(md.bound_limit.lower))
            if md.bound_limit.upper is not None:
                upper_bound_enabled = True
                upper_bound_inclusive = md.bound_limit.upper_closed
                upper_bound = self._to_attr(md.type(md.bound_limit.upper))

        default_value = None
        allowed_values = None
        if md.is_optional and md.default is None:
            raise CompDeclError(f"no default value for optional field, {md.name}")
        if md.default is not None:
            if is_list and not isinstance(md.default, list):
                raise CompDeclError("Default value for list must be a list")

            # make sure the default type is correct
            if not isinstance(md.default, list):
                md.default = md.type(md.default)
            else:
                for idx, v in enumerate(md.default):
                    md.default[idx] = prim_type(md.default[idx])
            if md.choices is not None:
                values = md.default if is_list else [md.default]
                for v in values:
                    if v not in md.choices:
                        raise CompDeclError(
                            f"Default value for {v} must be one of {md.choices}"
                        )
            default_value = self._to_attr(md.default, prim_type)

        if md.choices is not None:
            allowed_values = self._to_attr(md.choices, prim_type)

        atomic = AttributeDef.AtomicAttrDesc(
            default_value=default_value,
            allowed_values=allowed_values,
            is_optional=md.is_optional,
            list_min_length_inclusive=list_min_length_inclusive,
            list_max_length_inclusive=list_max_length_inclusive,
            lower_bound_enabled=lower_bound_enabled,
            lower_bound_inclusive=lower_bound_inclusive,
            lower_bound=lower_bound,
            upper_bound_enabled=upper_bound_enabled,
            upper_bound_inclusive=upper_bound_inclusive,
            upper_bound=upper_bound,
        )
        self._append_attr(attr_type, md, atomic=atomic)

    def _append_attr(
        self,
        typ: str,
        md: _Metadata,
        atomic=None,
        union=None,
        pb_cls=None,
        col_params_binded_table=None,
    ):
        attr = AttributeDef(
            type=typ,
            name=md.name,
            desc=md.desc,
            prefixes=md.prefixes,
            atomic=atomic,
            union=union,
            custom_protobuf_cls=pb_cls,
            col_params_binded_table=col_params_binded_table,
        )
        self._attrs.append(
            _AttrDef(attr=attr, minor_min=md.minor_min, minor_max=md.minor_max)
        )
        if typ not in [AttrType.ATTR_TYPE_UNSPECIFIED, AttrType.AT_STRUCT_GROUP]:
            self._attr_types[md.fullname] = typ

    @staticmethod
    def _check_list(field_type) -> tuple[bool, type]:
        origin = get_origin(field_type)
        if origin is list:
            args = get_args(field_type)
            if not args:
                raise CompDeclError("list must have type.")
            return (True, args[0])
        else:
            return (False, field_type)

    @staticmethod
    def _build_metadata(
        field: DField, prefixes: list[str], parent: _Metadata = None
    ) -> _Metadata:
        if field.name in RESERVED:
            raise CompDeclError(f"{field.name} is a reserved word.")

        assert "md" in field.metadata, f"md not exist in {field.name}, {field.metadata}"
        md: _Metadata = field.metadata["md"]
        md.name = field.name
        md.type = field.type
        md.prefixes = prefixes
        md.fullname = Reflector._to_fullname(prefixes, field.name)

        if parent != None:
            # inherit parent‘s minor_min version if it is zero
            if md.minor_min == 0:
                md.minor_min = parent.minor_min
            elif md.minor_min < parent.minor_min:
                raise CompDeclError(
                    f"minor version of {md.name} must be greater than or equal to {parent.minor_min}"
                )
        return md

    @staticmethod
    def _build_list_limit(is_list: bool, limit: Interval) -> tuple[int, int]:
        if not is_list:
            # limit must be 1 if target type is not list
            return (1, 1)
        if limit is None:
            return (0, -1)

        limit.enforce_closed()
        list_min_length_inclusive = 0
        list_max_length_inclusive = -1
        if limit.lower != None:
            list_min_length_inclusive = int(limit.lower)
        if limit.upper != None:
            list_max_length_inclusive = int(limit.upper)
        return (list_min_length_inclusive, list_max_length_inclusive)

    @staticmethod
    def _to_attr_type(prim_type, is_list) -> str:
        if prim_type is float:
            return AttrType.AT_FLOATS if is_list else AttrType.AT_FLOAT
        elif prim_type is int:
            return AttrType.AT_INTS if is_list else AttrType.AT_INT
        elif prim_type is str:
            return AttrType.AT_STRINGS if is_list else AttrType.AT_STRING
        elif prim_type is bool:
            return AttrType.AT_BOOLS if is_list else AttrType.AT_BOOL
        else:
            return AttrType.ATTR_TYPE_UNSPECIFIED

    @staticmethod
    def _to_attr(v: Any, prim_type: type = None) -> Attribute:  # type: ignore
        is_list = isinstance(v, list)
        if prim_type == None:
            if is_list:
                raise CompDeclError(f"unknown list primitive type for {v}")
            prim_type = type(v)

        if prim_type == bool:
            return Attribute(bs=v) if is_list else Attribute(b=v)
        elif prim_type == int:
            return Attribute(i64s=v) if is_list else Attribute(i64=v)
        elif prim_type == float:
            return Attribute(fs=v) if is_list else Attribute(f=v)
        elif prim_type == str:
            return Attribute(ss=v) if is_list else Attribute(s=v)
        else:
            raise CompDeclError(f"unsupported primitive type {prim_type}")

    @staticmethod
    def _to_fullname(prefixes: list, name: str) -> str:
        if prefixes is not None and len(prefixes) > 0:
            return '/'.join(prefixes) + '/' + name
        else:
            return name

    @staticmethod
    def _force_dataclass(cls):
        if "__dataclass_params__" not in cls.__dict__:
            dataclass(cls)


class Definition:
    def __init__(
        self,
        cls: type[Component],
        domain: str,
        version: str,
        name: str = "",
        desc: str = None,
    ):
        if not issubclass(cls, Component):
            raise CompDeclError(f"{cls} must be subclass of Component")

        if name == "":
            name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

        if desc is None:
            desc = cls.__doc__ if cls.__doc__ is not None else ""

        versions = version.split(".")
        assert len(versions) == 3, "version must be in format of x.y.z"

        self.name = name
        self.domain = domain
        self.version = version

        self._minor = int(versions[1])

        r = Reflector(cls, self.name, self._minor)
        self._comp_def = ComponentDef(
            name=self.name,
            desc=_clean_text(desc),
            domain=self.domain,
            version=self.version,
            inputs=r.build_inputs(),
            outputs=r.build_outputs(),
            attrs=r.build_attrs(),
        )
        self._inputs: list[_IoDef] = r._inputs
        self._outputs: list[_IoDef] = r._outputs
        self._attrs: list[_AttrDef] = r._attrs
        self._attr_types = r._attr_types
        self._comp_cls = cls

    def __str__(self) -> str:
        return json_format.MessageToJson(self._comp_def, indent=0)

    @property
    def component_def(self) -> ComponentDef:  # type: ignore
        return self._comp_def

    @property
    def inputs(self) -> list[IoDef]:  # type: ignore
        return self._comp_def.inputs

    @property
    def outputs(self) -> list[IoDef]:  # type: ignore
        return self._comp_def.outputs

    @property
    def attrs(self) -> list[AttributeDef]:  # type: ignore
        return self._comp_def.attrs

    def make_component(self, param: NodeEvalParam | dict, check_exist: bool = True) -> type[Component]:  # type: ignore
        if isinstance(param, NodeEvalParam):
            version = param.version.split('.')
            minor = int(version[1])
            kwargs = self._parse_param(param, minor)
        elif isinstance(param, dict):
            minor_name = MINOR_NAME
            assert minor_name in param, f"param must contain {minor_name}"
            minor = param.pop(minor_name)
            kwargs = {}
            for k, v in param.items():
                k = Definition._trim_input_prefix(k)
                kwargs[k] = v
        else:
            raise ValueError(f"unsupported param type {type(param)}")
        creator = Creator(check_exist=check_exist)
        ins = creator.make(self._comp_cls, kwargs, minor)
        return ins

    def get_outputs(self, comp_inst) -> list[DistData]:  # type: ignore
        outputs = []
        minor = getattr(comp_inst, MINOR_NAME)
        for io in self._outputs:
            if minor > io.minor_min:
                break
            if io.is_deprecated and minor > io.minor_max:
                continue
            out = getattr(comp_inst, io.name)
            assert isinstance(out, Output), f"type of output should be Output"
            assert out.data is not None, f"output {io.name} must be not None"
            assert (
                out.data.type in io.io.types
            ), f"DistData type must be in {io.io.types}, but got {out.data.type}"
            outputs.append(out.data)

        return outputs

    def _parse_param(self, param: NodeEvalParam, minor: int) -> dict:  # type: ignore
        attrs = self._parse_attrs(param)

        assert all(
            isinstance(item, DistData) for item in param.inputs
        ), f"type of inputs must be DistData"
        assert all(
            isinstance(item, str) for item in param.output_uris
        ), f"type of output_uris must be str"

        def parse_io(io_defs: list[_IoDef], datas: list) -> dict:
            result = {}
            idx = -1
            for io in io_defs:
                if minor > io.minor_min:
                    continue
                if io.is_deprecated and minor > io.minor_max:
                    continue
                idx += 1
                assert idx < len(datas), f"miss io data, {datas}"
                result[io.name] = datas[idx]

            assert len(result) == len(
                datas
            ), f"invalid io size, excepted {len(datas)} but got {len(result)}"
            return result

        inputs = parse_io(self._inputs, param.inputs)
        output_uris = parse_io(self._outputs, param.output_uris)
        outputs = {k: Output(uri=uri, data=None) for k, uri in output_uris.items()}
        return {**attrs, **inputs, **outputs}

    def _parse_attrs(self, param: NodeEvalParam) -> dict:  # type: ignore
        attrs = {}
        for path, attr in zip(list(param.attr_paths), list(param.attrs)):
            path = Definition._trim_input_prefix(path)
            if path not in self._attr_types:
                raise ValueError(f"unknown attr key {path}, {self._attrs.keys()}")
            at = self._attr_types[path]
            attrs[path] = self._from_attr(attr, at)
        return attrs

    def make_checkpoint(self, param: NodeEvalParam) -> Checkpoint:  # type: ignore
        checkpoint_uri = param.checkpoint_uri
        if not checkpoint_uri or checkpoint_uri == "":
            return None

        parties = set()
        for input in param.inputs:
            assert isinstance(input, DistData)
            for dr in input.data_refs:
                parties.add(dr.party)
        assert len(parties) > 0

        version = param.version.split('.')
        minor = int(version[1])

        attrs = self._parse_attrs(param)

        args = {}
        cls = self._comp_cls
        for name, field in cls.__dataclass_fields__.items():
            if name == MINOR_NAME:
                continue
            md: _Metadata = field.metadata['md']
            if md.kind != FieldKind.BasicAttr and md.kind != FieldKind.TableColumnAttr:
                continue
            if md.is_deprecated_minor(minor) or not md.is_checkpoint:
                continue

            args[md.fullname] = (
                attrs[md.fullname] if md.fullname in attrs else md.default
            )

        return Checkpoint(checkpoint_uri, args, sorted(list(parties)))

    @staticmethod
    def _trim_input_prefix(p: str) -> str:
        if p.startswith("input/"):
            tokens = p.split('/', maxsplit=3)
            assert len(tokens) == 3, f"invalid input, {p}"
            return tokens[2]
        return p

    @staticmethod
    def _from_attr(value: Attribute, at: AttrType) -> Any:  # type: ignore
        if at == AttrType.ATTR_TYPE_UNSPECIFIED:
            raise ValueError("Type of Attribute is undefined.")
        elif at == AttrType.AT_FLOAT:
            return value.f
        elif at == AttrType.AT_INT:
            return value.i64
        elif at == AttrType.AT_STRING:
            return value.s
        elif at == AttrType.AT_BOOL:
            return value.b
        elif at == AttrType.AT_FLOATS:
            return list(value.fs)
        elif at == AttrType.AT_INTS:
            return list(value.i64s)
        elif at == AttrType.AT_BOOLS:
            return list(value.bs)
        elif at == AttrType.AT_CUSTOM_PROTOBUF:
            return value.s
        elif at == AttrType.AT_UNION_GROUP:
            return value.s
        elif at in [AttrType.AT_STRINGS, AttrType.AT_PARTY, AttrType.AT_COL_PARAMS]:
            return list(value.ss)
        elif at == AttrType.AT_STRUCT_GROUP:
            raise ValueError(f"AT_STRUCT_GROUP should be ignore")
        else:
            raise ValueError(f"unsupported type: {at}.")
