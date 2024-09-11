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

import os.path as ph_  # Pathlib not needed for the moment

import PyQt5.QtWidgets as qw_

import brick.interface.km.file_dialogs as fd_
from brick.data.config.type import text_t
from brick.data.config.specification import missing_required_value_t
from brick.data.type import pl_path_t
from brick.interface.km.library.pyqt5 import (
    ShowCriticalMessage,
    button_widget_t,
    hbox_layout_t,
    label_widget_t,
    paint_event_t,
    painter_t,
    widget_t,
vbox_layout_t,
)

# import interface.std_module_chooser as ch_


class path_wgt_t(widget_t):

    __slots__ = (
        "obj_mpp_type",
        "is_an_output",
        "choice",
        "linedit_wgt",
        "module_wgt",
        "button_wgt",
    )

    def __init__(self, parent: widget_t = None) -> None:
        #
        super().__init__(parent=parent)
        self.obj_mpp_type = None  # path, marked point, quality, or function (as str)
        self.is_an_output = None
        self.choice = None  # Selection made in the dialog
        self.linedit_wgt = None
        self.module_wgt = None
        self.button_wgt = None

    @classmethod
    def WithInitialValue(
        cls, value, obj_mpp_type: type, is_an_output: bool
    ) -> path_wgt_t:
        #
        instance = cls()

        if (value is None) or isinstance(value, missing_required_value_t):
            value = ""

        if text_t.IsPlainPath(obj_mpp_type):
            linedit_wgt = qw_.QLineEdit(value.__str__(), parent=instance)
            module_wgt = mod_caption_wgt = None
        else:
            # instance.paintEvent = instance.PaintEventWithBorder
            if ":" not in value:
                value = ":" + value
            path, elm = value.split(":")
            linedit_wgt = qw_.QLineEdit(elm, parent=instance)
            module_wgt = qw_.QLineEdit(path, parent=instance)
            mod_caption_wgt = label_widget_t("In", parent=instance)
        button_wgt = button_widget_t("...", parent=instance)
        button_wgt.SetFunction(instance.SelectDocument)

        button_wgt.setFixedWidth(30)

        if text_t.IsPlainPath(obj_mpp_type):
            layout = hbox_layout_t()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.AddWidget(linedit_wgt)
            layout.AddWidget(button_wgt)
        else:
            sublayout = hbox_layout_t()
            sublayout.setContentsMargins(0, 0, 0, 0)
            sublayout.AddWidget(linedit_wgt)
            sublayout.AddWidget(button_wgt)

            sublayt_2 = hbox_layout_t()
            sublayt_2.setContentsMargins(0, 0, 0, 0)
            sublayt_2.AddWidget(mod_caption_wgt)
            sublayt_2.AddWidget(module_wgt)

            layout = vbox_layout_t()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.AddLayout(sublayout)
            layout.AddLayout(sublayt_2)
        instance.setLayout(layout)

        instance.obj_mpp_type = obj_mpp_type
        instance.is_an_output = is_an_output
        instance.linedit_wgt = linedit_wgt
        instance.module_wgt = module_wgt
        instance.button_wgt = button_wgt

        return instance

    def text(self) -> str:
        #
        if text_t.IsPlainPath(self.obj_mpp_type):
            return self.linedit_wgt.text()
        else:
            path = self.module_wgt.text()
            if path.__len__() > 0:
                return path + ":" + self.linedit_wgt.text()
            else:
                return self.linedit_wgt.text()

    # def SaveStandardTypeChoice(self,
    #         std_chooser,
    #         from_dialog
    #         )-> None:
    #     #
    #     self.choice = std_chooser.ChoiceWidget().text()
    #     from_dialog.done(qw_.QDialog.Accepted)

    # def SaveStandardQualityChoice(self,
    #         std_chooser,
    #         from_dialog
    #         )-> None:
    #     #
    #     self.choice = std_chooser.ChoiceWidget().text()
    #     self.choice_details = std_chooser.choice_details[self.choice]
    #     from_dialog.done(qw_.QDialog.Accepted)

    # def SaveStandardFunctionChoice(self,
    #         std_chooser,
    #         from_dialog
    #         )-> None:
    #     #
    #     self.choice = std_chooser.ChoiceWidget().text()
    #     self.choice_details = std_chooser.choice_details[self.choice]
    #     from_dialog.done(qw_.QDialog.Accepted)

    def SelectDocument(self) -> None:
        #
        # TODO: use type field to allow selection of doc alone, folder alone, or both
        # If argument is empty, "resolve" returns the current folder, which would enforce "folder" selection mode
        # whereas we want "both" selection mode in such a case where there is not clue about the expected, file or
        # folder, selected node type.
        current_path = self.linedit_wgt.text()
        if current_path.__len__() > 0:
            selection_mode = None
        else:
            selection_mode = "both"
        current_doc = pl_path_t(current_path).resolve()
        if selection_mode is None:
            if current_doc.is_dir():
                selection_mode = "folder"
            elif current_doc.is_file():
                selection_mode = "document"
            else:
                selection_mode = "both"

        # # noinspection PyArgumentList
        # file_dialog = qw_.QFileDialog(self)
        # file_dialog.setDirectory(current_doc.parent.__str__())
        # file_dialog.selectFile(current_doc.__str__())

        if selection_mode == "folder":
            title = "Select Folder"
            # file_dialog.setWindowTitle("Select Folder")
            # file_dialog.setFileMode(qw_.QFileDialog.Directory)
        elif selection_mode == "document":
            title = "Select File"
            # file_dialog.setWindowTitle("Select File")
            # file_dialog.setFileMode(qw_.QFileDialog.ExistingFile)
        elif selection_mode == "both":
            title = "Select File or Folder"
            # file_dialog.setWindowTitle("Select File or Folder")
            # file_dialog.setFileMode(qw_.QFileDialog.AnyFile)
        else:
            raise RuntimeError("Contact Developer")

        # if text_t.IsPlainPath(self.type):
        #     dialog = file_dialog
        # else:
        #     dialog = file_dialog
        # dialog = qw_.QDialog(self)
        #
        # std_chooser = ch_.std_module_chooser_t.ForCategory(self.type)
        # if self.type is text_t.MARKED_POINT:
        #     save_std_choice_fct = lambda: self.SaveStandardTypeChoice(std_chooser, dialog)
        # elif self.type is text_t.QUALITY:
        #     save_std_choice_fct = lambda: self.SaveStandardQualityChoice(std_chooser, dialog)
        # else:
        #     save_std_choice_fct = lambda: self.SaveStandardFunctionChoice(std_chooser, dialog)
        # std_chooser.choice_validator.clicked.connect(save_std_choice_fct)
        #
        # layout = hbox_layout_t(dialog)
        # layout.addWidget(std_chooser)
        # layout.addWidget(file_dialog)
        # #
        # file_dialog.finished.connect(lambda result: dialog.done(result))

        if text_t.IsPlainPath(self.obj_mpp_type) and self.is_an_output:
            SelectedFile = fd_.SelectedOutputFile
        else:
            SelectedFile = fd_.SelectedInputFile
        selection = SelectedFile(
            title,
            title,
            mode=selection_mode,
            start_folder=current_doc.parent,
            initial_selection=current_doc,
        )
        if selection is None:
            return

        selection = selection.__str__()
        if text_t.IsPlainPath(self.obj_mpp_type):
            self.linedit_wgt.setText(selection)
        elif self.choice is None:  # Choice is not a standard module
            choice = selection
            if choice.endswith(".py"):
                if ("." in choice[:-3]) or (
                    " " in choice
                ):  # TODO: true python module name validation here
                    ShowCriticalMessage(
                        "Module Selection",
                        f"{choice}: Path must not contain dots or spaces",
                        self,
                    )
                    return

                self.linedit_wgt.setText(
                    ph_.basename(choice)
                )  # TODO: instead look for a marked_point_t descendent class and use its name here
                self.module_wgt.setText(choice)
            else:
                ShowCriticalMessage(
                    "Module Selection",
                    f"{choice}: Does not have the expected .py extension",
                    self,
                )
        else:
            if self.obj_mpp_type is text_t.MARKED_POINT:
                self.linedit_wgt.setText(self.choice)
            elif self.obj_mpp_type is text_t.QUALITY:
                module, quality = self.choice.split(".")
                self.linedit_wgt.setText(quality)
                self.module_wgt.setText(module)
            else:
                self.linedit_wgt.setText(self.choice)
            self.choice = None

    # def paintEvent(
    #     self, event: paint_event_t
    # ) -> None:  # QPaintEvent# PaintEventWithBorder(self, event) -> None:  # QPaintEvent
    #     #
    #     painter = painter_t(self)
    #     painter.SetPenColor("lightgray")
    #     painter.DrawRoundedRect(
    #         0, 0, self.GetWidth() - 1, self.GetHeight() - 1, 4.0, 4.0
    #     )
    #
    #     super().paintEvent(event)
