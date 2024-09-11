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

from typing import Callable, Sequence, Tuple, Union

import PyQt5.QtCore as qc_
import PyQt5.QtGui as qg_
import PyQt5.QtWidgets as qw_
from numpy import ndarray as array_t


BASE_PALETTE = qg_.QPalette.Base
COLOR_CYAN = qc_.Qt.cyan
DIALOG_ACCEPTATION = qw_.QDialog.Accepted
DIALOG_ACCEPT_OPEN = qw_.QFileDialog.AcceptOpen
DIALOG_ACCEPT_SAVE = qw_.QFileDialog.AcceptSave
DIALOG_AUTO_OWERWRITE = qw_.QFileDialog.DontConfirmOverwrite
DIALOG_MODE_ANY = qw_.QFileDialog.AnyFile
DIALOG_MODE_EXISTING_FILE = qw_.QFileDialog.ExistingFile
DIALOG_MODE_FOLDER = qw_.QFileDialog.Directory
FIXED_SIZE = qw_.QSizePolicy.Fixed
FORMAT_RICH = qc_.Qt.RichText
HCENTER_ALIGNED = qc_.Qt.AlignHCenter
KEY_CONTROL = qc_.Qt.ControlModifier.__int__()
KEY_M = qc_.Qt.Key_M
KEY_META = qc_.Qt.MetaModifier.__int__()
KEY_SHIFT = qc_.Qt.ShiftModifier.__int__()
RIGHT_ALIGNED = qc_.Qt.AlignRight
TOP_ALIGNED = qc_.Qt.AlignTop
SIZE_EXPANDING = qw_.QSizePolicy.Expanding
SIZE_MINIMUM = qw_.QSizePolicy.Minimum
TAB_POSITION_EAST = qw_.QTabWidget.East
TRANSPARENT_TO_MOUSE = qc_.Qt.WA_TransparentForMouseEvents
TABLE_H_STRETCH = qw_.QHeaderView.Stretch

action_t = qw_.QAction
alignment_flag_t = qc_.Qt.AlignmentFlag
alignment_t = qc_.Qt.Alignment
attribute_t = qc_.Qt.WidgetAttribute
color_t = qc_.Qt.GlobalColor
dialog_accept_mode_t = qw_.QFileDialog.AcceptMode
dialog_mode_t = qw_.QFileDialog.FileMode
dialog_option_t = qw_.QFileDialog.Option
event_t = qc_.QEvent
layout_t = qw_.QLayout
wheel_event_t = qg_.QWheelEvent
key_event_t = qg_.QKeyEvent
mouse_event_t = qg_.QMouseEvent
paint_event_t = qg_.QPaintEvent
point_t = qc_.QPoint
scroll_container_t = qw_.QScrollArea
size_policy_t = qw_.QSizePolicy.Policy
tab_position_t = qw_.QTabWidget.TabPosition


"""
AMethod = qw_.QSomeWidgetClass.aMethod does not work because the call then misses self.
"""


class widget_t(qw_.QWidget):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)

    def GetWidth(self) -> int:
        return self.width()

    def GetHeight(self) -> int:
        return self.height()

    def Center(self) -> None:
        """"""
        screen_center = qw_.QDesktopWidget().availableGeometry(self).center()
        geometry = self.frameGeometry()
        geometry.moveCenter(screen_center)  # Moves the window

    def DetachAndRelease(self) -> None:
        self.setParent(None)


class label_widget_t(qw_.QLabel):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)


class button_widget_t(qw_.QPushButton):
    """"""

    def __init__(self, text: str, parent: qw_.QWidget = None):
        """"""
        super().__init__(text=text, parent=parent)
        _SetCapitalizedMethods(self)

    def SetFunction(self, function: Callable) -> None:
        self.clicked.connect(function)


class combobox_widget_t(qw_.QComboBox):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)

    def Selection(self) -> str:
        return self.currentText()

    def SelectionIndex(self) -> int:
        return self.currentIndex()

    def ItemAt(self, index: int) -> str:
        return self.itemText(index)

    def SetFunction(self, function: Callable) -> None:
        self.activated.connect(function)  # or currentTextChanged???


class table_widget_t(qw_.QTableWidget):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)

    def SetHResizeMode(self, mode: qw_.QHeaderView.ResizeMode) -> None:
        self.horizontalHeader().setSectionResizeMode(mode)

    def SetItemAsStr(self, row: int, col: int, item: str) -> None:
        self.setItem(row, col, qw_.QTableWidgetItem(item))

    def GetNRows(self) -> int:
        return self.rowCount()

    def GetNCols(self) -> int:
        return self.columnCount()

    def GetHHeaderHeight(self) -> int:
        return self.horizontalHeader().height()

    def GetRowHeight(self, row: int = 0) -> int:
        return self.rowHeight(row)


class single_input_widget_t(qw_.QLineEdit):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)


