#!/usr/bin/env python3

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

import sys as sy_
from typing import Optional, Tuple

import skimage.io as io_
from brick.interface.ko.config import CommandLineParser

import brick.interface.io.config as iocf
import brick.interface.io.reporting as mg_
import brick.interface.km.file_dialogs as fd_
from brick.interface.km.prm_component.input_bool import bool_wgt_t
from brick.config.config import config_t, raw_config_h
from brick.config.parameter import parameter_t
from brick.config.section import NonDefaultUnits
from brick.data.config.dependencies import PARENT_PRM_OF_SECTION
from brick.data.config.std_labels import std_label_e
from brick.data.interface.category_translations import CATEGORY_TRANSLATIONS
from brick.data.type import pl_path_t
from brick.interface.km.image import image_container_t
from brick.interface.km.library.pyqt5 import (
    FIXED_SIZE,
    SIZE_EXPANDING,
    SIZE_MINIMUM,
    TAB_POSITION_EAST,
    button_widget_t,
    grid_layout_t,
    hbox_layout_t,
    label_widget_t,
    patience_window_t,
    scroll_container_t,
    tab_widget_t,
    vbox_layout_t,
    widget_event_loop_t,
    widget_t,
)
from brick.interface.km.prm_component.comment import prm_comment_t
from brick.interface.km.section import controlled_section_t, section_t
from brick.interface.km.status_area import status_area_t


# TODO: At least part of the graphics code is a mess, maybe more than a part. Review and improve some day
# TODO: use the Qt signal&slot approach instead of storing widget dependencies (wherever possible)


_ADVANCED_MODE_OPTION_NAME = "advanced-mode"


class stdout_redirector_t:
    stdout = sy_.stdout
    messages = []

    def Start(self)->None:
        """"""
        sy_.stdout = self

    def Stop(self)->None:
        """"""
        sy_.stdout = self.stdout

    def write(self, text:str, /)->None:
        """"""
        self.messages.append(text)


