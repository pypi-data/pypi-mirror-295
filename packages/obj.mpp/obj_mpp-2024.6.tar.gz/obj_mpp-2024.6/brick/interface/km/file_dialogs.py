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

from typing import Dict, Optional, Sequence, Tuple, Union

from brick.data.type import pl_path_t
from brick.interface.km.library.pyqt5 import (
    DIALOG_ACCEPT_OPEN,
    DIALOG_ACCEPT_SAVE,
    DIALOG_ACCEPTATION,
    DIALOG_AUTO_OWERWRITE,
    DIALOG_MODE_ANY,
    DIALOG_MODE_EXISTING_FILE,
    DIALOG_MODE_FOLDER,
    ShowErrorMessage,
    file_selection_widget_t,
    widget_event_loop_t,
)


"""
allowed_types: {"Type": "extension", "Type": ("extension", "extension",...), ...}
filter: "Image files (*.png *.xpm *.jpg);Text files (*.txt);Any files (*)"
"""


allowed_type_t = Dict[str, Union[str, Sequence[str]]]


def SelectedInputFile(
    title: str,
    caption: str,
    /,
    *,
    mode: str = "both",
    allowed_types: allowed_type_t = None,
    start_folder: Union[str, pl_path_t] = None,
    initial_selection: Union[str, pl_path_t] = None,
) -> Optional[pl_path_t]:
    #
    _EnsureAQAppIsRunning()

    extension_filter, _ = _AllowedTypesElements(allowed_types)
    check_existence = False
    if mode == "document":
        dialog_mode = DIALOG_MODE_EXISTING_FILE
    elif mode == "folder":
        dialog_mode = DIALOG_MODE_FOLDER
    elif mode == "both":
        # TODO: check if that allows to select a folder (documentation says "The name of a file, whether it exists or
        # not."), so a priori, no. But then how can we allow selection of either a file or a folder?
        dialog_mode = DIALOG_MODE_ANY
        check_existence = True
    else:
        raise ValueError(f"{mode}: Invalid mode")

    while True:
        dialog = _GenericFileDialog(
            title, caption, extension_filter, start_folder, initial_selection
        )
        dialog.SetAcceptMode(DIALOG_ACCEPT_OPEN)
        dialog.SetFileMode(dialog_mode)

        output = _SelectedFile(dialog)
        if output is None:
            return None
        if check_existence and not output.exists():
            ShowErrorMessage(f"{output}: Inexistent file or folder")
            start_folder = _StartFolderFromFolder(output)
            initial_selection = None
        else:
            # The file dialog does not allow to select either a file or a folder. So the solution here is to select a file,
            # and if a folder was needed, take the parent.
            if (mode == "folder") and output.is_file():
                output = output.parent
            return output


def SelectedOutputFile(
    title: str,
    caption: str,
    /,
    *,
    mode: str = "both",
    allowed_types: allowed_type_t = None,
    auto_overwrite: bool = False,
    start_folder: Union[str, pl_path_t] = None,
    initial_selection: Union[str, pl_path_t] = None,
) -> Optional[pl_path_t]:
    #
    _EnsureAQAppIsRunning()

    if mode not in ("document", "folder", "both"):
        raise ValueError(f"{mode}: Invalid mode")
    extension_filter, allowed_extensions = _AllowedTypesElements(allowed_types)

    while True:
        dialog = _GenericFileDialog(
            title, caption, extension_filter, start_folder, initial_selection
        )
        dialog.SetAcceptMode(DIALOG_ACCEPT_SAVE)
        dialog.SetFileMode(DIALOG_MODE_ANY)
        if auto_overwrite:
            dialog.SetOption(DIALOG_AUTO_OWERWRITE)

        output = _SelectedFile(dialog)
        if output is None:
            return None
        # The file dialog does not allow to select either a file or a folder. So the solution here is to select a file,
        # and if a folder was needed, take the parent. See (*) below.
        if (mode == "folder") and output.exists() and output.is_file():
            output = output.parent

        erroneous_selection = False
        if output.exists():
            if (mode == "document") and not output.is_file():
                ShowErrorMessage(f"{output}: Not of regular file")
                erroneous_selection = True
            # Unnecessary due to (*) above
            # elif (mode == "folder") and not output.is_dir():
            #     ShowErrorMessage(f"{output}: Not a folder")
            #     erroneous_selection = True

        if not erroneous_selection:
            if ("*" in allowed_extensions) or (
                output.suffix.lower()[1:] in allowed_extensions
            ):
                return output
            else:
                ShowErrorMessage(f"{output}: Extension is not valid")

        start_folder = _StartFolderFromFolder(output)
        initial_selection = None


# def ContinueDespitePotentialOverwriting(path: pl_path_t) -> bool:
#     #
#     if path.exists():
#         # noinspection PyArgumentList
#         overwriting_dialog = qw_.QMessageBox()
#         overwriting_dialog.setWindowTitle("File Overwriting Confirmation")
#         overwriting_dialog.setText(f"{path.__str__()}:\nFile already exists.")
#         overwriting_dialog.setInformativeText("Do you want to overwrite it?")
#         overwriting_dialog.setStandardButtons(
#             qw_.QMessageBox.Cancel | qw_.QMessageBox.Save
#         )
#         overwriting_dialog.setDefaultButton(qw_.QMessageBox.Cancel)
#
#         return overwriting_dialog.exec_() == qw_.QMessageBox.Save
#
#     return True


def _EnsureAQAppIsRunning() -> None:
    #
    if widget_event_loop_t.GetInstance() is None:
        _ = widget_event_loop_t([])  # Empty sys.argv
        # Initially, there was a tuple argument: (f"Launched-From-{__name__}",).
        # But PySide2 complains about not being of type typing.Sequence[str].


def _AllowedTypesElements(
    allowed_types: Optional[allowed_type_t],
) -> Tuple[str, Tuple[str]]:
    """"""
    if allowed_types is None:
        return "Any file or folder (*)", ("*",)

    types = []
    extensions = []
    filters = []
    for _type, extension in allowed_types.items():
        types.append(_type)
        if isinstance(extension, str):
            extensions.append(extension)
            if extension == "*":
                new_extensions = ("*",)
            else:
                new_extensions = (f"*.{extension}",)
        else:
            extensions.extend(extension)
            new_extensions = tuple(f"*.{_ext}" for _ext in extension)
        filters.append(f"{_type.title()} ({' '.join(new_extensions)})")

    return ";".join(filters), tuple(extensions)


def _StartFolderFromFolder(folder: pl_path_t) -> Optional[pl_path_t]:
    """"""
    output = folder

    root = folder.root
    while (output != root) and (not output.exists()):
        output = output.parent
    if output == root:
        output = None

    return output


def _GenericFileDialog(
    title: str,
    caption: str,
    extension_filter: str,
    start_folder: Union[str, pl_path_t],
    initial_selection: Union[str, pl_path_t],
) -> file_selection_widget_t:
    #
    # noinspection PyArgumentList
    output = file_selection_widget_t(caption, extension_filter=extension_filter)
    output.SetWindowTitle(title)
    if start_folder is not None:
        output.SetDirectory(start_folder.__str__())
    if initial_selection is not None:
        output.SelectFile(initial_selection.__str__())

    return output


def _SelectedFile(dialog: file_selection_widget_t) -> Optional[pl_path_t]:
    #
    status = dialog.RunAndGetClosingStatus()
    if status == DIALOG_ACCEPTATION:
        return pl_path_t(dialog.SelectedFile())

    return None
