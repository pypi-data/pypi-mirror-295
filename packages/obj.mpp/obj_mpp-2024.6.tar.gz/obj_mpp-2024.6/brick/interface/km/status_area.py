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

import re as re_
# import time as tm_

import PyQt5.QtGui as qg_
import PyQt5.QtWidgets as qw_


class status_area_t(qw_.QWidget):
    #
    def __init__(self, title: str) -> None:
        #
        super().__init__(parent=None)
        self.title = qw_.QLabel(title)
        self.contents = qw_.QPlainTextEdit("")

        self.title.setStyleSheet("color: green; font-weight: bold;")

        self.contents.setReadOnly(True)
        self.contents.setUndoRedoEnabled(False)
        self.contents.setLineWrapMode(qw_.QPlainTextEdit.WidgetWidth)
        self.contents.setWordWrapMode(qg_.QTextOption.WordWrap)
        self.contents.setStyleSheet("font-family: monospace;")

        # self.latest_repaint = tm_.clock_gettime(tm_.CLOCK_MONOTONIC)

        # size_policy = qw_.QSizePolicy()
        # size_policy.setHorizontalPolicy(qw_.QSizePolicy.Expanding)
        # self.title.setSizePolicy(size_policy)
        # self.contents.setSizePolicy(size_policy)

        layout = qw_.QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.contents)
        self.setLayout(layout)

    # def setWidth(self,
    #         width: int
    #         )-> None:
    #
    # self.title.resize(width, self.title.height())
    # self.contents.resize(width, self.contents.height())

    def SetTitle(self, title: str) -> None:
        #
        self.title.setText(title)
        self.title.repaint()

    def Clear(self) -> None:
        #
        self.contents.clear()

    def text(self) -> str:
        #
        return self.contents.toPlainText()

    def write(self, text: str) -> None:
        #
        # It looks like "print" sends separately the contents and the end character. It then looks like
        # "appendPlainText" appends a newline automatically (why?), even if the contents is empty (why?).
        #
        text = re_.sub(r"\\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?m", "", text)
        if text.__len__() > 0:
            self.contents.appendPlainText(text)  # Adds a(n unwanted) newline
            # Repainting every time makes Qt crash. The following command:
            #     gdb --args python mpp_detector_gi.py resource/twoD/microscopy-circle.ini
            # leads to:
            #     Thread 1 "python" received signal SIGSEGV, Segmentation fault.
            #     0x00007fffd7f78c71 in ?? () from /usr/lib/libQt5XcbQpa.so.5
            # Solution: do not repaint every time! or at all! Anyway, Qt still crashes from time to time!
            # new_time_point = tm_.clock_gettime(tm_.CLOCK_MONOTONIC)
            # if new_time_point > self.latest_repaint + 3.0:
            #     self.contents.repaint()
            #     self.latest_repaint = new_time_point
