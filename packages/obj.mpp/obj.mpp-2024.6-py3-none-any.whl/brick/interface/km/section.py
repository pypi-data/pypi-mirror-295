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

from typing import ClassVar, List, Optional, Sequence, Tuple, Union

import PyQt5.QtCore as qc_
import PyQt5.QtWidgets as qw_

import brick.config.parameter as cr_
from brick.config.parameter import parameter_t as functional_parameter_t
from brick.config.section import section_t as functional_section_t
from brick.data.config.std_labels import std_label_e
from brick.interface.km.library.pyqt5 import (
    TOP_ALIGNED,
    FIXED_SIZE,
    SIZE_EXPANDING,
    grid_layout_t,
    hbox_layout_t,
    label_widget_t,
    widget_t,
)
from brick.interface.km.parameter import parameter_t


class base_section_t(qw_.QGroupBox):

    HEADER_NAMES: ClassVar[Tuple[str]] = ("Parameter", "Type(s)", "Value", "Unit", "Comment")
    HEADER_STYLE: ClassVar[str] = "background-color: darkgray; padding-left: 5px;"

    _slots = ("details",)

    details: functional_section_t

    def __init__(self):
        #
        super().__init__()
        # self.__class__._slots corresponds to the derived class
        for slot in base_section_t._slots + self.__class__._slots:
            setattr(self, slot, None)

    @classmethod
    def FromFunctionalSection(cls, section: functional_section_t) -> base_section_t:
        """"""
        instance = cls()

        instance.setTitle(cr_.FormattedName(section.name, " "))
        instance.details = section

        return instance

    @classmethod
    def NewHeaders(cls) -> List[label_widget_t]:
        """"""
        output = []

        for text in cls.HEADER_NAMES:
            header = label_widget_t(f'<font color="blue">{text}</font>')
            header.SetStyleSheet(cls.HEADER_STYLE)
            output.append(header)

        comment = output[-1]
        width = comment.fontMetrics().boundingRect(comment.text()).width() + 6
        comment.setMaximumWidth(width)

        return output


class section_t(base_section_t):

    _slots = ("parameters",)

    parameters: List[parameter_t]  # Visual parameters, not functional ones

    @classmethod
    def ForSection(
        cls, section: functional_section_t
    ) -> section_t:
        #
        instance = cls.FromFunctionalSection(section)

        headers = base_section_t.NewHeaders()
        parameters, layout = _ParametersFromSpecifications(section, section.name)

        instance.parameters = parameters

        for h_idx, header in enumerate(headers):
            layout.AddWidget(header, 0, h_idx)
        instance.setLayout(layout)

        return instance

    def ActiveParameters(self) -> Sequence[parameter_t]:
        """
        Mimics the controlled_section_t version
        """
        return self.parameters

    def __getitem__(self, key: Union[int, str]) -> Optional[parameter_t]:
        """"""
        if isinstance(key, int):
            return self.parameters[key]
        else:
            index = self.details.IndexOf(key)
            if index is None:
                return None
            else:
                return self.parameters[index]


class controlled_section_t(base_section_t):

    _slots = ("parameters", "page_stack")

    parameters: List[List[parameter_t]]  # Visual parameters, not functional ones
    page_stack: qw_.QStackedWidget

    @classmethod
    def ForSection(
        cls,
        section: functional_section_t,
        controller: parameter_t,
    ) -> controlled_section_t:
        """
        The controller must have an "input" field with a "parameter_sets" field and a "currentIndex" method.
        """
        instance = cls.FromFunctionalSection(section)

        instance.page_stack = qw_.QStackedWidget()
        instance.parameters = []

        section_name = section.name
        current_selection = controller.input.currentIndex()
        for c_idx, functional_prms in enumerate(controller.input.parameter_sets):
            headers = base_section_t.NewHeaders()
            if (c_idx == current_selection) and (section.__len__() > 0):
                parameters, layout = _ParametersFromSpecifications(
                    section, section_name
                )
            else:
                parameters, layout = _ParametersFromSpecifications(
                    functional_prms, section_name
                )
            for h_idx, header in enumerate(headers):
                layout.AddWidget(header, 0, h_idx)

            page = widget_t()
            page.SetLayout(layout)

            instance.parameters.append(parameters)
            instance.page_stack.addWidget(page)

        instance.page_stack.setSizePolicy(SIZE_EXPANDING, FIXED_SIZE)
        # Curiously, the stacked widget cannot be simply declared as child of instance; This must be specified through
        # a layout.
        layout = hbox_layout_t()
        layout.AddWidget(instance.page_stack)
        layout.SetContentsMargins(0, 0, 0, 0)
        instance.setLayout(layout)

        index = controller.input.currentIndex()
        instance.page_stack.setCurrentIndex(index)
        controller.input.activated.connect(instance.page_stack.setCurrentIndex)
        # OR: self.currentTextChanged.connect(function)   activated

        return instance

    def ActiveParameters(self) -> Sequence[parameter_t]:
        """"""
        return self.parameters[self.page_stack.currentIndex()]


def _ParametersFromSpecifications(
    specifications: Sequence[functional_parameter_t],
    section: std_label_e,
) -> Tuple[List[parameter_t], grid_layout_t]:
    #
    section_is_output = (section == std_label_e.sct_output)
    parameters = []
    layout = _NewParameterLayout()

    for row, functional_parameter in enumerate(specifications, start=1):
        # if functional_parameter.value == functional_parameter.default:
        #     continue
        if section_is_output and (functional_parameter.name == "result_output_function"):
            # Exclude external output selection from GUI
            continue

        parameter = parameter_t.ForParameter(functional_parameter, section)
        parameters.append(parameter)

        has_unit = parameter.unit is not None
        layout.AddWidget(parameter.name, row, 0, alignment=qc_.Qt.AlignRight)
        layout.AddWidget(parameter.type_selector, row, 1)
        layout.AddWidget(parameter.input, row, 2)
        layout.AddWidget(parameter.comment, row, 4)
        if has_unit:
            layout.AddWidget(parameter.unit, row, 3)

    return parameters, layout


def _NewParameterLayout() -> grid_layout_t:
    """"""
    output = grid_layout_t()

    output.SetAlignment(TOP_ALIGNED)
    output.SetColumnStretch(2, 2)

    return output
