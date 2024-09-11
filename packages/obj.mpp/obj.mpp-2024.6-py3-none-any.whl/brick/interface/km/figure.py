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

import brick.interface.km.file_dialogs as fd_
import brick.interface.io.reporting as rp_
import brick.interface.io.storage as st_
from brick.data.type import array_t, number_h, pl_path_t

from typing import Any, Dict, Optional, Sequence, Tuple

import imageio as io_
import matplotlib as cm_
import matplotlib.cm as cm2
import matplotlib.pyplot as pl_
import matplotlib.widgets as wg_
import numpy as nmpy
import scipy.ndimage as im_
import skimage.measure as ms_
from matplotlib.backend_bases import FigureCanvasBase as canvas_t
from matplotlib.text import Annotation as base_annotation_t
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t
from mpl_toolkits.mplot3d import proj3d as pj_
from mpl_toolkits.axes_grid1.inset_locator import inset_axes as inset_axes_t


_CSV_SEPARATORS = (",", ".", ";", ":", "/", "|", "\\")

_ANNOTATION_TEXT_STYLE = {"fc": "yellow", "boxstyle": "round,pad=0.5", "alpha": 0.5}
_ANNOTATION_ARROW_STYLE = {"arrowstyle": "->", "connectionstyle": "arc3,rad=0"}
_ANNOTATION_STYLE = {
    "textcoords": "offset pixels",
    "fontsize": 9,
    "horizontalalignment": "center",
    "verticalalignment": "bottom",
    "bbox": _ANNOTATION_TEXT_STYLE,
    "arrowprops": _ANNOTATION_ARROW_STYLE,
}


button_press_event_t = Any  # Decprecated: canvas_t.button_press_event
button_release_event_t = Any  # Decprecated: canvas_t.button_release_event


