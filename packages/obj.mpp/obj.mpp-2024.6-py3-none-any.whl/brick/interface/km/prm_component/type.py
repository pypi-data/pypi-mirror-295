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

from typing import Any, Sequence

from brick.interface.km.library.pyqt5 import combobox_widget_t, label_widget_t, widget_t


single_type_t = label_widget_t


class multiple_types_t(combobox_widget_t):
    def __init__(
        self, types: Sequence[Any], type_: type, parent: widget_t = None
    ) -> None:
        #
        super().__init__(parent=parent)

        for type_ in types:
            self.AddItem(type_.__name__)

        self.SetCurrentText(type_.__name__)
        # TODO: add the switch mechanism with stacked widget

    #
    # def ChangeValueField(self, new_type: action_t) -> None:
    #     #
    #     raise NotImplementedError
    #     # value_field     = self.prm_data[1]
    #     # parent          = value_field.parent()
    #     # new_type_as_str = new_type.text()
    #     #
    #     # if (new_type_as_str == 'None') or (new_type_as_str == 'int') or (new_type_as_str == 'str'):
    #     #     if isinstance(value_field, qw_.QLineEdit):
    #     #         if new_type_as_str == 'None':
    #     #             value_field.setText('None')
    #     #         return
    #     #     new_value_field = qw_.QLineEdit('None', parent = parent)
    #     # elif new_type.parentWidget().title() == 'tuple':
    #     #     try:
    #     #         new_n_elms = int(new_type_as_str)
    #     #         if isinstance(value_field, vl_.tuple_wgt_t) and (value_field.n_elms() == new_n_elms):
    #     #             return
    #     #         new_value_field = vl_.tuple_wgt_t.WithInitialValue(parent, ('',)*new_n_elms)
    #     #     except:
    #     #         if isinstance(value_field, qw_.QLineEdit):
    #     #             return
    #     #         new_value_field = qw_.QLineEdit('()', parent = parent)
    #     # elif new_type_as_str == 'path':
    #     #     if isinstance(value_field, vl_.path_wgt_t):
    #     #         return
    #     #     new_value_field = vl_.path_wgt_t.WithInitialValue(parent, '', 'path')
    #     # else:
    #     #     raise TypeError(f'{new_type_as_str}{mg_.SEP}Unknown parameter type')
    #     #
    #     # parent.layout().replaceWidget(value_field, new_value_field)
    #     # value_field.setVisible(False) # Why is this "workaround" necessary?
    #     #
    #     # self.prm_data[1] = new_value_field
