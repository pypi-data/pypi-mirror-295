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

from typing import ClassVar, Dict, Tuple

import PyQt5.QtWidgets as qw_

from brick.data.config.specification import missing_required_value_t


class bool_wgt_t(qw_.QWidget):

    MODE_LABELS: ClassVar[Dict[str, Tuple[str, str]]] = {
        "boolean": ("True", "False"),
        "current": ("On", "Off"),
    }

    def __init__(self, parent: qw_.QWidget = None) -> None:
        #
        super().__init__(parent=parent)
        self.true_btn = None

    @classmethod
    def WithInitialValue(
        cls, value: bool, mode: str = "boolean"
    ) -> bool_wgt_t:
        #
        instance = cls()

        if (value is None) or isinstance(
            value, missing_required_value_t
        ):
            value = False

        labels = cls.MODE_LABELS.get(mode)
        if labels is None:
            raise ValueError(f"{mode}: Invalid mode")
        true_btn = qw_.QRadioButton(labels[0], parent=instance)
        false_btn = qw_.QRadioButton(labels[1], parent=instance)
        true_btn.setChecked(value)
        false_btn.setChecked(not value)

        instance.true_btn = true_btn

        layout = qw_.QHBoxLayout()
        layout.addWidget(true_btn)
        layout.addWidget(false_btn)
        instance.setLayout(layout)

        return instance

    def text(self) -> str:
        return str(self.true_btn.isChecked())