class mkpt_figure_t:

    __slots__ = (
        "root",
        "grid",
        "main_axes",
        "buttons",
        "sep_slider",
        "mkpt_lst",
        "mkpt_lmp",
        "viewpoint_3D_status",
        "click_3D_position",
    )

    def __init__(self):
        #
        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in mkpt_figure_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def _NewWithGrid(
        cls, image: array_t, mkpt_lst: Optional[Sequence]
    ) -> mkpt_figure_t:
        #
        instance = cls()

        root = pl_.figure()
        root.set_layout_engine('constrained')
        root.get_layout_engine().set(wspace=0, hspace=0)#.set_constrained_layout_pads(wspace=0, hspace=0)
        instance.root = root

        grid = root.add_gridspec(nrows=3, ncols=6, height_ratios=[0.8, 0.17, 0.03])
        instance.grid = grid

        instance._AddSaveButtonsForImage(image, mkpt_lst)
        instance._AddSeparatorSlider()
        instance.mkpt_lst = mkpt_lst

        return instance

    @classmethod
    def NewFor2D(
        cls, image: array_t, mkpt_lst: Sequence = None, mkpt_lmp: array_t = None,
    ) -> mkpt_figure_t:
        #
        instance = cls._NewWithGrid(image, mkpt_lst)
        instance.mkpt_lmp = mkpt_lmp

        instance.main_axes = instance.root.add_subplot(
            instance.grid[0, :], label="main"
        )
        # Only to lighten code below
        axes = instance.main_axes

        axes.xaxis.tick_top()
        axes.set_ylabel("Row")
        axes.format_coord = lambda x, y: f"R:{int(y + 0.5)},C:{int(x + 0.5)}"

        if (mkpt_lst is not None) and (mkpt_lmp is not None):
            _ = instance.root.canvas.mpl_connect(
                "button_press_event", instance._On2DButtonPress,
            )

        return instance

    @classmethod
    def NewFor3D(cls, image: array_t, mkpt_lst: Sequence = None,) -> mkpt_figure_t:
        #
        instance = cls._NewWithGrid(image, mkpt_lst)

        instance.main_axes = instance.root.add_subplot(
            instance.grid[0, :], label="main", projection=axes_3d_t.name
        )
        # Only to lighten code below
        axes = instance.main_axes

        axes.set_xlim(left=0, right=image.shape[0])
        axes.set_ylim(bottom=0, top=image.shape[1])
        axes.set_zlim(bottom=0, top=image.shape[2])

        coords = ("x", "y", "z")
        labels = ("X=Row", "Y=Col", "Z=Depth")
        colors = ("red", "green", "blue")
        for axis_lbl, label, color in zip(coords, labels, colors):
            labeling_fct = getattr(axes, f"set_{axis_lbl}label")
            axis = getattr(axes, axis_lbl + "axis")

            labeling_fct(label)
            axis.label.set_color(color)
            axis.line.set_color(color)
            axes.tick_params(axis_lbl, colors=color)

        instance.viewpoint_3D_status = axes.text2D(
            0, 1, f"Az={axes.azim}, El={axes.elev}", transform=axes.transAxes,
        )

        canvas = instance.root.canvas
        _ = canvas.mpl_connect("button_press_event", instance._On3DButtonPress)
        _ = canvas.mpl_connect("button_release_event", instance._On3DButtonRelease)

        return instance

    def _AddSaveButtonsForImage(
        self, image: array_t, mkpt_lst: Optional[Sequence]
    ) -> None:
        #
        pl_.rc("font", size=8)

        all_arguments = (
            ("Save\nImage\nas PNG", "save image as png", image),
            ("Save\nImage\nas NPZ", "save image as npz", image),
            ("Save\nContour\nImage", "save contour image", mkpt_lst),
            ("Save\nRegion\nImage", "save region image", mkpt_lst),
            ("Save\nMarks\nas CSV", "save marks as csv", mkpt_lst),
            ("Save\nMarked\nPoints", "save marked points", mkpt_lst),
        )

        # Another Matplotlib nicety: despite countless attempts, this is the best I found to factorize button creation!
        if (mkpt_lst is not None) and (mkpt_lst[0].dim == 2):
            btn_save_0 = self._NewSaveButton(0, all_arguments[0])
        else:
            btn_save_0 = None
        btn_save_1 = self._NewSaveButton(1, all_arguments[1])
        if mkpt_lst is None:
            btn_save_2 = btn_save_3 = btn_save_4 = btn_save_5 = None
        else:
            btn_save_2 = self._NewSaveButton(2, all_arguments[2])
            btn_save_3 = self._NewSaveButton(3, all_arguments[3])
            btn_save_4 = self._NewSaveButton(4, all_arguments[4])
            btn_save_5 = self._NewSaveButton(5, all_arguments[5])

        # Only to keep a reference so that buttons remain responsive (see Button documentation)
        self.buttons = (
            btn_save_0,
            btn_save_1,
            btn_save_2,
            btn_save_3,
            btn_save_4,
            btn_save_5,
        )

    def _NewSaveButton(self, position: int, arguments: Tuple[str, str, Any]) -> Any:
        #
        button_room = self.root.add_subplot(self.grid[1, position], label=arguments[1])
        output = wg_.Button(button_room, arguments[0])
        output.on_clicked(
            lambda _: _OnSaveButtonClicked(arguments[1], arguments[2], self.sep_slider)
        )

        return output

    def _AddSeparatorSlider(self):
        #
        slider_room = self.root.add_subplot(self.grid[2, :], label="sep_slider")
        self.sep_slider = wg_.Slider(
            slider_room,
            "CSV Sep.",
            0,
            _CSV_SEPARATORS.__len__() - 1,
            valinit=0.0,
            valstep=1.0,
            valfmt="%d",
        )
        slider_room.xaxis.set_visible(True)
        slider_room.set_xticks(range(_CSV_SEPARATORS.__len__()))
        slider_room.set_xticklabels(_CSV_SEPARATORS)
        slider_room.tick_params(axis="x", direction="in", bottom=True, top=True, labelsize=12)

    def Plot2DImage(self, image: array_t) -> None:
        #
        # matshow cannot be used since image is normally RGB here
        self.main_axes.imshow(image)

    def PlotVoxels(self, image: array_t) -> None:
        #
        self.main_axes.voxels(image, facecolors="#1f77b430")

    def PlotIsosurface(self, image: array_t) -> None:
        #
        binary_map = (image > 0.0).astype(nmpy.float16)
        vertices, faces, _, _ = ms_.marching_cubes(binary_map, 0.5)

        dilated_image = im_.grey_dilation(image, size=(3, 3, 3))
        rounded_vertices = nmpy.around(vertices).astype(nmpy.uint16)
        one_v_per_f = rounded_vertices[faces[:, 0], :]
        face_values = dilated_image[tuple(one_v_per_f[:, idx] for idx in range(3))]
        ValueToColor = cm2.get_cmap("gist_rainbow")
        face_colors = ValueToColor(face_values)

        poly_collection = self.main_axes.plot_trisurf(
            vertices[:, 0],
            vertices[:, 1],
            faces,
            vertices[:, 2],
            edgecolor="k",
            linewidth=0.15,
        )
        # Passing facecolors to plot_trisurf does not work!
        poly_collection.set_facecolors(face_colors)

    def PlotAnnotations(self, locrup: int) -> None:
        #
        font_dct = {
            "family": "monospace",
            "color": "red",
            "size": 8,
            "va": "center",
        }

        # https://matplotlib.org/api/text_api.html#matplotlib.text.Text.get_window_extent
        for mkpt in self.mkpt_lst:
            h_offset = (mkpt.bbox.maxs[1] - mkpt.bbox.mins[1] + 1) // 4
            self.main_axes.text(
                mkpt.position[1] - h_offset,
                mkpt.position[0],
                mkpt.runtime_uid[locrup:],
                fontdict=font_dct,
            )

    def AddColorbar(self, quality_details: Dict[str, Any], dim: int) -> None:
        #
        max_n_ticks = 7

        uninfinitized = nmpy.sort(quality_details["uninfinitized"])
        pushed_to_1 = quality_details["pushed_to_1"]

        n_uninfinitized = uninfinitized.__len__()
        if n_uninfinitized < 2:
            return

        if dim == 2:
            colors = nmpy.zeros((pushed_to_1.__len__(), 4), dtype=nmpy.float64)
            colors[:, 3] = 1.0
            colors[:, 0] = pushed_to_1[::-1]
            colormap = cm_.colors.ListedColormap(colors)
            container = inset_axes_t(
                self.main_axes,
                width="5%",
                height="100%",
                loc="right",
                bbox_to_anchor=(0.075, 0, 1, 1),
                bbox_transform=self.main_axes.transAxes,
                borderpad=0,
            )
            axes = None
        else:
            ValueToColor = cm2.get_cmap("gist_rainbow")
            colormap = cm_.colors.ListedColormap(ValueToColor(pushed_to_1[::-1]))
            container = None
            axes = self.main_axes

        if n_uninfinitized > max_n_ticks:
            step = (n_uninfinitized - 1) / (max_n_ticks - 1)
            kept_idc = nmpy.fromiter(
                (round(factor * step) for factor in range(max_n_ticks)),
                dtype=nmpy.uint64,
            )
            ticks = uninfinitized[nmpy.unique(kept_idc)]
        else:
            ticks = uninfinitized

        if n_uninfinitized > 1:
            centers = (
                0.5 * (uninfinitized[: (n_uninfinitized - 1)] + uninfinitized[1:])
            ).tolist()
            normalization = cm_.colors.BoundaryNorm(
                [uninfinitized[0]] + centers + [uninfinitized[-1]], n_uninfinitized
            )
        else:
            normalization = cm_.colors.NoNorm(
                vmin=uninfinitized[0], vmax=uninfinitized[-1]
            )

        # The creation of axes for the colorbar disturbs the layout, regardless of use_gridspec. In 3D, this does not
        # make much of a difference, but in 2D the layout becomes ugly. Hence the container hack in 2D.
        colorbar = self.root.colorbar(
            cm2.ScalarMappable(cmap=colormap, norm=normalization),
            cax=container,
            ax=axes,
            ticks=ticks,
            spacing="proportional",
            label="Quality",
        )
        colorbar.set_ticks(ticks)
        colorbar.ax.tick_params(axis="y", direction="inout")
        # This is necessary only because of the container hack
        colorbar.ax.zorder = -10

    def _On2DButtonPress(self, event: button_press_event_t) -> None:
        #
        if event.inaxes == self.main_axes:
            row = int(event.ydata + 0.5)
            col = int(event.xdata + 0.5)
            mkpt_lbl = self.mkpt_lmp[row, col]

            if mkpt_lbl > 0:
                mkpt = self.mkpt_lst[mkpt_lbl - 1]
                text, reference, offset = _MKPTAnnotation(mkpt)
                self.main_axes.annotate(
                    text, xy=reference, xytext=offset, **_ANNOTATION_STYLE,
                )
                event.canvas.draw_idle()

                return

        self._RemoveAllAnnotations(event.canvas)

    def _On3DButtonPress(self, event: button_press_event_t) -> None:
        #
        self.click_3D_position = (event.x, event.y)

    def _On3DButtonRelease(self, event: button_release_event_t) -> None:
        #
        if (event.x, event.y) == self.click_3D_position:
            idx_o_closest = self._MKPTClosestToEvent(event)
            if idx_o_closest is None:
                self._RemoveAllAnnotations(event.canvas)
            else:
                self._Annotate3DMKPT(event.canvas, idx_o_closest)
        else:
            self.viewpoint_3D_status.set_text(
                f"Az={int(round(self.main_axes.azim))}, El={int(round(self.main_axes.elev))}"
            )
            event.canvas.draw_idle()

    def _Annotate3DMKPT(self, canvas: canvas_t, idx: int) -> None:
        #
        text, reference, offset = _MKPTAnnotation(self.mkpt_lst[idx])
        annotation = annotation_t(
            text, xyz=reference, xytext=offset, **_ANNOTATION_STYLE,
        )
        self.main_axes.add_artist(annotation)

        canvas.draw_idle()

    def _RemoveAllAnnotations(self, canvas: canvas_t) -> None:
        #
        any_removed = False
        for child in self.main_axes.get_children():
            # Leave base_annotation_t here (as opposed to annotation_t) so that it works for both 2-D and 3-D
            if isinstance(child, base_annotation_t):
                child.remove()
                any_removed = True
        if any_removed:
            canvas.draw_idle()

    def _MKPTClosestToEvent(self, event: button_release_event_t) -> Optional[int]:
        #
        sq_distances = tuple(
            self._EventToPointSqDistance(event, mkpt.position) for mkpt in self.mkpt_lst
        )
        min_sq_distance = min(sq_distances)
        output = nmpy.argmin(sq_distances).item()

        half_sq_lengths = (
            (length / 2) ** 2 for length in self.mkpt_lst[output].bbox.lengths
        )
        if min_sq_distance > max(half_sq_lengths):
            return None

        return output

    def _EventToPointSqDistance(
        self, event: button_release_event_t, point_3D: array_t
    ) -> float:
        #
        x2_01, y2_01, _ = pj_.proj_transform(*point_3D, self.main_axes.get_proj())
        x2, y2 = self.main_axes.transData.transform((x2_01, y2_01))

        return (x2 - event.x) ** 2 + (y2 - event.y) ** 2


