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

from typing import Any, ClassVar

from brick.interface.km.status_area import status_area_t
from brick.interface.km.library.pyqt5 import button_widget_t, widget_t


class prm_comment_t(button_widget_t):

    comment_area: ClassVar[Any] = None
    last_opened: ClassVar[prm_comment_t] = None

    __slots__ = ("source", "contents")

    def __init__(self, parent: widget_t = None) -> None:
        #
        text = "?"

        # noinspection PyArgumentList
        super().__init__(text=text, parent=parent)
        self.source = None
        self.contents = None

    @classmethod
    def WithInitialValue(
        cls, source: str, contents: str
    ) -> prm_comment_t:
        #
        instance = cls()

        instance.source = source
        instance.contents = contents
        # noinspection PyUnresolvedReferences
        instance.SetFunction(instance.ToggleContents)

        return instance

    def ToggleContents(self) -> None:
        #
        cls = self.__class__
        if cls.last_opened is self:
            self.contents = cls.comment_area.contents.toPlainText()
        else:
            if cls.last_opened is not None:
                cls.last_opened.contents = (
                    cls.comment_area.contents.toPlainText()
                )
            cls.last_opened = self
            cls.comment_area.title.setText(self.source)
            cls.comment_area.contents.setPlainText(self.contents)

    def text(self) -> str:
        return self.contents

    @classmethod
    def SetCommentArea(cls, comment_area: status_area_t) -> None:
        #
        cls.comment_area = comment_area
