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

import argparse as ap_
from enum import Enum as enum_t
from typing import Any, Callable, ClassVar, Dict, List, Optional, Sequence, Tuple, Union

import brick.interface.io.reporting as rp_
from brick.config.parameter import parameter_t
from brick.config.section import SectionLabelFromName, section_t
from brick.data.config.specification import (
    CONFIG_SPECIFICATION,
    missing_required_value_t,
)
from brick.data.config.specification import parameter_t as static_parameter_t
from brick.data.config.specification import section_t as static_section_t
from brick.data.config.std_labels import std_label_e
from brick.data.type import pl_path_t


# noinspection PyArgumentList
config_completeness_e = enum_t("config_completeness_e", "MINIMAL BASIC FULL")
# MINIMAL: everything that has no default value
# BASIC: everything tagged as basic in the specification
# FULL: everything, surprisingly


raw_config_h = Dict[std_label_e, Dict[str, Any]]
light_config_h = Dict[std_label_e, Sequence[parameter_t]]


class config_t(dict):

    INI_DEFAULT_SECTION: ClassVar[str] = "DEFAULT"
    INI_VALUE_ASSIGNEMENT: ClassVar[str] = "="
    INI_MOD_ELM_SEPARATOR: ClassVar[str] = ":"
    INI_COMMENT_MARKER: ClassVar[str] = "#"
    # On the command line, specify INI document file with option --ini_document INI_document_path
    INI_DOCUMENT_OPTION: ClassVar[str] = "ini_document"

    # dict as a __dict__, so __slots__ here is meaningless
    _slots = ("ini_document", "has_default_value", "issues")

    ini_document: pl_path_t
    has_default_value: Tuple[str, ...]
    issues: List[str, ...]

    def __init__(self):
        #
        super().__init__()
        for slot in config_t._slots:
            setattr(self, slot, None)

        self.issues = []

    @classmethod
    def Standard(cls, completeness: config_completeness_e) -> config_t:
        #
        instance = cls()

        for section_name, section_elements in CONFIG_SPECIFICATION.items():
            static_section = section_elements[0]
            static_parameters = section_elements[1:]

            if not _SectionMatchesCompleteness(static_section, completeness):
                continue

            parameters = []
            n_parameters = 0
            n_basic_prms = 0
            for static_parameter in static_parameters:
                n_parameters += 1
                if static_parameter.basic:
                    n_basic_prms += 1

                if _ParameterMatchesCompleteness(static_parameter, completeness):
                    parameter = parameter_t.FromSpecification(
                        static_parameter, section_name
                    )
                    parameters.append(parameter)

            section = section_t.FromSpecification(
                section_name, static_section, parameters
            )
            instance[section_name] = section

        return instance

    @classmethod
    def NewEmpty(cls, ini_document: Union[str, pl_path_t] = None) -> config_t:
        """"""
        instance = cls()

        if ini_document is not None:
            if isinstance(ini_document, str):
                ini_document = pl_path_t(ini_document)
            instance.ini_document = ini_document

        return instance

    @classmethod
    def NewFromRawVersion(
        cls,
        GetRawConfig: Callable[[Any], raw_config_h],
        from_file: Union[str, pl_path_t] = None,
        arguments: Union[Dict[str, str], ap_.Namespace] = None,
    ) -> Tuple[Optional[config_t], bool, Optional[light_config_h]]:
        """"""
        if from_file is None:
            instance = cls.Standard(config_completeness_e.FULL)
        else:
            raw_config = GetRawConfig(from_file)
            if raw_config is None:
                return None, False, None
            instance = cls.NewEmpty(ini_document=from_file)
            instance.SetFromRawConfig(raw_config)
            instance.AddDefaults()

        if arguments is not None:
            instance.OverwriteWithCommandLineArguments(arguments)

        # print("--------------- CONFIG INSTANCE")
        # for key, values in instance.items():
        #     for value in values:
        #         print("    ", value)
        config_is_valid, for_deferred_check = instance.Validity()
        instance.Finalize()

        return instance, config_is_valid, for_deferred_check

    def SetFromRawConfig(self, raw_config: raw_config_h) -> None:
        """"""
        for sct_name, sct_prms in raw_config.items():
            if sct_name == self.__class__.INI_DEFAULT_SECTION:
                continue

            std_sct_name = SectionLabelFromName(sct_name)
            if std_sct_name is None:
                rp_.ReportIP(sct_name.value, "section", section_t.VALID_SECTION_NAMES)
                self.issues.append(
                    f"{sct_name}: Section {section_t.VALID_SECTION_NAMES}"
                )  # TODO: Adjust message
                continue
            sct_name = std_sct_name

            parameters = []
            for p_idx, (prm_name, prm_value_as_str) in enumerate(sct_prms.items()):
                parameter = parameter_t.FromUntypedEntry(
                    prm_name,
                    prm_value_as_str,
                    self.__class__.INI_COMMENT_MARKER,
                    sct_name,
                )
                parameters.append(parameter)

            section = section_t.FromSpecification(
                sct_name, CONFIG_SPECIFICATION[sct_name][0], parameters
            )
            self[sct_name] = section

    def AddDefaults(self) -> None:
        #
        has_default_value = []
        default_config = self.__class__.Standard(config_completeness_e.FULL)
        for default_section in default_config.values():
            section_name = default_section.name
            if section_name in self:
                section = self[section_name]
                for parameter in default_section:
                    if section.ParameterWithName(parameter.name) is None:
                        section.append(parameter)
                        has_default_value.append(parameter.UId)
            else:
                self[section_name] = default_section
                has_default_value.extend(_prm.UId for _prm in default_section)

        self.has_default_value = tuple(has_default_value)

    def OverwriteWithCommandLineArguments(
        self, arguments: Union[Dict[str, str], ap_.Namespace]
    ) -> None:
        #
        if isinstance(arguments, ap_.Namespace):
            arguments = vars(arguments)
            del arguments[self.__class__.INI_DOCUMENT_OPTION]

        for prm_uid, value in arguments.items():
            if not isinstance(value, missing_required_value_t):
                sct_name, prm_name = parameter_t.SectionAndParameterFromUId(prm_uid)
                # It would be better to include the SectionLabelFromName call in SectionAndParameterFromUId, but this
                # cannot be done easily without circular imports.
                sct_name = SectionLabelFromName(sct_name)
                section = self[sct_name]
                parameter = section.ParameterWithName(prm_name)
                if parameter is None:
                    parameter = parameter_t.FromUntypedEntry(
                        prm_name, value, self.__class__.INI_COMMENT_MARKER, sct_name
                    )
                    section.append(parameter)
                else:
                    parameter.SetTypesAndValueFromString(value)

    def Finalize(self) -> None:
        #
        if self.ini_document is None:
            ini_doc_folder = None
        else:
            ini_doc_folder = self.ini_document.parent

        unit_conversions = {
            _prm.name: _prm.value for _prm in self[std_label_e.sct_range_units]
        }
        for section in self.values():
            for parameter in section:
                value = parameter.value
                unit = parameter.unit
                if unit is not None:
                    conversion_factor = unit_conversions.get(unit)
                    if conversion_factor is None:
                        self.issues.append(
                            f'{section.name.value}.{parameter.name}: Has undefined unit "{unit}"'
                        )
                    elif conversion_factor != 1.0:
                        if isinstance(value, Sequence):
                            converted_value = tuple(
                                conversion_factor * _val for _val in value
                            )
                        else:
                            converted_value = conversion_factor * value
                        parameter.value = converted_value

        for sct_name, prm_name in parameter_t.PATH_PARAMETERS:
            parameter = self[sct_name].ParameterWithName(prm_name)
            if (parameter is None) or (parameter.value is None):
                continue

            # Some parameters can be a range or a path to an image for example; Hence type must be tested.
            if isinstance(parameter.value, str):
                if parameter.value.__len__() > 0:
                    value = pl_path_t(parameter.value)
                else:
                    value = None
            else:
                value = parameter.value
            if isinstance(value, pl_path_t):
                if (ini_doc_folder is not None) and not value.is_absolute():
                    value = (ini_doc_folder / value).resolve()
                parameter.value = value
            elif value is None:
                parameter.value = value

        # for prm_name, (
        #     sct_name,
        #     doc_prm_name,
        # ) in parameter_t.DOC_ELM_SPLITABLE_PRMS.items():
        #     section = self[sct_name]
        #     parameter = section.ParameterWithName(prm_name)
        #     if (parameter is not None) and isinstance(parameter.value, str):
        #         document, element = _SplittedDocumentAndElement(parameter.value)
        #         parameter.value = element
        #         split_prm = parameter_t.ForProgrammaticEntry(
        #             doc_prm_name, document, sct_name
        #         )
        #         section.append(split_prm)

    def Validity(self) -> Tuple[bool, light_config_h]:
        #
        is_valid = True
        for_deferred_check = {}

        for section in self.values():
            # section_name in CONFIG_SPECIFICATION: necessarily true; see FromINIDocument
            section_name = section.name
            if CONFIG_SPECIFICATION[section_name].__len__() > 1:
                valid_parameters = tuple(
                    _prm.name for _prm in CONFIG_SPECIFICATION[section_name][1:]
                )

                for parameter in section:
                    if parameter.name not in valid_parameters:
                        rp_.ReportIP(
                            parameter.name,
                            f"parameter in [{section_name}]",
                            valid_parameters,
                        )
                        is_valid = False
                    elif isinstance(parameter.value, missing_required_value_t):
                        # print("--------- IN CONFIG")
                        rp_.ReportE(
                            f"[{section_name}] {parameter.name}",
                            "Missing required parameter",
                        )
                        is_valid = False
            else:
                # Skip section with optional-only parameters (parameters of external functions, although some are
                # provided by Obj.MPP). The parameters must be checked later on (e.g. by CheckPassedParameters).
                for_deferred_check[section_name] = section

        return is_valid, for_deferred_check

    def AsRawDict(self) -> raw_config_h:
        """"""
        output = {_key: _val.AsDict() for _key, _val in self.items()}

        for prm_name, (
            sct_name,
            doc_prm_name,
        ) in parameter_t.DOC_ELM_SPLITABLE_PRMS.items():
            if (sct_name in output) and (prm_name in output[sct_name]):
                parameter = output[sct_name][prm_name]
                if isinstance(parameter, str):
                    document, element = _SplittedDocumentAndElement(parameter)
                    output[sct_name][prm_name] = element
                    output[sct_name][doc_prm_name] = document

        return output