# Ideally, this class should not be necessary, but somehow, something working when outside a custom figure class
# (rotation of annotations with axes) does not work here.
class annotation_t(base_annotation_t):
    #
    def __init__(self, text: str, xyz: Tuple[number_h, ...] = None, **kwargs):
        #
        super().__init__(text, xy=(0, 0), **kwargs)
        self._verts3d = xyz

    def draw(self, renderer) -> None:
        #
        xs, ys, _ = pj_.proj_transform(*self._verts3d, self.axes.M)
        self.xy = (xs, ys)
        super().draw(renderer)


def _MKPTAnnotation(mkpt) -> Tuple[str, Tuple[number_h, ...], Tuple[number_h, ...]]:
    #
    bbox_lengths = mkpt.bbox.lengths

    if bbox_lengths.__len__() == 2:
        reference = tuple(reversed(mkpt.position))
        offset = (0.5 * bbox_lengths[1] + 10, 0.5 * bbox_lengths[0] + 15)
    else:
        reference = mkpt.position
        single_offset = 3 * max(tuple(0.5 * length + 5 for length in bbox_lengths))
        offset = 2 * (single_offset,)

    pos_as_str = ", ".join(f"{elm:.2f}" for elm in mkpt.position)
    marks_as_str = "/".join(elm.__str__() for elm in mkpt.raw_marks)
    annotation = f"Q={mkpt.quality:.3f}\n" f"{pos_as_str}\n" f"{marks_as_str}"

    return annotation, reference, offset