class detector_t(widget_t):
    #
    # Defining __slots__ makes Qt crash (or might be a bug with self.__class__.__slots__ on derived class)
    __slots__ = (
        "ini_document",
        "sections",
        "status_area",
        "image",
    )

    def __init__(self) -> None:
        #
        super().__init__()
        self.setWindowTitle("Obj.MPP Detector")

        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in detector_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def FromConfig(
        cls, config: config_t, advanced_mode: bool = False
    ) -> Optional[detector_t]:
        #
        instance = cls()

        # --- Top-level widgets
        title = (
            '<font color="green"><b>Obj.MPP</b>: '
            "Object/pattern detection using a Marked Point Process</font><br/>"
            "<i>Object Detector</i>"
        )
        category_selector = tab_widget_t()
        runtime_area = tab_widget_t()
        advanced_mode_lyt = _AdvancedModeLayout(advanced_mode, instance)
        button_lyt, button_close = _ActionButtonsAndLayouts(
            config.ini_document is not None, instance
        )

        # --- (N-1)-level widgets
        status_area = status_area_t("Parameter Description")
        prm_comment_t.SetCommentArea(status_area)

        image = image_container_t()
        image.SetSizePolicy(FIXED_SIZE, FIXED_SIZE)
        image.SetScaledContents(True)
        if config.ini_document is not None:
            image.SetImage(io_.imread(config[std_label_e.sct_signal]["signal_path"]))

        runtime_area.AddTab(status_area, "Details")
        runtime_area.AddTab(image, "Image")
        runtime_area.SetTabPosition(TAB_POSITION_EAST)

        # --- Sections
        categories = {}
        sections = {}
        ordered_sections = []
        for category in CATEGORY_TRANSLATIONS.keys():
            for section in config.values():
                if section.category == category:
                    ordered_sections.append(section)
        for section in ordered_sections:
            section_name = section.name
            category_name = CATEGORY_TRANSLATIONS[section.category]

            if section_name == std_label_e.sct_range_units:
                section = NonDefaultUnits(section)

            if category_name not in categories:
                categories[category_name] = widget_t(parent=None)
                categories[category_name].setLayout(vbox_layout_t())
                scroll_area = scroll_container_t()
                scroll_area.setWidget(categories[category_name])
                scroll_area.setWidgetResizable(True)
                category_selector.AddTab(scroll_area, category_name)

            if section_name in PARENT_PRM_OF_SECTION:
                # Optional sections are not in section
                parent_section, parent_prm = PARENT_PRM_OF_SECTION[section_name]
                if parent_section not in sections:
                    raise RuntimeError("Contact Developer Please")
                # /!\ This means that child sections must be created after their controlling parameters
                parameter = sections[parent_section][parent_prm]
                visual_section = controlled_section_t.ForSection(
                    section,
                    parameter,
                )
            else:
                # for p in section:
                #     print("CREATING...", p)
                visual_section = section_t.ForSection(section)
            categories[category_name].layout().AddWidget(visual_section)
            sections[section_name] = visual_section

        # --- Layout...
        layout = grid_layout_t()
        layout.AddWidget(label_widget_t(title), 0, 0, 1, 1)
        layout.AddWidget(category_selector, 1, 0, 1, 1)
        layout.addLayout(advanced_mode_lyt, 2, 0, 1, 1)
        layout.AddLayout(button_lyt, 3, 0, 1, 1)
        layout.AddWidget(runtime_area, 0, 1, 3, 1)
        layout.AddWidget(button_close, 3, 1, 1, 1)

        layout.SetColumnStretch(0, 2)
        # status_area.setWidth(categories.width())

        instance.SetLayout(layout)
        # --- ...Layout

        instance.ini_document = config.ini_document
        instance.sections = sections
        instance.status_area = status_area
        instance.image = image

        instance.ToggleAdvancedMode(advanced_mode)

        return instance

    # def Sections(self) -> Iterator:
    #     """"""
    #     tabs = tuple(
    #         self.category_selector.widget(idx)
    #         for idx in range(self.category_selector.count())
    #     )
    #     for tab in tabs:
    #         for section in tab.findChildren(base_section_t):
    #             yield section

    def ToggleAdvancedMode(self, advanced_mode: bool) -> None:
        """"""
        for section in self.sections.values():  # .Sections():
            if section.details.basic:
                should_check_parameters = True
            elif advanced_mode:
                section.setVisible(True)
                should_check_parameters = True
            else:
                section.setVisible(False)
                should_check_parameters = False

            if should_check_parameters:
                section_is_output = (section.details.name == std_label_e.sct_output)
                for parameter in section.ActiveParameters():
                    if section_is_output and (parameter.details.name == "result_output_function"):
                        continue

                    if not parameter.details.basic:
                        if advanced_mode:
                            parameter.SetVisible(True)
                        else:
                            parameter.SetVisible(False)

    def NewConfigFromInterface(self, _) -> raw_config_h:
        """
        /!\\ Remember that this should be raw: str keys and str values
        """
        # print("---------------", "HERE")
        output = {}

        for section in self.sections.values():  # Sections():
            section_as_dict = {}
            section_name = section.details.name
            # print("---------------", section_name)

            for parameter in section.ActiveParameters():
                # value = parameter.GetValue()
                value = parameter.text()
                # print("---------------", parameter.details.name, value)
                if value.__len__() > 0:
                    section_as_dict[parameter.details.name] = value

            output[section_name.value] = section_as_dict

        # if std_label_e.sct_mpp.value in output:
        #     # Disables parallel processing, just in case it disturbs the interaction with Qt (why?)
        #     output[std_label_e.sct_mpp.value]["n_parallel_workers"] = "1"

        return output

    def SaveConfig(self, new_ini: bool = None) -> None:
        #
        do_save = True

        if new_ini is None:
            raise ValueError(f"new_ini{mg_.SEP}Parameter should not be None")
        elif new_ini:
            doc_name = fd_.SelectedOutputFile(
                "Save Config As",
                "Save Config As",
                mode="document",
                allowed_types={"Obj.MPP config files": ("ini", "INI")},
            )
            if doc_name is None:
                do_save = False
            else:
                self.ini_document = doc_name
        else:
            pass  # Will overwrite self.ini_document

        if do_save:
            config = self.NewConfigFromInterface(None)
            iocf.WriteConfigToINIDocument(config, self.ini_document)

    def Run(self) -> None:
        #
        import tempfile as tp_

        import brick.marked_point.mkpt_list as ml_
        import mpp_detector_cli as dt_

        self.status_area.Clear()
        self.status_area.SetTitle("Obj.MPP Detection...")
        # self.image.ResetImage()  # At this point, the image is not set if GUI called w/o config

        # Turn external output off (it is also set invisible in the interface)
        arguments = {
            parameter_t.ParameterUId(
                std_label_e.sct_output, "result_output_function"
            ): "",
        }
        if self.ini_document is None:
            # The GUI has been launched w/o ini document as argument
            ini_document = "fake ini document"
        else:
            ini_document = self.ini_document
        config, config_is_valid, for_deferred_check = config_t.NewFromRawVersion(
            self.NewConfigFromInterface,
            from_file=ini_document,
            arguments=arguments,
        )

        img_path = config[std_label_e.sct_signal]["signal_path"]
        # print(config.AsRawDict())
        # print("PATH-----------------", img_path)
        try:
            image = io_.imread(img_path)
            # print("IMAGE-----------------", image.shape)
        except Exception as error:
            mg_.ReportE(
                "MKPT Detection",
                f"Image file: \"{img_path}\"\nError:\n{error}",
            )
            return
        self.image.SetImage(image)

        _, doc_name = tp_.mkstemp()
        doc_name = pl_path_t(doc_name)
        iocf.WriteConfigToINIDocument(config, doc_name)

        mg_.SetTarget(self.status_area, end_character="")
        # stdout_redirector = stdout_redirector_t()
        # stdout_redirector.Start()
        try:
            # For now, for_deferred_check is ignored in the GI version
            marked_points = dt_.RunDetector(config.AsRawDict(), {})
        except Exception as error:
            marked_points = None
            mg_.ReportE(
                "MKPT Detection",
                f"Config file: {doc_name}\nError:\n{error}",
            )
        # stdout_redirector.Stop()
        # self.status_area.contents.setPlainText("\n".join(stdout_redirector.messages))
        try:
            doc_name.unlink()
        except Exception as error:
            mg_.ReportE(
                str(doc_name),
                f"Cannot be removed with error:\n"
                f"{error}\n"
                f"Should be removed at next boot",
            )

        if not ((marked_points is None) or (marked_points.__len__() == 0)):
            keys = tuple(marked_points.keys())
            contour_map = ml_.ContourMapOfDetection(marked_points[keys[0]]) > 0
            self.image.DrawPoints(contour_map.nonzero(), (255, 0, 0))