class image_widget_t(qw_.QLabel):
    """"""

    __slots__ = ("widget_image",)

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.widget_image = None
        _SetCapitalizedMethods(self)

    def GetWidth(self) -> int:
        return self.width()

    def SetWidgetImage(self, rgb_image: array_t) -> None:
        """
        QImage call taken from:
        https://github.com/baoboa/pyqt5/blob/master/examples/widgets/imageviewer.py
        """
        # widget_image must be kept alive in instance
        self.widget_image = qg_.QImage(
            rgb_image.data,
            rgb_image.shape[1],
            rgb_image.shape[0],
            3 * rgb_image.shape[1],
            qg_.QImage.Format_RGB888,
        )
        self.setPixmap(qg_.QPixmap.fromImage(self.widget_image))

    def DrawPoints(
        self,
        points: Tuple[array_t, array_t],
        color: Tuple[int, int, int],
        bbox_width: int = 1,
        bbox_height: int = 1,
    ) -> None:
        """"""
        # noinspection PyArgumentList
        contour_qpoints = tuple(point_t(point[1], point[0]) for point in zip(*points))
        # noinspection PyArgumentList
        pixmap = qg_.QPixmap(self.pixmap())

        painter = qg_.QPainter()
        painter.begin(pixmap)
        # noinspection PyArgumentList
        painter.setPen(qg_.QPen(qg_.QColor(*color)))  # Must be after call to begin
        for point in contour_qpoints:
            # TODO: Check why -1's are necessary
            # noinspection PyArgumentList
            painter.drawPoint(point.x() + bbox_width - 1, point.y() + bbox_height - 1)
        painter.end()

        self.setPixmap(pixmap)


class scrollable_widget_t(qw_.QScrollArea):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)

    @classmethod
    def NewForWidget(cls, widget: qw_.QWidget) -> scrollable_widget_t:
        """"""
        instance = cls()
        instance.setWidget(widget)
        # instance.setBackgroundRole(qg_.QPalette.Dark)

        return instance


class tab_widget_t(qw_.QTabWidget):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)


class menu_t(qw_.QMenu):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)

    @classmethod
    def NewSubmenuForMenuWithName(cls, menu: menu_t, name: str) -> menu_t:
        """"""
        instance = menu.addMenu(name)
        instance.__class__ = cls

        return instance

    def AddEntry(self, entry: str) -> None:
        self.addAction(entry)

    def SetFunction(self, function: Callable) -> None:
        self.triggered.connect(function)


class file_selection_widget_t(qw_.QFileDialog):
    """"""

    def __init__(self, caption: str, extension_filter: str = None):
        """"""
        if extension_filter is None:
            extension_filter = "Any files (*)"
        super().__init__(caption=caption, filter=extension_filter)
        _SetCapitalizedMethods(self)

    def SelectedFile(self) -> str:
        return self.selectedFiles()[0]

    def RunAndGetClosingStatus(self) -> int:
        return self.exec_()


class patience_window_t(qw_.QSplashScreen):
    """"""

    WIDTH: int = 480
    HEIGHT: int = int(WIDTH / 1.6180339887)
    MESSAGE: str = (
        "Obj.MPP\n"
        "Object/Pattern Detection using a Marked Point Process\n"
        "Launching..."
    )

    def __init__(self, event_loop: widget_event_loop_t, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

        cls = self.__class__

        contents = qg_.QPixmap(cls.WIDTH, cls.HEIGHT)
        contents.fill(qc_.Qt.darkGray)

        max_line_length = max(map(len, cls.MESSAGE.split("\n")))
        font = qg_.QFont()
        font.setStyleHint(qg_.QFont.Monospace)
        # Why times 2? It should not be necessary I think, but it works that way...
        font.setPixelSize(2 * int(cls.WIDTH / (max_line_length + 2)))
        painter = qg_.QPainter(contents)
        painter.setFont(font)
        painter.drawText(
            0,
            0,
            cls.WIDTH,
            cls.HEIGHT,
            qc_.Qt.AlignHCenter | qc_.Qt.AlignVCenter,
            cls.MESSAGE,
        )
        self.painter = painter  # Maintains a ref, otherwise app crashes

        self.setPixmap(contents)
        self.show()
        event_loop.processEvents()


class hbox_layout_t(qw_.QHBoxLayout):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)


class vbox_layout_t(qw_.QVBoxLayout):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)


class grid_layout_t(qw_.QGridLayout):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        _SetCapitalizedMethods(self)


class painter_t(qg_.QPainter):
    """
    /!\\ Do not set capitalized methods, it freezes the GUI
    """

    def SetPenColor(self, color: Union[str, color_t]) -> None:
        self.setPen(qg_.QColor(color))
        # self.setPen(qg_.QPen(color))

    def DrawRoundedRect(
        self, x: int, y: int, w: int, h: int, radius_x: float, radius_y: float
    ) -> None:
        self.drawRoundedRect(x, y, w, h, radius_x, radius_y)

    def DrawPointSequence(self, points: Sequence[point_t]) -> None:
        self.drawPoints(*points)


class widget_event_loop_t(qw_.QApplication):
    """"""

    @staticmethod
    def GetInstance() -> qc_.QCoreApplication:
        return widget_event_loop_t.instance()

    @staticmethod
    def Run() -> int:
        return qw_.QApplication.exec_()


def GetEventModifiers(event: Union[key_event_t, mouse_event_t, wheel_event_t]) -> int:
    """"""
    return event.modifiers().__int__()


def ShowErrorMessage(message: str, parent: qw_.QWidget = None) -> None:
    """"""
    qw_.QErrorMessage(parent).showMessage(message)


def ShowCriticalMessage(title: str, message: str, parent: qw_.QWidget = None) -> None:
    """"""
    qw_.QMessageBox.critical(parent, title, message)


def _SetCapitalizedMethods(widget: Union[qw_.QLayout, qw_.QWidget]) -> None:
    """"""
    for name in dir(widget):
        first_letter = name[0]
        # hasattr test: necessary since this function is called early in the initialization process, so some fields
        # might not have been set yet.
        if (first_letter == first_letter.lower()) and hasattr(widget, name):
            attribute = getattr(widget, name)
            if isinstance(attribute, Callable):
                setattr(widget, first_letter.upper() + name[1:], attribute)