def _OnSaveButtonClicked(operation: str, data: Any, sep_slider) -> None:
    #
    if operation == "save image as png":
        img_path = _SavePath("Image", "Image", "Image", "png")
        if img_path is not None:
            io_.imwrite(
                img_path, nmpy.around(255.0 * data).astype("uint8"),
            )
    elif operation == "save image as npz":
        img_path = _SavePath("Image Array", "Image Array", "Numpy", "npz")
        if img_path is not None:
            nmpy.savez_compressed(img_path, data)
    elif operation == "save contour image":
        mkpt_dim = data[0].dim
        if mkpt_dim == 2:
            extension = "png"
        else:
            extension = "tif"
        img_path = _SavePath("Contour Image", "Contour Image", "Image", extension)
        if img_path is not None:
            st_.SaveDetectionAsContourImage(mkpt_dim, data, None, None, img_path)
    elif operation == "save region image":
        mkpt_dim = data[0].dim
        if mkpt_dim == 2:
            extension = "png"
        else:
            extension = "tif"
        img_path = _SavePath("Region Image", "Region Image", "Image", extension)
        if img_path is not None:
            st_.SaveDetectionAsRegionImage(mkpt_dim, data, None, None, img_path)
    elif operation == "save marks as csv":
        csv_path = _SavePath("Marks", "Marks", "CSV", "csv")
        if csv_path is not None:
            st_.SaveDetectionInCSVFormat(
                data, None, None, csv_path, sep=_CSV_SEPARATORS[int(sep_slider.val)]
            )
    elif operation == "save marked points":
        json_path = _SavePath("Marked Points", "Marked Points", "JSON", "json")
        if json_path is not None:
            st_.SaveDetectionInFormatForRebuilding(data, None, None, json_path)
    else:
        raise rp_.BugException()


def _SavePath(
    for_title: str, for_message: str, for_filter: str, extension: str
) -> Optional[pl_path_t]:
    #
    save_path = fd_.SelectedOutputFile(
        f"Save {for_title} as {extension.upper()}",
        f"Select a {extension.upper()} Name for the {for_message}",
        mode = "document",
        allowed_types = {f"{for_filter} files": (extension, extension.upper())},
    )

    return save_path
    # if save_path is not None:
    #     if save_path.suffix.lower() != f".{extension}":
    #         save_path = save_path.with_suffix(f".{extension}")
    #
    #     if fd_.ContinueDespitePotentialOverwriting(save_path):
    #         return save_path
    #
    # return None
