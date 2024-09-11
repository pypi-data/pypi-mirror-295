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

from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

from brick.data.abbreviations import STD_ABBREVIATIONS
from brick.data.config.parameter import (
    DOC_ELM_SPLITABLE_PRMS,
    OUTPUT_PARAMETERS,
    # PARAMETER_FUNCTION_MARKER,
    # PARAMETER_PATH_MARKER,
    # PARAMETER_RANGE_MARKER,
    PARAMETER_UID_SEPARATOR,
    PARAMETER_WORD_SEPARATOR,
    PATH_PARAMETERS,
)
from brick.data.config.specification import (
    CONFIG_SPECIFICATION,
    PARAMETER_RANGE_SUFFIX,
    missing_required_value_t,
)
from brick.data.config.specification import parameter_t as static_parameter_t
from brick.data.config.std_labels import std_label_e
from brick.data.config.type import pl_path_t, text_t, tuple_t
from brick.data.config.unit import UNIT_SEPARATOR


def _ParameterUId(sct_label: Union[str, std_label_e], name: str, separator: str) -> str:
    #
    if isinstance(sct_label, str):
        sct_part = sct_label
    else:
        sct_part = sct_label.value

    return f"{sct_part}{separator}{name}"


# TODO: Add comment to explain why parameter_t is not a subclass of static_parameter_t
class parameter_t:

    PARAMETER_WORD_SEPARATOR: ClassVar[str] = PARAMETER_WORD_SEPARATOR
    PARAMETER_UID_SEPARATOR: ClassVar[str] = PARAMETER_UID_SEPARATOR

    # PARAMETER_RANGE_MARKER: ClassVar[str] = PARAMETER_RANGE_MARKER
    # PARAMETER_PATH_MARKER: ClassVar[str] = PARAMETER_PATH_MARKER
    # PARAMETER_FUNCTION_MARKER: ClassVar[str] = PARAMETER_FUNCTION_MARKER

    OUTPUT_PARAMETERS: ClassVar[Tuple[str, ...]] = tuple(
        _ParameterUId(_sct, _nme, PARAMETER_UID_SEPARATOR)
        for _sct, _nme in OUTPUT_PARAMETERS
    )
    DOC_ELM_SPLITABLE_PRMS: ClassVar[
        Dict[str, Tuple[std_label_e, str]]
    ] = DOC_ELM_SPLITABLE_PRMS
    PATH_PARAMETERS: ClassVar[Tuple[Tuple[std_label_e, str]]] = PATH_PARAMETERS

    # name: INI-configuration name; Must respect Python identifier constraints
    # formatted_name: version of "name" that can be used in interfaces
    # comment: user-defined description provided in INI configuration document
    __slots__ = static_parameter_t.__slots__ + (
        "UId",
        "formatted_name",
        "spec_type",
        "python_type",
        "obj_mpp_type",
        "value",
        "unit",
        "comment",
    )

    UId: str
    formatted_name: str
    value: Any
    unit: str
    comment: str

    def __init__(self):
        """"""
        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in parameter_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def FromSpecification(
        cls, specification: static_parameter_t, section: std_label_e
    ) -> parameter_t:
        """"""
        instance = cls()

        for field in static_parameter_t.__slots__:
            setattr(instance, field, getattr(specification, field))

        instance.UId = cls.ParameterUId(section, specification.name)
        instance.formatted_name = FormattedName(
            instance.name, cls.PARAMETER_WORD_SEPARATOR
        )
        instance._SetTypes(instance.default)
        instance.value = instance.default

        return instance

    @classmethod
    def FromUntypedEntry(
        cls,
        name: str,
        value: str,
        comment_marker: str,
        section: std_label_e,
    ) -> parameter_t:
        """"""
        comment_start = value.find(comment_marker)
        if comment_start != -1:
            value = value[:comment_start].strip()
            comment = value[(comment_start + 1) :].strip()
            if comment.__len__() == 0:
                comment = None
        else:
            comment = None

        specification = _SpecificationFromNameAndSection(name, section)
        if specification is None:
            instance = cls._ForValueLessProgrammaticEntry(name, section)
        else:
            instance = cls.FromSpecification(specification, section)
        instance.SetTypesAndValueFromString(value)
        instance.comment = comment

        return instance

    @classmethod
    def ForProgrammaticEntry(
        cls,
        name: str,
        value: Any,
        section: std_label_e,
    ) -> parameter_t:
        """"""
        instance = cls._ForValueLessProgrammaticEntry(name, section)
        instance._SetTypes(value)
        instance.value = value

        return instance

    @classmethod
    def _ForValueLessProgrammaticEntry(
        cls,
        name: str,
        section: std_label_e,
    ) -> parameter_t:
        """"""
        section_spec = CONFIG_SPECIFICATION[section][0]
        specification = static_parameter_t(
            name=name,
            definition="Programmatic Entry",
            description="",
            basic=section_spec.basic,
            optional=section_spec.optional,
            types=(None, object),
            default=None,
        )
        instance = cls.FromSpecification(specification, section)
        # instance.SetValueFromString(value, unit_conversions=unit_conversions)

        return instance

    def SetTypesAndValueFromString(
        self,
        value_w_unit: Optional[str],
    ) -> None:
        """"""
        if (value_w_unit is None) or (value_w_unit.__len__() == 0):
            value = None
            unit = None
        else:
            value_as_str, unit = _ValueAsStringAndUnit(self.name, value_w_unit)
            try:
                value = eval(value_as_str)
            except (SyntaxError, NameError):
                value = value_as_str

        self._SetTypes(value)
        self.value = value
        self.unit = unit

    def _SetTypes(self, value: Any) -> None:
        """"""
        non_none_types = self.types[int(self.types[0] is None) :]

        if value is None:
            spec_type = non_none_types[0]
            python_type = getattr(spec_type, "python_type", spec_type)
            obj_mpp_type = getattr(spec_type, "obj_mpp_type", python_type)
        elif isinstance(value, missing_required_value_t):
            # Cannot be None according to specification (/!\ future changes)
            spec_type = value.MainType()
            python_type = getattr(spec_type, "python_type", spec_type)
            obj_mpp_type = getattr(spec_type, "obj_mpp_type", python_type)
        else:
            spec_type = None
            python_type = type(value)
            obj_mpp_type = python_type
            if obj_mpp_type is tuple:
                for type_ in non_none_types:
                    if isinstance(type_, tuple_t):
                        spec_type = type_
                        obj_mpp_type = type_.obj_mpp_type
                        break
            elif obj_mpp_type in (str, pl_path_t):
                for type_ in non_none_types:
                    if isinstance(type_, text_t):
                        spec_type = type_
                        obj_mpp_type = type_.obj_mpp_type
                        break
            if spec_type is None:
                spec_type = python_type

        # if isinstance(obj_mpp_type, numeric_t):
        #     obj_mpp_type = obj_mpp_type.type
        # elif (obj_mpp_type is str) or isinstance(value, pl_path_t):
        #     for type_ in non_none_types:
        #         if isinstance(type_, text_t):
        #             obj_mpp_type = type_.obj_mpp_type
        #             break
        # elif obj_mpp_type is tuple:
        #     for type_ in non_none_types:
        #         if isinstance(type_, tuple_t):
        #             obj_mpp_type = type_
        #             break
        # elif isinstance(obj_mpp_type, text_t):
        #     obj_mpp_type = obj_mpp_type.obj_mpp_type

        self.spec_type = spec_type
        self.python_type = python_type
        self.obj_mpp_type = obj_mpp_type

    def EducatedValueAndTypes(self) -> Tuple[Any, Any, type, Any, Tuple[Any, ...]]:
        """"""
        # The value is always set, but it can be the default one
        value = self.value
        non_none_types = self.types[int(self.types[0] is None) :]

        if self.obj_mpp_type is tuple_t.MARK_INTERVAL:
            if (value is not None) and (value.__len__() < 3):
                value = (*value, 0.0)  # Adding infinite precision

        return value, self.spec_type, self.python_type, self.obj_mpp_type, non_none_types

    @classmethod
    def ParameterUId(cls, sct_label: Union[str, std_label_e], name: str) -> str:
        #
        return _ParameterUId(sct_label, name, cls.PARAMETER_UID_SEPARATOR)

    @classmethod
    def SectionAndParameterFromUId(cls, parameter_uid: str) -> List[str]:
        """
        It is assumed that the UId is valid: no test performed.
        """
        return parameter_uid.split(cls.PARAMETER_UID_SEPARATOR)

    def IsAnOutput(self) -> bool:
        """"""
        return self.UId in self.__class__.OUTPUT_PARAMETERS

    def __str__(self) -> str:
        """"""
        output = [self.__class__.__name__]

        for slot in self.__slots__:
            output.append(f"    {slot}: {getattr(self, slot)}")

        return "\n".join(output)


