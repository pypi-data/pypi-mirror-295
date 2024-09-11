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

import itertools as it_
import pathlib as phlb
from typing import Callable, List, Optional, Sequence, Tuple, Union
import sys as sy_


import numpy as nmpy

# import PySide2.QtCharts as qh_
# import PyQt5.QtChart as qh_
import skimage.io as io_

import brick.interface.io.reporting as mg_
import brick.interface.km.file_dialogs as fd_
import brick.structure.explorer as ex_
from brick.data.marked_point.std_marks import mark_details_t
from brick.data.marked_point.twoD.std_marked_points import STD_MARKED_POINTS
from brick.data.type import array_t, number_h, pl_path_t
from brick.interface.km.image import image_container_t as base_image_container_t
from brick.interface.km.library.pyqt5 import (
    COLOR_CYAN,
    FIXED_SIZE,
    FORMAT_RICH,
    HCENTER_ALIGNED,
    KEY_CONTROL,
    KEY_M,
    KEY_META,
    KEY_SHIFT,
    TABLE_H_STRETCH,
    TRANSPARENT_TO_MOUSE,
    GetEventModifiers,
    ShowCriticalMessage,
    button_widget_t,
    combobox_widget_t,
    event_t,
    grid_layout_t,
    hbox_layout_t,
    label_widget_t,
    layout_t,
    paint_event_t,
    painter_t,
    point_t,
    single_input_widget_t,
    table_widget_t,
    vbox_layout_t,
    wheel_event_t,
    widget_event_loop_t,
    widget_t,
)
from brick.marked_point.generic import marked_point_t
from brick.signal.signal_context import signal_context_t


marks_h = Sequence[number_h]
update_marks_fct_h = Callable[[marks_h, int], None]
update_stats_fct_h = Callable[[marked_point_t, marks_h, bool], None]
mkpt_creation_fct_h = Callable[..., marked_point_t]


_KEY_MODIFIERS = ("+Sft", "+Ctl", "+Win")

_MOD_COMBINATIONS = [""]
for length in range(1, _KEY_MODIFIERS.__len__() + 1):
    _MOD_COMBINATIONS.extend(
        "[" + "".join(combination) + "]"
        for combination in it_.combinations(_KEY_MODIFIERS, length)
    )

_QUALITY_STATISTICS = ("Latest", "Min", "Mean", "Median", "Max")
_QUALITY_STATISTICS_FCT = (
    lambda qualities: qualities[-1],
    nmpy.min,
    nmpy.mean,
    nmpy.median,
    nmpy.max,
)


