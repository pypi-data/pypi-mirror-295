# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2018)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

from collections import namedtuple as namedtuple_t
from typing import Any, ClassVar, Dict, Sequence, Tuple, Union

from brick.data.type import pl_path_t
from brick.marked_point.generic import marked_point_t
from brick.quality.generic import quality_env_t


# These types are defined for standardization of the specification, They are not functional. Functional versions, if
# needed, should be defined in modules written in brick/config folder. Note that functional types cannot be defined
# alone since they require the specification, while the specification would require them also (circular import).
section_t = namedtuple_t("section_t", "category definition description basic optional")
# parameter_t = namedtuple_t(
#     "parameter_t", "name definition description basic optional types default"
# )
# class section_t:
#
#     __slots__ = ("category", "definition", "description", "basic", "optional")


class parameter_t:

    __slots__ = (
        "name",
        "definition",
        "description",
        "basic",
        "optional",
        "types",
        "default",
    )

    name: str
    definition: str
    description: str
    basic: bool
    optional: bool
    types: tuple  # Can be Python types or types declared here
    default: Any

    def __init__(self, **kwargs):
        """"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def AsDict(self) -> Dict[str, Any]:
        """"""
        return {_fld: getattr(self, _fld) for _fld in self.__class__.__slots__}


number_h = Union[int, float]


class numeric_t:

    INTEGER: ClassVar[type] = int
    FLOAT: ClassVar[type] = float
    INFINITY_NEG: ClassVar[float] = -float("inf")
    INFINITY_POS: ClassVar[float] = float("inf")
    INFINITE_PRECISION: ClassVar[float] = 0.0

    __slots__ = ("python_type", "min", "min_inclusive", "max", "max_inclusive", "precision")

    python_type: type  # int or float
    min: number_h
    min_inclusive: bool
    max: number_h
    max_inclusive: bool
    precision: number_h

    def __init__(
        self,
        python_type: type = None,
        min_: number_h = INFINITY_NEG,
        max_: number_h = INFINITY_POS,
        precision: number_h = INFINITE_PRECISION,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
    ):
        """"""
        if python_type is None:
            if min_ != self.__class__.INFINITY_NEG:
                python_type = type(min_)
            if (python_type is None) and (max_ != self.__class__.INFINITY_POS):
                python_type = type(max_)
            elif python_type is None:
                raise ValueError("Numeric parameter without identifiable type")
            elif (max_ != self.__class__.INFINITY_POS) and not isinstance(max_, python_type):
                raise ValueError(f"{min_}/{max_}: Type mismatch {python_type}/{type(max_)}")
        elif (min_ != self.__class__.INFINITY_NEG) and not isinstance(min_, python_type):
            raise ValueError(
                f"{min_}: Minimum with invalid type; Actual={type(min_)}, Expected={python_type}"
            )
        elif (max_ != self.__class__.INFINITY_POS) and not isinstance(max_, python_type):
            raise ValueError(
                f"{max_}: Maximum with invalid type; Actual={type(max_)}, Expected={python_type}"
            )
        # Assumed True
        # if python_type not in (int, float):
        #     raise ValueError(f"{python_type}: Invalid type; Expected=int or float")
        if python_type is int:
            if precision == self.__class__.INFINITE_PRECISION:
                precision = 1
            elif not isinstance(precision, int):
                raise ValueError(
                    f"{precision}: Precision with invalid type; Actual={type(precision)}, Expected=int"
                )

        self.python_type = python_type
        self.min = min_
        self.max = max_
        self.precision = precision
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def __str__(self) -> str:
        """"""
        if self.python_type is int:
            python_type = "Integer"
        else:
            python_type = "Floating-point number"

        if self.min == self.__class__.INFINITY_NEG:
            min_ = ""
        else:
            if self.min_inclusive:
                inclusiveness = ""
            else:
                inclusiveness = " (excluded)"
            min_ = f" from {self.min}{inclusiveness}"

        if self.max == self.__class__.INFINITY_POS:
            max_ = ""
        else:
            if self.max_inclusive:
                inclusiveness = ""
            else:
                inclusiveness = " (excluded)"
            max_ = f" to {self.max}{inclusiveness}"

        if ((self.python_type is int) and (self.precision != 1)) or (
            (self.python_type is float) and (self.precision != self.__class__.INFINITE_PRECISION)
        ):
            precision = f" with a precision of {self.precision}"
        else:
            precision = ""

        return f"{python_type}{min_}{max_}{precision}"


class tuple_t:

    GENERIC: ClassVar[str] = "Generic"
    NUMERIC: ClassVar[str] = "Numeric"
    MARK_INTERVAL: ClassVar[str] = "Mark interval"
    DOMAIN_REGION: ClassVar[str] = "Domain region"
    SUBTYPES: ClassVar[Tuple[str, ...]] = (
        GENERIC,
        NUMERIC,
        MARK_INTERVAL,
        DOMAIN_REGION,
    )

    __slots__ = ("lengths", "python_type", "obj_mpp_type")

    lengths: Tuple[int, ...]
    python_type: type
    obj_mpp_type: str  # Among tuple_t.SUBTYPES

    def __init__(self, lengths: Union[int, Sequence[int]], obj_mpp_type: str = GENERIC):
        """"""
        if isinstance(lengths, int):
            self.lengths = (lengths,)
        else:
            self.lengths = tuple(sorted(lengths))
        self.python_type = tuple
        self.obj_mpp_type = obj_mpp_type

    @property
    def __name__(self) -> str:
        """"""
        return "tuple"


class _path_document_t(pl_path_t):
    pass


class _path_folder_t(pl_path_t):
    pass


class _path_any_t(pl_path_t):
    pass


def _function():
    pass


class text_t:

    PATH_DOCUMENT: ClassVar[type] = _path_document_t
    PATH_FOLDER: ClassVar[type] = _path_folder_t
    PATH_ANY: ClassVar[type] = _path_any_t
    PATH_OPTIONS: ClassVar[Tuple[type,...]] = (PATH_DOCUMENT, PATH_FOLDER, PATH_ANY)
    MARKED_POINT: ClassVar[type] = marked_point_t
    QUALITY: ClassVar[type] = quality_env_t
    FUNCTION: ClassVar[type] = type(_function)

    __slots__ = ("python_type", "obj_mpp_type")

    python_type: type
    obj_mpp_type: type  # Among text_t fields, expect PATH_OPTIONS

    def __init__(self, obj_mpp_type: type):
        """"""
        if obj_mpp_type in self.__class__.PATH_OPTIONS:
            self.python_type = pl_path_t
        else:
            self.python_type = str
        self.obj_mpp_type = obj_mpp_type

    @classmethod
    def IsPlainPath(cls, obj_mpp_type: type) -> bool:
        """
        As opposed to standard element or "path_to_document:element_in_document".
        Do not use isinstance(obj_mpp_type, pl_path_t) since PosixPath is not
        """
        return obj_mpp_type in cls.PATH_OPTIONS

    @property
    def __name__(self) -> str:
        """"""
        return "str"


missing_value_type_h = Union[type, text_t, tuple_t]


class missing_required_value_t:

    __slots__ = ("types",)

    types: Tuple[missing_value_type_h, ...]  # Can be Python types or types declared here

    def __init__(
        self, types: Union[missing_value_type_h, Sequence[missing_value_type_h]] = None
    ):
        """"""
        if types is not None:
            self.SetTypes(types)

    def SetTypes(
        self, types: Union[missing_value_type_h, Sequence[missing_value_type_h]]
    ) -> None:
        """"""
        if isinstance(types, Sequence):
            self.types = tuple(types)
        else:
            self.types = (types,)

        if None in self.types:
            raise ValueError(
                f"{self.types}: None among possible types of required value; Invalid specification"
            )

    def MainType(self) -> type:
        """"""
        return self.types[0]

    def __str__(self) -> str:
        """"""
        if self.types.__len__() > 1:
            types_as_str = " among: " + ", ".join(_typ.__name__ if isinstance(_typ, type) else _typ.__class__.__name__ for _typ in self.types)
        elif isinstance(self.types[0], type):
            types_as_str = ": " + self.types[0].__name__
        else:
            types_as_str = ": " + self.types[0].__class__.__name__

        return f"REQUIRED VALUE with TYPE{types_as_str}"