def FormattedName(name: Union[str, std_label_e], separator: str) -> str:
    #
    if isinstance(name, std_label_e):
        name = name.value

    name_cmps = []
    for component in name.split(separator):
        name_cmps.append(STD_ABBREVIATIONS.get(component, component))

    return " ".join(name_cmps).capitalize()


def _ValueAsStringAndUnit(name: str, value_w_unit: str) -> Tuple[str, Optional[str]]:
    #
    unit = None

    check_unit = name.endswith(PARAMETER_RANGE_SUFFIX)
    if check_unit:
        separator_idx = value_w_unit.rfind(UNIT_SEPARATOR)
        if separator_idx != -1:
            value = value_w_unit[:separator_idx]
            unit = value_w_unit[(separator_idx + 1) :].strip()
        else:
            value = value_w_unit

        # if value_w_unit[-2:] in STD_UNIT_ABBREVIATIONS:
        #     unit = value_w_unit[-2:]
        # elif value_w_unit[-1:] in STD_UNIT_ABBREVIATIONS:
        #     unit = value_w_unit[-1:]
        #
        # if unit is None:
        #     value = value_w_unit
        # else:
        #     value = value_w_unit[: -unit.__len__()]
    else:
        value = value_w_unit

    # print(name, value_w_unit, value, unit)
    # import inspect
    # stack = inspect.stack(context=1)
    # for step in stack:
    #     print("    ", step.function)

    return value, unit


