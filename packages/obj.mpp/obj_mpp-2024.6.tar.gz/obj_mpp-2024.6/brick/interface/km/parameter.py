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

from typing import Union

from brick.config.parameter import parameter_t as functional_parameter_t, missing_required_value_t
from brick.data.config.std_labels import std_label_e
from brick.data.config.type import text_t
from brick.data.config.unit import UNIT_SEPARATOR
from brick.interface.km.library.pyqt5 import (
    label_widget_t,
    single_input_widget_t,
    widget_t,
)
from brick.interface.km.prm_component.comment import prm_comment_t
from brick.interface.km.prm_component.input_bool import bool_wgt_t
from brick.interface.km.prm_component.input_path import path_wgt_t
from brick.interface.km.prm_component.input_stdelm import (
    standard_element_t,
    std_elm_category_e,
)
from brick.interface.km.prm_component.input_tuple import tuple_wgt_t
from brick.interface.km.prm_component.type import multiple_types_t, single_type_t


class parameter_t:
    """
    In order to leave the section widget put the name, type, input, and comment widgets of each parameter in columns,
    parameter_t is not a container widget. Instead, it just store its component widgets for later addition to a layout.
    """

    __slots__ = (
        "details",
        "name",  # Visual version, not functional one, which is details.name
        "type_selector",
        "input",
        "unit",
        "comment",
    )

    details: functional_parameter_t
    name: label_widget_t
    type_selector: Union[single_type_t, multiple_types_t]
    input: widget_t
    unit: single_input_widget_t
    comment: prm_comment_t

    def __init__(self) -> None:
        #
        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in parameter_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def ForParameter(
        cls,
        parameter: functional_parameter_t,
        section: std_label_e,
    ) -> parameter_t:
        #
        instance = cls()

        instance.details = parameter
        instance.name = label_widget_t(parameter.formatted_name)

        value, spec_type, python_type, obj_mpp_type, non_none_types = parameter.EducatedValueAndTypes()

        if non_none_types.__len__() > 1:
            type_selector = multiple_types_t(non_none_types, obj_mpp_type)
        else:
            type_selector = single_type_t(python_type.__name__)
        instance.type_selector = type_selector

        if obj_mpp_type is text_t.MARKED_POINT:
            value_input = standard_element_t(
                value, std_elm_category_e.MARKED_POINT, section
            )
        elif obj_mpp_type is text_t.QUALITY:
            value_input = standard_element_t(value, std_elm_category_e.QUALITY, section)
        elif (obj_mpp_type is text_t.FUNCTION) or text_t.IsPlainPath(obj_mpp_type):
            value_input = path_wgt_t.WithInitialValue(value, obj_mpp_type, parameter.IsAnOutput())
        elif python_type is bool:
            value_input = bool_wgt_t.WithInitialValue(value)
        elif python_type is tuple:
            value_input = tuple_wgt_t.WithInitialValue(value, spec_type)
        else:
            # This test is here because "single_input_widget_t" is just an "alias" for PyQt5.QLineEdit. Normally, it
            # should be in the "WithInitialValue" method as with the others input widgets.
            if (value is None) or isinstance(value, missing_required_value_t):
                initial_value = ""
            else:
                initial_value = str(value)
            value_input = single_input_widget_t(initial_value)
        instance.input = value_input

        if parameter.unit is not None:
            instance.unit = single_input_widget_t(parameter.unit)

        contents = f"{parameter.definition}.\n\n{parameter.description}."
        if parameter.comment is not None:
            contents += f"\n\n{parameter.comment}."
        comment = prm_comment_t.WithInitialValue(
            section.value + ":" + parameter.formatted_name,
            contents,
        )
        instance.comment = comment

        name_style = "padding-right: 5px;"
        if parameter.optional:
            name_style += "color: gray;"
        instance.name.SetStyleSheet(name_style)
        instance.type_selector.setStyleSheet(name_style)

        return instance

    def SetVisible(self, visible: bool) -> None:
        """"""
        self.name.setVisible(visible)
        self.type_selector.setVisible(visible)
        self.input.setVisible(visible)
        self.comment.setVisible(visible)
        if self.unit is not None:
            self.unit.setVisible(visible)

    def text(self) -> str:
        #
        if self.unit is None:
            unit = None
        else:
            unit = self.unit.text()

        if (unit is None) or (unit.__len__() == 0):
            return self.input.text()

        return f"{self.input.text()}{UNIT_SEPARATOR}{unit}"

    # def GetValue(self, unit_conversions: unit_conversions_h = None) -> Any:
    #     """"""
    #     # TODO: check qt encoding .decode(encoding)
    #     self.details.SetValueFromString(
    #         self.input.text()#, unit_conversions=unit_conversions
    #     )
    #
    #     return self.details.value