class qchooser_wdw_t(widget_t):
    #
    # Defining _slots makes Qt crash (or might be a bug with self.__class__._slots on derived class)
    _slots = (
        "_layout_mb_prm",  # mb=main>bottom
        "_layout_mbp_marks",  # mbp=main>bottom point (mark)
        "_canvas",
        "_static_info_zone",
        "_mpp_selector",
        "_mpp_selector_previous",
        "_quality_table",
        "_quality_chart",
        "_mkpt_classes",
        "_quality_classes",
        "_qualities",
    )

    def __init__(self) -> None:
        #
        super().__init__()
        # Do not use self.__class__._slots because it will be the parent slots in case of inheritance
        for slot in qchooser_wdw_t._slots:
            setattr(self, slot, None)

        self.SetWindowTitle("Obj.MPP Quality Chooser")

    @classmethod
    def WithImage(cls, img_path: Union[str, pl_path_t]) -> Optional[qchooser_wdw_t]:
        #
        instance = cls()

        # --- Layout Creation
        # layout_main --- objmpp_title
        #              |_ layout_m_btm --- layout_mb_img
        #                               |_ self._layout_mb_prm
        # layout_mb_img:
        #     - "Choose Image" button
        #     - self._canvas
        #     - dynamic_info_zone
        #     - self._static_info_zone
        # self._layout_mb_prm:
        #     - "Clear Marked Points" button
        #     - self._mpp_selector
        #     - current_marks_layout (one layout among self._layout_mbp_marks dict)
        #     - self._quality_table
        #     - quality_chart_wgt (whose chart() is stored in self._quality_chart)
        #     - "Exit" button
        # self._layout_mbp_marks: grid layout with name/current/min/max per mark
        layout_main = vbox_layout_t()
        layout_m_btm = hbox_layout_t()  # m=main, btm=bottom
        layout_mb_img = vbox_layout_t()  # mb=main>bottom
        instance._layout_mb_prm = vbox_layout_t()

        # --- Widget Creation
        # Simple widgets
        objmpp_title = label_widget_t(
            '<font color="green"><b>Obj.MPP</b>: '
            "Object/pattern detection using a Marked Point Process</font><br/>"
            "<i>Object Quality Chooser</i>",
            parent=None,
        )
        instance._static_info_zone = label_widget_t(parent=None)
        dynamic_info_zone = label_widget_t(parent=None)
        instance._canvas = image_container_t(
            instance,
            dynamic_info_zone,
            instance._UpdateMarksWithUpdatedMarks,
            instance._UpdateStatisticsWithNewMKPT,
        )

        # MKPT-related widgets
        instance._mkpt_classes = tuple(
            class_type
            for class_type in ex_.StandardMarkedPoints("class")
            if class_type.__name__[:-2] in STD_MARKED_POINTS
        )
        instance._mpp_selector = combobox_widget_t()
        instance._layout_mbp_marks = {}
        for class_type in instance._mkpt_classes:
            type_name = class_type.__name__[:-2]
            # noinspection PyArgumentList
            instance._mpp_selector.AddItem(type_name)
            instance._layout_mbp_marks[type_name] = grid_layout_t()
            for label, c_idx in zip(("Current", "Min", "Max"), range(1, 4)):
                instance._layout_mbp_marks[type_name].AddWidget(
                    label_widget_t(label), 0, c_idx
                )
            for mk_idx, (mk_name, _, __) in enumerate(
                _ElementsForMarkedPoint(class_type, read_only=True), start=1
            ):
                if mk_idx > 1:
                    mk_name.SetText(
                        mk_name.text() + " " + _MOD_COMBINATIONS[mk_idx - 1]
                    )
                else:
                    mk_name.SetStyleSheet("border: 1px solid darkgray")
                instance._layout_mbp_marks[type_name].AddWidget(mk_name, mk_idx, 0)
                for c_idx in range(1, 4):
                    instance._layout_mbp_marks[type_name].AddWidget(
                        label_widget_t(), mk_idx, c_idx
                    )
        instance._mpp_selector.SetFunction(instance._OnMarkedPointChanged)
        current_marks_layout = instance._layout_mbp_marks[
            instance._mpp_selector.Selection()
        ]
        instance._mpp_selector_previous = instance._mpp_selector.Selection()

        # Quality-related widgets: Statistics
        instance._quality_classes = ex_.StandardQualityFunctionInfos()
        instance._quality_table = table_widget_t(
            instance._quality_classes.__len__(), _QUALITY_STATISTICS.__len__()
        )
        instance._quality_table.SetHorizontalHeaderLabels(_QUALITY_STATISTICS)
        v_headers = []
        for idx, fun_class in enumerate(instance._quality_classes.values()):
            v_headers.append(fun_class[0].__name__[:-2])
        instance._quality_table.SetVerticalHeaderLabels(v_headers)
        instance._quality_table.SetHResizeMode(TABLE_H_STRETCH)

        # Quality-related widgets: Histograms
        # quality_chart_wgt = qh_.QtCharts.QChartView()
        # instance._quality_chart = quality_chart_wgt.chart()
        # instance._quality_chart.legend().setAlignment(RIGHT_ALIGNED)

        instance._quality_table.SetFixedHeight(
            instance._quality_table.GetHHeaderHeight()
            + instance._quality_table.GetNRows()
            * instance._quality_table.GetRowHeight()
        )
        instance._static_info_zone.SetAlignment(HCENTER_ALIGNED)
        instance._static_info_zone.SetTextFormat(FORMAT_RICH)
        dynamic_info_zone.SetTextFormat(FORMAT_RICH)

        # --- Layout Arrangement
        layout_main.AddWidget(objmpp_title)
        layout_main.AddLayout(layout_m_btm)
        layout_m_btm.AddLayout(layout_mb_img)
        layout_m_btm.AddLayout(instance._layout_mb_prm)
        qchooser_wdw_t._AddButtonToLayout(
            layout_mb_img, "Choose Image", instance._ChooseReadAndShowImage
        )
        qchooser_wdw_t._AddButtonToLayout(
            instance._layout_mb_prm,
            "Clear Marked Points",
            instance._ClearMarkedPointsAndStatistics,
        )
        layout_mb_img.AddWidget(instance._canvas)
        layout_mb_img.AddWidget(dynamic_info_zone)
        layout_mb_img.AddWidget(instance._static_info_zone)
        instance._layout_mb_prm.AddWidget(instance._mpp_selector)
        instance._layout_mb_prm.AddLayout(current_marks_layout)
        instance._layout_mb_prm.AddWidget(instance._quality_table)
        # instance._layout_mb_prm.AddWidget(quality_chart_wgt)
        qchooser_wdw_t._AddButtonToLayout(
            instance._layout_mb_prm, "Exit", instance.close
        )
        instance.SetLayout(layout_main)

        # --- Data Preparation
        if not instance._ReadAndShowImage(img_path):
            return None
        instance._PrepareMarkedPointSelections()
        instance._ResetStatistics()

        # --- Interface Adjustments
        # noinspection PyArgumentList
        instance.Resize(instance._canvas.GetWidth() + 800, 400)
        instance.Center()

        return instance

    def _ChooseReadAndShowImage(self, _: bool = False) -> None:
        #
        img_path = _ImagePathFromChooser()
        if img_path is None:
            return

        _ = self._ReadAndShowImage(img_path)
        self._ResetStatistics()

    def _ReadAndShowImage(self, img_path: Union[str, pl_path_t]) -> bool:
        #
        if isinstance(img_path, str):
            img_path = phlb.Path(img_path)

        try:
            image = io_.imread(img_path)
        except Exception as error:
            # noinspection PyArgumentList
            ShowCriticalMessage(
                "Error Loading Image",
                f"{img_path.name}: Image cannot be loaded "
                f"from\n{img_path.parent}.\n\nMessage:\n{error}",
                parent=self,
            )
            return False

        if image.ndim not in (2, 3):
            # noinspection PyArgumentList
            ShowCriticalMessage(
                "Error Loading Image",
                f"{img_path.name}: Image cannot be loaded "
                f"from\n{img_path.parent}.\n\nMessage:\n{image.shape}: Invalid image size",
                parent=self,
            )
            return False

        img_lengths = image.shape
        self._canvas.SetImage(image)
        self._static_info_zone.SetText(
            f"{img_path.name} &mdash; w:{img_lengths[1]} &times; h:{img_lengths[0]}"
        )

        return True

    def _PrepareMarkedPointSelections(self) -> None:
        #
        class_name = self._mpp_selector.Selection()
        class_type = self._mkpt_classes[self._mpp_selector.SelectionIndex()]
        marks = self._canvas.UpdateMarkedPointCursor(
            0, 0, new_class_name=class_name, new_class_type=class_type
        )
        for idx in range(marks.__len__()):
            widget = (
                self._layout_mbp_marks[class_name].itemAtPosition(idx + 1, 1).widget()
            )
            widget.setText(round(marks[idx], 3).__str__())

    def _UpdateMarksWithUpdatedMarks(
        self, marks: marks_h, mod_combination: int
    ) -> None:
        #
        class_name = self._mpp_selector.Selection()
        widget = (
            self._layout_mbp_marks[class_name]
            .itemAtPosition(mod_combination + 1, 1)
            .widget()
        )
        widget.setText(round(marks[mod_combination], 3).__str__())

    def _UpdateStatisticsWithNewMKPT(
        self, mkpt: marked_point_t, marks: marks_h, positive_mkpt: bool
    ) -> None:
        #
        image = self._canvas.np_image
        if image.ndim == 3:
            image = nmpy.sqrt((image ** 2).sum(axis=-1))
        for fun_name, fun_class in self._quality_classes.items():
            # /!\ signal_for_qty should normally not be written to directly
            signals = fun_class[0].SignalsFromRawSignal(image, 2)
            signal_context_t.signal_for_qty = signals.signal_for_qty
            quality = fun_class[0].MKPTQuality(mkpt)
            # In order to force re-computation of quality with next quality function
            mkpt.quality = None
            self._qualities[fun_name.split(".")[1]].append((quality, positive_mkpt))

        if positive_mkpt:
            class_name = self._mpp_selector.Selection()
            layout_mbp_marks = self._layout_mbp_marks[class_name]
            for prm_idx, prm in enumerate(marks, start=1):
                min_label_wgt = layout_mbp_marks.itemAtPosition(prm_idx, 2).widget()
                max_label_wgt = layout_mbp_marks.itemAtPosition(prm_idx, 3).widget()
                current_min = min_label_wgt.text()
                current_max = max_label_wgt.text()
                if current_min.__len__() > 0:
                    current_min = float(current_min)
                    current_max = float(current_max)
                    if prm < current_min:
                        min_label_wgt.setText(round(prm, 3).__str__())
                    elif prm > current_max:
                        max_label_wgt.setText(round(prm, 3).__str__())
                else:
                    min_label_wgt.setText(round(prm, 3).__str__())
                    max_label_wgt.setText(round(prm, 3).__str__())

        # chart = self._quality_chart
        # chart.removeAllSeries()
        histogram_max = 0
        # quality_names = tuple(self._quality_classes.keys())

        # pn_=positive and negative
        for fun_idx, pn_qualities in enumerate(self._qualities.values()):
            positive_qualities = tuple(elm[0] for elm in pn_qualities if elm[1])
            if positive_qualities.__len__() > 0:
                for rdc_idx, reduce_fun in enumerate(_QUALITY_STATISTICS_FCT):
                    quality = round(reduce_fun(positive_qualities), 3)
                    # noinspection PyArgumentList
                    self._quality_table.SetItemAsStr(fun_idx, rdc_idx, str(quality))

            if pn_qualities.__len__() > 2:
                raw_qualities = tuple(elm[0] for elm in pn_qualities)
                # series = qh_.QtCharts.QLineSeries()
                # series.setName(quality_names[fun_idx].split(".")[1])
                quality_histogram, _ = nmpy.histogram(
                    raw_qualities, bins=min(raw_qualities.__len__(), 10)
                )
                # noinspection PyArgumentList
                histogram_max = max(histogram_max, quality_histogram.max())
                # for q_idx, n_elements in enumerate(quality_histogram, start=1):
                #     # 0.05*fun_idx: to avoid superimposition of the plots
                #     series.append(q_idx, n_elements + 0.05 * fun_idx)
                # chart.addSeries(series)

        # series = chart.series()
        # if series.__len__() > 0:
        #     chart.createDefaultAxes()
        #     h_axis, v_axis = chart.axes()
        #     h_axis.setTitleText("Bin index")
        #     h_axis.setTickCount(series[0].count())
        #     h_axis.setLabelFormat("%d")
        #     v_axis.setTitleText("Occurrences")
        #     v_axis.setRange(0, histogram_max)
        #     v_axis.setTickCount(histogram_max + 1)
        #     v_axis.setLabelFormat("%d")

    def _ResetStatistics(self) -> None:
        #
        for class_type in self._mkpt_classes:
            type_name = class_type.__name__[:-2]
            for mk_idx in range(1, class_type.marks_details.__len__() + 1):
                for c_idx in (2, 3):
                    self._layout_mbp_marks[type_name].itemAtPosition(
                        mk_idx, c_idx
                    ).widget().setText("")

        self._qualities = {}
        for fun_idx, fun_name in enumerate(self._quality_classes):
            self._qualities[fun_name.split(".")[1]] = []
            for rdc_idx in range(self._quality_table.GetNCols()):
                self._quality_table.SetItemAsStr(fun_idx, rdc_idx, "")

        # self._quality_chart.removeAllSeries()

    def _ClearMarkedPointsAndStatistics(self) -> None:
        #
        self._canvas.ResetImage()
        self._ResetStatistics()

    def _OnMarkedPointChanged(self, new_mkpt_class: int) -> None:
        #
        new_mkpt_class = self._mpp_selector.ItemAt(new_mkpt_class)

        previous_lyt = self._layout_mbp_marks[self._mpp_selector_previous]
        for idx in range(previous_lyt.count()):
            widget = previous_lyt.itemAt(idx).widget()
            if widget is not None:
                widget.setVisible(False)
        lyt_idx = self._layout_mb_prm.IndexOf(previous_lyt)
        self._layout_mb_prm.RemoveItem(previous_lyt)

        current_lyt = self._layout_mbp_marks[new_mkpt_class]
        for idx in range(current_lyt.count()):
            widget = current_lyt.itemAt(idx).widget()
            if widget is not None:
                widget.setVisible(True)
        self._layout_mb_prm.InsertLayout(lyt_idx, current_lyt)
        self._mpp_selector_previous = new_mkpt_class

        self._ClearMarkedPointsAndStatistics()
        self._PrepareMarkedPointSelections()

    def keyPressEvent(self, event: event_t, *args, **kwargs) -> None:
        #
        if event.key() == KEY_M:
            pass

    @staticmethod
    def _AddButtonToLayout(layout: layout_t, title: str, action: Callable) -> None:
        #
        button = button_widget_t(title)
        button.SetFunction(action)
        layout.AddWidget(button)