def _SpecificationFromNameAndSection(
    name: str, section: std_label_e
) -> Optional[static_parameter_t]:
    #
    for output in CONFIG_SPECIFICATION[section][1:]:
        if output.name == name:
            return output

    # The configuration should have been validated, so this can only happen for parameters of optional sections
    # dedicated to non-standard parameters such as mark ranges or quality parameters.
    return None

    # def IsRange(self) -> bool:
    #     """"""
    #     return _ParameterIs(self.formatted_name, self.__class__.PARAMETER_RANGE_MARKER)

    # def IsPath(self) -> bool:
    #     """"""
    #     return _ParameterIs(self.formatted_name, self.__class__.PARAMETER_PATH_MARKER)

    # def IsFunction(self) -> bool:
    #     """"""
    #     return _ParameterIs(
    #         self.formatted_name, self.__class__.PARAMETER_FUNCTION_MARKER
    #     )

    # def IsMarkedPointType(self) -> bool:
    #     """"""
    #     return self.name == "object_type"

    # def IsMarkedPointQuality(self) -> bool:
    #     """"""
    #     return self.name == "object_quality"


# def _ParameterIs(formatted_name: str, what: str) -> bool:
#     """"""
#     return (
#         re_.search(r"\b" + what + r"\b", formatted_name, flags=re_.IGNORECASE)
#         is not None
#     )
