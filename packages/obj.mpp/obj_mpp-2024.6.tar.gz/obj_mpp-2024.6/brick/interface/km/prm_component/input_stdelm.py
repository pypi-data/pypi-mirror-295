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

from enum import Enum as enum_t
from typing import Any, Optional, Tuple

import brick.interface.io.reporting as mg_
import brick.structure.explorer as ex_
from brick.config.config import config_t
from brick.config.parameter import parameter_t
from brick.data.config.no_circular_import import PARAMETER_RANGE_SUFFIX
from brick.data.config.std_labels import std_label_e
from brick.data.config.type import missing_required_value_t, tuple_t
from brick.marked_point.generic import marked_point_t
from brick.data.marked_point.std_marks import mark_details_t
from brick.data.marked_point.twoD.std_marked_points import STD_MARKED_POINTS
from brick.interface.km.library.pyqt5 import combobox_widget_t, widget_t


# noinspection PyArgumentList
std_elm_category_e = enum_t("std_elm_category_e", "MARKED_POINT QUALITY")


class standard_element_t(combobox_widget_t):

    _slots = ("text", "category", "parameter_sets")

    def __init__(
        self,
        initial_value: Optional[str],
        category: std_elm_category_e,
        section: std_label_e,
        parent: widget_t = None,
    ) -> None:
        #
        super().__init__(parent=parent)

        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in standard_element_t._slots:
            setattr(self, slot, None)

        self.text = self.currentText  # Add the text method
        self.category = category

        if category == std_elm_category_e.MARKED_POINT:
            mkpt_types = tuple(
                _typ
                for _typ in ex_.StandardMarkedPoints("class")
                if _typ.__name__[:-2] in STD_MARKED_POINTS
            )
            elements = (_typ.__name__[:-2] for _typ in mkpt_types)
            self.parameter_sets = []
            for mkpt_type in mkpt_types:
                # Must be converted from generator to tuple, otherwise mkpt_type will be the last value of the loop for
                # all the generated elements.
                parameter_set = tuple(
                    _ParameterForMark(name, details, mkpt_type, section)
                    for name, details in mkpt_type.marks_details.items()
                )
                self.parameter_sets.append(parameter_set)
        elif category == std_elm_category_e.QUALITY:
            elements = (
                elm.split(".")[1] for elm in ex_.StandardQualityFunctionInfos().keys()
            )
            self.parameter_sets = []
            for _, signature in ex_.StandardQualityFunctionInfos().values():
                parameter_set = (
                    _ParameterForQualityArgument(name, value, section)
                    for name, value in signature.arg_default_values.items()
                )
                self.parameter_sets.append(parameter_set)
        else:
            # Just in case a category is added but not handled here
            raise ValueError(f"{category}{mg_.SEP}Invalid category")
        for element in elements:
            self.AddItem(element)

        if (initial_value is None) or isinstance(
            initial_value, missing_required_value_t
        ):
            pass
        else:
            if config_t.INI_MOD_ELM_SEPARATOR in initial_value:
                initial_value = initial_value.split(config_t.INI_MOD_ELM_SEPARATOR)[1]
            self.SetCurrentText(initial_value)

    def Options(self) -> Tuple[str, ...]:
        """"""
        return tuple(self.itemText(_idx) for _idx in range(self.count()))


def _ParameterForMark(
    name: str, mark: mark_details_t, type_: marked_point_t, section: std_label_e
) -> parameter_t:
    #
    parameter = parameter_t.ForProgrammaticEntry(
        type_.ININameOf(name) + PARAMETER_RANGE_SUFFIX, mark.default_range, section
    )
    parameter.basic = True
    parameter.optional = False
    parameter.types = (None, tuple_t((2, 3), obj_mpp_type=tuple_t.MARK_INTERVAL))

    return parameter


def _ParameterForQualityArgument(
    name: str, value: Any, section: std_label_e
) -> parameter_t:
    #
    parameter = parameter_t.ForProgrammaticEntry(name, value, section)
    parameter.basic = True

    return parameter