class image_container_t(base_image_container_t):
    #
    # Defining _slots makes Qt crash (or might be a bug with self.__class__._slots on derived class)
    _slots = (
        "class_name",
        "class_type",
        "field_len_height",
        "field_len_width",
        "img_height",
        "img_lengths",
        "img_width",
        "mkpt",
        "mkpt_half_size",
        "mkpt_mark_steps",
        "mkpt_marks",
        "_info_zone",
        "_ProcessUpdatedMKPT",
        "_ProcessNewMKPT",
    )

    def __init__(
        self,
        parent: widget_t,
        info_zone: label_widget_t = None,
        ProcessUpdatedMKPT: update_marks_fct_h = None,
        ProcessNewMKPT: update_stats_fct_h = None,
    ) -> None:
        #
        super().__init__(parent=parent)
        # Do not use self.__class__._slots because it will be the parent slots in case of inheritance
        for slot in image_container_t._slots:
            setattr(self, slot, None)

        # self.setBackgroundRole(qg_.QPalette.Base)
        # noinspection PyArgumentList
        self.SetSizePolicy(FIXED_SIZE, FIXED_SIZE)
        self.SetMouseTracking(True)
        self.SetAttribute(TRANSPARENT_TO_MOUSE, True)

        self._info_zone = info_zone
        self._ProcessUpdatedMKPT = ProcessUpdatedMKPT
        self._ProcessNewMKPT = ProcessNewMKPT

    def SetImage(self, image: array_t) -> Optional[str]:
        #
        error_msg = super().SetImage(image)
        if error_msg is not None:
            ShowCriticalMessage(
                "Image Display",
                error_msg,
                parent=self,
            )
            return None

        self.img_width = image.shape[1]
        self.img_height = image.shape[0]
        self.img_lengths = image.shape[:2]
        self.field_len_width = self.img_width.__str__().__len__()
        self.field_len_height = self.img_height.__str__().__len__()

        signal_context_t.Clear()
        signal_context_t.SetSignalsForQualityAndStatistics(self.img_lengths, None, None)

        self.setAttribute(TRANSPARENT_TO_MOUSE, False)

        return None

    def UpdateMarkedPointCursor(
        self,
        row: int,
        col: int,
        new_class_name: str = None,
        new_class_type: mkpt_creation_fct_h = None,
        new_marks: marks_h = None,
    ) -> Optional[marks_h]:
        """
        Qt coord. sys.: row=y (not -y), col=x
        """
        if new_class_name is None:
            if new_marks is None:
                raise mg_.BugException()
            mkpt_bbox_shape, contour_points, _, _ = _MarkedPointDetails(
                self.class_name, self.class_type, new_marks, self.img_lengths
            )
            if contour_points is None:
                return None
            self.mkpt_marks = new_marks
        else:
            if new_marks is not None:
                raise mg_.BugException()
            (
                mkpt_bbox_shape,
                contour_points,
                new_marks,
                new_mark_steps,
            ) = _MarkedPointDetails(
                new_class_name, new_class_type, None, self.img_lengths
            )
            self.class_name = new_class_name
            self.class_type = new_class_type
            # Cannot be factorized after if-else since required below
            self.mkpt_marks = new_marks
            self.mkpt_mark_steps = new_mark_steps

        self.mkpt_half_size = tuple(
            int(round(0.5 * mkpt_bbox_shape[_idx])) for _idx in range(2)
        )
        if self.mkpt is not None:
            self.mkpt.DetachAndRelease()
        self.mkpt = mkpt_cursor_t(
            row - self.mkpt_half_size[1],
            col - self.mkpt_half_size[0],
            mkpt_bbox_shape,
            contour_points,
            self,
        )

        return new_marks

    def enterEvent(self, _: event_t, *args, **kwargs) -> None:
        #
        self.mkpt.SetVisible(True)

    def leaveEvent(self, _: event_t, *args, **kwargs) -> None:
        #
        self.mkpt.SetVisible(False)

    def mouseMoveEvent(self, event: event_t, *args, **kwargs) -> None:
        #
        evt_x, evt_y = event.x(), event.y()
        row, col = self._RowColFromEventXY(evt_x, evt_y)

        self.mkpt.Move(evt_x - self.mkpt_half_size[1], evt_y - self.mkpt_half_size[0])
        if self._info_zone is not None:
            self._info_zone.SetText(
                f"<pre>TL+r&darr;{row:<{self.field_len_height}}+"
                f"c&rarr;{col:<{self.field_len_width}} / "
                f"BL+x&rarr;{col:<{self.field_len_width}}+"
                f"y&uarr;{self.img_height - row:<{self.field_len_height}} "
                f"= {self.np_image[row, col]}</pre>"
            )

    def mousePressEvent(self, event: event_t, *args, **kwargs) -> None:
        #
        row, col = self._RowColFromEventXY(event.x(), event.y())
        mkpt = self.class_type((row, col), *self.mkpt_marks, False)
        if mkpt.crosses_border:
            return

        positive_mkpt = event.modifiers().__int__() == 0
        if positive_mkpt:
            color = (0, 255, 128)
        else:
            color = (255, 0, 0)
        self.DrawPoints(
            self.mkpt.contour_points,
            color,
            bbox_width=mkpt.bbox.mins[1],
            bbox_height=mkpt.bbox.mins[0],
        )

        self._ProcessNewMKPT(mkpt, self.mkpt_marks, positive_mkpt)

    def wheelEvent(self, event: wheel_event_t, *args, **kwargs) -> None:
        """
        qc_.Qt.NoModifier, qc_.Qt.ShiftModifier, qc_.Qt.ControlModifier, qc_.Qt.MetaModifier: 0, 1, 2, 4
        """
        mods = GetEventModifiers(event)
        new_marks = list(self.mkpt_marks)  # list: to make a copy

        mod_combination = ""
        if (mods & KEY_SHIFT) > 0:
            mod_combination += _MOD_COMBINATIONS[1][1:-1]
        if (mods & KEY_CONTROL) > 0:
            mod_combination += _MOD_COMBINATIONS[2][1:-1]
        if (mods & KEY_META) > 0:
            mod_combination += _MOD_COMBINATIONS[3][1:-1]
        if mod_combination == "":
            mod_combination = 0
        else:
            mod_combination = _MOD_COMBINATIONS.index(f"[{mod_combination}]")
        mod_combination = min(mod_combination, new_marks.__len__() - 1)

        if event.angleDelta().y() > 0:
            new_marks[mod_combination] += self.mkpt_mark_steps[mod_combination]
        else:
            new_marks[mod_combination] -= self.mkpt_mark_steps[mod_combination]
        if (
            self.UpdateMarkedPointCursor(event.x(), event.y(), new_marks=new_marks)
            is not None
        ):
            self.mkpt.SetVisible(True)
            self._ProcessUpdatedMKPT(new_marks, mod_combination)