def Main() -> None:
    """"""
    parser = CommandLineParser()
    arguments = parser.parse_args()
    ini_document = getattr(arguments, config_t.INI_DOCUMENT_OPTION)
    advanced_mode = _ADVANCED_MODE_OPTION_NAME in sy_.argv

    config, _, _ = config_t.NewFromRawVersion(
        iocf.RawConfigFromINIDocument, from_file=ini_document, arguments=arguments
    )
    if config is None:
        sy_.exit(1)

    event_loop = widget_event_loop_t(sy_.argv)
    patience_window = patience_window_t(event_loop)

    detector = detector_t.FromConfig(config, advanced_mode=advanced_mode)
    if detector is not None:
        detector.show()
        patience_window.finish(detector)
        end_status = event_loop.Run()
        sy_.exit(end_status)


def _AdvancedModeLayout(advanced_mode: bool, parent: detector_t) -> hbox_layout_t:
    """"""
    output = hbox_layout_t()

    boolean = bool_wgt_t.WithInitialValue(advanced_mode, mode="current")
    boolean.true_btn.toggled.connect(parent.ToggleAdvancedMode)

    output.addWidget(label_widget_t("<i>Advanced Mode</i>"))
    output.addWidget(boolean)

    return output


def _ActionButtonsAndLayouts(
    has_ini_document: bool, parent: detector_t
) -> Tuple[grid_layout_t, button_widget_t]:
    #
    buttons = []
    geometries = []

    button = button_widget_t("Save Config As")
    button.SetFunction(lambda: parent.SaveConfig(new_ini=True))
    buttons.append(button)
    if has_ini_document:
        geometries.append((0, 0, 1, 1))

        button = button_widget_t("Save Config (Overwriting)")
        button.SetFunction(lambda: parent.SaveConfig(new_ini=False))
        buttons.append(button)
        geometries.append((1, 0, 1, 1))
    else:
        geometries.append((0, 0, 2, 1))

    button = button_widget_t("Run")
    button.SetSizePolicy(SIZE_MINIMUM, SIZE_EXPANDING)
    button.SetFunction(parent.Run)
    buttons.append(button)
    geometries.append((0, 1, 2, 1))

    layout = grid_layout_t()
    for button, geometry in zip(buttons, geometries):
        layout.AddWidget(button, *geometry)
    layout.setContentsMargins(0, 0, 0, 0)

    button_close = button_widget_t("Close")
    button_close.SetSizePolicy(SIZE_MINIMUM, SIZE_MINIMUM)
    button_close.SetFunction(parent.Close)

    return layout, button_close


if __name__ == "__main__":
    #
    Main()


# class config_widget_t(widget_t):
#     @classmethod
#     def FromConfig(
#         cls, config: config_t, advanced_mode: bool = False
#     ) -> config_widget_t:
#         #
#         instance = cls(parent=None)
#
#         layout = grid_layout_t()
#         row = 0
#         for sct_name, sct_prms in config.visual_prms.items():
#             section_name = cs_.FormattedName(sct_name, "_").upper()
#             section_wgt = label_widget_t(f"<b>{section_name}</b>")
#             section_wgt.setMargin(10)
#             layout.AddWidget(section_wgt, row, 0, 1, 3, HCENTER_ALIGNED)
#             row += 1
#
#             for prm_name, prm_value in sct_prms.items():
#                 layout.AddWidget(prm_value.name, row, 0)
#                 layout.AddWidget(prm_value.type_selector, row, 1)
#                 layout.AddWidget(prm_value.input, row, 2)
#                 # prm_value.comment: Currently not used
#
#                 if prm_value.documentation is not None:
#                     prm_value.name.setToolTip(prm_value.documentation)
#                 if isinstance(prm_value.default_value, missing_required_prm_t):
#                     prm_value.input.setToolTip("No default value (mandatory parameter)")
#                 else:
#                     prm_value.input.setToolTip(
#                         f"Default value: {prm_value.default_value}"
#                     )
#
#                 row += 1
#
#         instance.setLayout(layout)
#
#         # Put scroll area creation at the end
#         # noinspection PyArgumentList
#         instance.scroll_area = scrollable_widget_t.NewForWidget(instance)
#
#         return instance
#
#     def show(self):
#         #
#         self.scroll_area.show()
