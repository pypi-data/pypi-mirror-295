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

from typing import Any, ClassVar, Sequence, Tuple, Union

from brick.data.config.type import missing_required_value_t, tuple_t
from brick.interface.km.library.pyqt5 import (
    combobox_widget_t,
    hbox_layout_t,
    single_input_widget_t,
    widget_t,
)


class tuple_wgt_t(widget_t):

    ENTRY_ANY: ClassVar[str] = "any"
    ENTRIES: ClassVar[Tuple[str, ...]] = ("2", "3", "4", "5", "6") + (ENTRY_ANY,)

    _slots = ("length_selector", "components")

    length_selector: combobox_widget_t
    components: Tuple[single_input_widget_t, ...]

    def __init__(self, parent: widget_t = None):
        #
        super().__init__(parent=parent)

        # Leave self.__class__ so _slots will correspond to the derived class
        for slot in self.__class__._slots:
            setattr(self, slot, None)

    @classmethod
    def WithInitialValue(
        cls, value: tuple, spec_type: Union[tuple, tuple_t]
    ) -> tuple_wgt_t:
        #
        instance = cls()

        if (value is None) or isinstance(value, missing_required_value_t):
            value = ()
            length = 0
        else:
            length = value.__len__()

        if spec_type is tuple:
            entries = cls.ENTRIES
            max_entry = entries[-2]
        else:
            entries = tuple(str(_lgh) for _lgh in spec_type.lengths)
            max_entry = entries[-1]
        if entries.__len__() > 1:
            length_selector = combobox_widget_t()
            for entry in entries:
                length_selector.AddItem(entry)
            length_as_str = str(length)
            if length_as_str in entries:
                length_selector.SetCurrentText(length_as_str)
            elif cls.ENTRY_ANY in entries:
                length_selector.SetCurrentText(cls.ENTRY_ANY)
            elif length > 0:
                raise ValueError(
                    f"{value}: Tuple with invalid length; Expected={entries}"
                )
            instance.length_selector = length_selector

        components = []
        if instance.length_selector is not None:
            for _ in range(int(max_entry)):
                widget = single_input_widget_t("", parent=None)
                components.append(widget)
            if length > 0:
                _AdjustComponents(components, length, value=value)
        elif length > 0:
            for element in value:
                widget = single_input_widget_t(str(element), parent=None)
                components.append(widget)
        else:
            widget = single_input_widget_t("", parent=None)
            components.append(widget)
        instance.components = tuple(components)

        if instance.length_selector is not None:
            instance.length_selector.SetFunction(instance.SetLength)

        layout = hbox_layout_t()
        layout.SetContentsMargins(0, 0, 0, 0)
        if instance.length_selector is not None:
            layout.AddWidget(instance.length_selector)
        for component in instance.components:
            layout.AddWidget(component)
        instance.SetLayout(layout)

        return instance

    def SetLength(self, new_index: int) -> None:
        """"""
        new_length = self.length_selector.ItemAt(new_index)
        if new_length == self.__class__.ENTRY_ANY:
            new_length = 1
        else:
            new_length = int(new_length)
        _AdjustComponents(self.components, new_length)

    def text(self) -> str:
        #
        if self.components.__len__() > 1:
            output = "("

            contents_length = 0
            for component in self.components:
                # Do not use "visible" here since setting visible does not really set the property until it is actually
                # shown. The documentation explains about ancestors being visible or not, but it was not clear that the
                # property is apparently not effective immediately.
                if not component.isEnabled():
                    break
                contents = component.text().strip()
                output += contents + ", "
                contents_length += contents.__len__()

            if contents_length > 0:
                return output[:-2] + ")"
            else:
                return ""
        else:
            return self.components[0].text().strip()


def _AdjustComponents(
    components: Sequence[single_input_widget_t, ...],
    length: int,
    value: Sequence[Any] = None,
) -> None:
    """
    If "value" is given, it must have a length of "length"
    """
    for c_idx, component in enumerate(components):
        if c_idx < length:
            component.SetVisible(True)
            component.setEnabled(True)
            if value is not None:
                component.SetText(str(value[c_idx]))
        else:
            component.SetVisible(False)
            component.setEnabled(False)