class mkpt_cursor_t(widget_t):
    #
    # Alt: https://doc.qt.io/qtforpython/PySide2/QtGui/QCursor.html?highlight=qcursor#PySide2.QtGui.QCursor
    #
    _slots = ("contour_points", "contour_gui_points")  # Defining slots makes Qt crash

    def __init__(
        self,
        row: int,
        col: int,
        domain_lengths: Sequence[int],
        contour_points: Tuple[array_t, array_t],
        parent: widget_t,
    ) -> None:
        #
        super().__init__(parent=parent)
        # Do not use self.__class__._slots because it will be the parent slots in case of inheritance
        for slot in mkpt_cursor_t._slots:
            setattr(self, slot, None)

        self.SetGeometry(row, col, domain_lengths[1], domain_lengths[0])
        self.SetAttribute(TRANSPARENT_TO_MOUSE, True)
        self.SetVisible(False)

        self.contour_points = contour_points
        self.contour_gui_points = tuple(
            point_t(point[1], point[0]) for point in zip(*contour_points)
        )

    def paintEvent(self, event: paint_event_t, *args, **kwargs) -> None:
        #
        painter = painter_t(self)
        painter.SetPenColor(COLOR_CYAN)
        painter.DrawPointSequence(self.contour_gui_points)


# TODO: replace this by input_stdelm one day
def _ElementsForMarkedPoint(mkpt_type: marked_point_t, read_only: bool = False) -> tuple:
    #
    return tuple(
        _ElementsForMark(name, details, read_only=read_only)
        for name, details in mkpt_type.marks_details.items()
    )


