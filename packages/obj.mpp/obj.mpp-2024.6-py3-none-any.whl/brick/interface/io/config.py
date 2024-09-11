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

import configparser as cp_
import sys as sy_
from typing import Optional, Union

import brick.interface.io.reporting as mg_
import brick.interface.ko.text_color as tc_
from brick.config.config import config_t, raw_config_h
from brick.data.config.specification import missing_required_value_t
from brick.data.config.std_labels import std_label_e
from brick.data.type import pl_path_t
from brick.config.section import NonDefaultUnits


def PrintInRawForm(
    config: Union[raw_config_h, config_t], include_empty: bool = False
) -> None:
    #
    if isinstance(config, config_t):
        for section in config.values():
            if section.name == std_label_e.sct_range_units:
                section = NonDefaultUnits(section)

            if not ((section.__len__() > 0) or include_empty):
                continue

            mg_.ReportI(f"[{section.name.value}]")

            for parameter in section:
                mg_.ReportI(f"{parameter.name} = {parameter.value}")
    else:
        for sct_name, parameters in config.items():
            if not ((parameters.__len__() > 0) or include_empty):
                continue
            # Contrary to the config_t branch above, it cannot be checked (without going back to the specification) if a
            # unit has its default value or not, so the section is simply ignored.
            if sct_name == std_label_e.sct_range_units:
                continue

            mg_.ReportI(f"[{sct_name}]")

            for prm_name, value in parameters.items():
                mg_.ReportI(f"{prm_name} = {value}")


def Print(config: config_t) -> None:
    #
    field_length = 0
    for section in config.values():
        if (section.__len__() > 0) and (section.name != std_label_e.sct_range_units):
            field_length = max(
                field_length, max(map(lambda _elm: _elm.name.__len__(), section))
            )

    for section in config.values():
        if section.name == std_label_e.sct_range_units:
            section = NonDefaultUnits(section)

        if section.__len__() == 0:
            continue

        mg_.ReportI(
            tc_.ColoredText(f"[{section.name.value}]", "blue"),
        )

        for parameter in section:
            if (config.has_default_value is not None) and (
                parameter.UId in config.has_default_value
            ):
                equ_sign = "?"
            else:
                equ_sign = ":"

            value = parameter.value
            type_as_str = (
                ""
                if (value is None)
                or isinstance(value, missing_required_value_t)
                or isinstance(value, str)
                or isinstance(value, pl_path_t)
                else "/" + type(value).__name__
            )

            value_as_str = tc_.ColoredText(value.__str__(), "green")
            type_as_str = tc_.ColoredText(type_as_str, "magenta")
            mg_.ReportI(
                f"    {parameter.name:<{field_length}}{equ_sign}{value_as_str}{type_as_str}",
            )


def RawConfigFromINIDocument(
    ini_document: Union[str, pl_path_t],
) -> Optional[raw_config_h]:
    #
    if isinstance(ini_document, str):
        ini_document = pl_path_t(ini_document)

    if ini_document.is_file():
        # RawConfigParser=legacy version
        raw_config = cp_.ConfigParser(
            delimiters=config_t.INI_VALUE_ASSIGNEMENT,
            comment_prefixes=config_t.INI_COMMENT_MARKER,
            empty_lines_in_values=False,
            interpolation=None,
        )
        raw_config.optionxform = lambda option: option
        # Returns DEFAULT <Section: DEFAULT> if ini_document does not exist
        raw_config.read(ini_document, encoding=sy_.getfilesystemencoding())

        return raw_config
    else:
        return None


def WriteConfigToINIDocument(
    config: Union[raw_config_h, config_t], path: pl_path_t
) -> None:
    #
    encoding = sy_.getfilesystemencoding()
    # TODO: check qt encoding .decode(encoding)

    with path.open("w", encoding=encoding) as ini_accessor:
        if isinstance(config, config_t):
            for section in config.values():
                if section.name == std_label_e.sct_range_units:
                    section = NonDefaultUnits(section)

                if section.__len__() == 0:
                    continue

                print(f"[{section.name}]", file=ini_accessor)

                for parameter in section:
                    print(f"{parameter.name} = {parameter.value}", file=ini_accessor)

                print(f"", file=ini_accessor)
        else:
            for sct_name, parameters in config.items():
                if parameters.__len__() == 0:
                    continue

                print(f"[{sct_name}]", file=ini_accessor)

                for prm_name, value in parameters.items():
                    print(f"{prm_name} = {value}", file=ini_accessor)

                print(f"", file=ini_accessor)


# def __str__(self) -> str:
#     #
#     components = []
#     for field_name in dir(self):
#         if not (field_name.startswith("__") and field_name.endswith("__")):
#             field_value = getattr(self, field_name)
#             if not isinstance(field_value, Callable):
#                 if hasattr(field_value, "text") and isinstance(
#                     field_value.text, Callable
#                 ):
#                     field_value = (
#                         f"{type(field_value).__name__}={field_value.text()}"
#                     )
#                 components.append(f"{field_name}: {field_value}\n")
#
#     return "".join(components)


# def ConfigFromINIDocument(
#     ini_document: Union[str, pl_path_t],
# ) -> Optional[config_t]:
#     #
#     if isinstance(ini_document, str):
#         ini_document = pl_path_t(ini_document)
#
#     # RawConfigParser=legacy version
#     raw_config = cp_.ConfigParser(
#         delimiters=config_t.INI_VALUE_ASSIGNEMENT,
#         comment_prefixes=config_t.INI_COMMENT_MARKER,
#         empty_lines_in_values=False,
#         interpolation=None,
#     )
#     raw_config.optionxform = lambda option: option
#     # Returns DEFAULT <Section: DEFAULT> if ini_document does not exist
#     raw_config.read(ini_document, encoding=sy_.getfilesystemencoding())
#
#     output = config_t.FromRawConfig(raw_config)
#     output.ini_document = ini_document
#
#     output.AddDefaults()
#
#     return output