def _SectionMatchesCompleteness(
    section: static_section_t, completeness: config_completeness_e
) -> bool:
    """"""
    return (
        (completeness == config_completeness_e.FULL)
        or ((completeness == config_completeness_e.BASIC) and section.basic)
        or ((completeness == config_completeness_e.MINIMAL) and not section.optional)
    )


def _ParameterMatchesCompleteness(
    parameter: static_parameter_t, completeness: config_completeness_e
) -> bool:
    """"""
    return (
        (completeness == config_completeness_e.FULL)
        or ((completeness == config_completeness_e.BASIC) and parameter.basic)
        or (
            (completeness == config_completeness_e.MINIMAL)
            and isinstance(parameter.default, missing_required_value_t)
        )
    )


def _SplittedDocumentAndElement(value: str) -> Tuple[str, str]:
    #
    if config_t.INI_MOD_ELM_SEPARATOR in value:
        components = value.split(config_t.INI_MOD_ELM_SEPARATOR)
        document = "".join(components[:-1])
        element = components[-1]

        if document.__len__() > 0:
            document = pl_path_t(document)
        else:
            document = None
    else:
        document = None
        element = value

    return document, element


def CheckSpecificationValidity() -> None:
    #
    issues = []

    for section_name, section_elements in CONFIG_SPECIFICATION.items():
        static_section = section_elements[0]
        static_parameters = section_elements[1:]

        if not (static_section.basic or static_section.optional):
            issues.append(f"{section_name}: Section is not basic but not optional")

        n_parameters = 0
        n_basic_prms = 0
        for static_parameter in static_parameters:
            more_issues = _CheckParameterValidity(section_name, static_section, static_parameter)
            issues.extend(more_issues)

            n_parameters += 1
            if static_parameter.basic:
                n_basic_prms += 1

        if static_section.basic and (n_parameters > 0) and (n_basic_prms == 0):
            issues.append(f"{section_name}: Basic section without any basic parameters")

    if issues.__len__() > 0:
        print("\n".join(issues))
        raise rp_.silent_exception_t()


def _CheckParameterValidity(
    section_name: std_label_e, section: static_section_t, parameter: static_parameter_t
) -> List[str]:
    """"""
    output = []

    if (not section.basic) and parameter.basic:
        output.append(f"{section_name}.{parameter.name}: Basic parameter in a non-basic section")
    if not (parameter.basic or parameter.optional):
        output.append(f"{section_name}.{parameter.name}: Parameter is not basic but not optional")
    if isinstance(parameter.default, missing_required_value_t):
        if parameter.optional:
            output.append(f"{section_name}.{parameter.name}: Required parameter declared optional")
        if None in parameter.types:
            output.append(f'{section_name}.{parameter.name}: Required parameter with "None" among its possible types')
        if parameter.default.types != parameter.types:
            output.append(f'{section_name}.{parameter.name}: Mismatch between "type" and "default.type"')

    return output