def _ElementsForMark(
    name: str, details: mark_details_t, read_only: bool = False
) -> tuple:
    #
    name_wgt = label_widget_t(name, parent=None)

    if details.default_range is None:
        hint = None
        initial_value = None
    else:
        left_symbol = "[" if details.min_inclusive else "]"
        right_symbol = "]" if details.max_inclusive else "["
        hint = f"{left_symbol}{details.min}, {details.max}{right_symbol}"
        initial_value = details.default_range[0]

    if isinstance(details.type, int) or isinstance(details.type, float):
        if initial_value is None:
            initial_value = ""
        else:
            initial_value = initial_value.__str__()
        if read_only:
            value_wgt = label_widget_t(initial_value, parent=None)
        else:
            value_wgt = single_input_widget_t(initial_value, parent=None)
            # https://doc-snapshots.qt.io/qtforpython/PySide2/QtWidgets/QLineEdit.html#PySide2.QtWidgets.PySide2.QtWidgets.QLineEdit.setValidator
            # https://doc-snapshots.qt.io/qtforpython/PySide2/QtWidgets/QLineEdit.html#PySide2.QtWidgets.PySide2.QtWidgets.QLineEdit.hasAcceptableInput
            if hint is not None:
                value_wgt.SetPlaceholderText(hint)
    else:
        value_wgt = None

    comment_wgt = None

    return name_wgt, value_wgt, comment_wgt


def _ImagePathFromChooser() -> Optional[Union[str, pl_path_t]]:
    #
    return fd_.SelectedInputFile(
        "Choose Image",
        "Choose Image",
        mode="document",
    )
    # # noinspection PyArgumentList
    # path, _ = qw_.QFileDialog.getOpenFileName(
    #     parent, "Choose Image", qc_.QDir.currentPath()
    # )
    #
    # if path.__len__() == 0:
    #     return None
    # else:
    #     return path


def _MarkedPointDetails(
    class_name: str,
    class_type: mkpt_creation_fct_h,
    marks: Optional[marks_h],
    img_lengths: Tuple[int, int],
) -> Tuple[
    Optional[Tuple[int, ...]],
    Optional[Tuple[array_t, array_t]],
    Optional[marks_h],
    Optional[List[number_h]],
]:
    #
    if marks is None:
        initial_radius = round(0.05 * min(*img_lengths)).__int__()
        if class_name == "circle":
            marks = [initial_radius]
            mark_steps = [1]
        elif class_name == "ellipse":
            marks = [initial_radius, 1.80, nmpy.pi / 10.0]
            mark_steps = [1, 0.05, nmpy.pi / 36.0]
        elif class_name == "square":
            marks = [initial_radius, nmpy.pi / 10.0]
            mark_steps = [1, nmpy.pi / 36.0]
        elif class_name == "rectangle":
            marks = [initial_radius, 1.80, nmpy.pi / 10.0]
            mark_steps = [1, 0.05, nmpy.pi / 36.0]
        elif class_name == "superquadric":
            marks = [initial_radius, 1.80, 2.0, 2.0, nmpy.pi / 10.0]
            mark_steps = [1, 0.05, 0.1, 0.1, nmpy.pi / 36.0]
        else:
            # Just in case there is a typo above
            raise ValueError(f"{class_name}{mg_.SEP}Invalid class name")
    else:
        mark_steps = None

    try:
        mkpt = class_type(
            (0.5 * img_lengths[0], 0.5 * img_lengths[1]),
            *marks,
            check_marks=True,
        )
    except (TypeError, ValueError):
        return None, None, None, None

    contour_points = mkpt.Contour().nonzero()

    return mkpt.bbox.lengths, contour_points, marks, mark_steps


def Main() -> None:
    """"""
    event_loop = widget_event_loop_t(sy_.argv)

    if sy_.argv.__len__() > 1:
        img_path = sy_.argv[1]
    else:
        img_path = _ImagePathFromChooser()
        if img_path is None:
            sy_.exit(0)

    main_wdw = qchooser_wdw_t.WithImage(img_path)
    if main_wdw is not None:
        main_wdw.show()
        end_status = event_loop.Run()
        sy_.exit(end_status)


if __name__ == "__main__":
    #
    Main()
