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

import brick.interface.io.reporting as rp_
import brick.interface.io.storage as st_
import brick.interface.io.mkpt_list as ml_
from brick.data.type import array_t, path_h, pl_path_t
from brick.interface.km.figure import mkpt_figure_t
from brick.marked_point.generic import marked_point_t
from brick.signal.constant import INFINITY_NUMPY_FLOAT

from typing import Any, Dict, Optional, Sequence

import imageio as io_
import matplotlib.pyplot as pl_
import numpy as nmpy
from PIL import Image, ImageDraw, ImageFont


def Output2DObjects(
    mkpt_lst: Sequence[marked_point_t],
    center_rng: tuple,
    background: array_t,
    plot_thickness: int = 1,
    with_annotations: bool = False,
    show_figure: bool = True,
    result_folder: path_h = ".",
    signal_id: str = "",
    date_as_str: str = "",
    img_basename: str = None,
) -> None:
    #
    # Must accept mkpt_lst and image as first 2 arguments, and date_as_str as optional argument
    #
    if not _BackgroundIsValid(background, 2):
        return

    quality_details = _NormalizedQualities(mkpt_lst)
    if with_annotations:
        locrup = ml_.LengthOfCommonRuntimeUIDPrefix(mkpt_lst)
    else:
        locrup = 0

    mkpt_lmp = nmpy.zeros(background.shape[:2], dtype=nmpy.uint16)
    output = _ColorOutputImage(background, 2)
    _DrawROIinColor(output, center_rng, 1, 1.0)
    _DrawMarkedPoints(
        output, mkpt_lmp, mkpt_lst, quality_details, True, 0, 1, plot_thickness,
    )

    # Plot here so that output is not altered with legend (see below)
    if show_figure:
        figure = mkpt_figure_t.NewFor2D(output, mkpt_lst=mkpt_lst, mkpt_lmp=mkpt_lmp)
        figure.Plot2DImage(output)
        figure.AddColorbar(quality_details, 2)
        if with_annotations:
            figure.PlotAnnotations(locrup)
        # But do not block with show() here to let saving below occur right away
    else:
        figure = None

    if (img_basename is not None) and (img_basename != ""):
        if with_annotations:
            _DrawAnnotationsInArray(output, mkpt_lst, locrup)

        if result_folder is None:
            result_folder = "."
        io_.imwrite(
            st_.OutputDocName(pl_path_t(result_folder), img_basename, "png", date_as_str, signal_id),
            nmpy.around(255.0 * output).astype("uint8"),
        )

    if show_figure:
        pl_.show()
        pl_.close(figure.root)


def Output3DObjects(
    mkpt_lst: Sequence[marked_point_t],
    center_rng: tuple,
    background: array_t,
    plot_thickness: int = 2,
    with_annotations: bool = False,
    show_figure: bool = True,
    result_folder: path_h = ".",
    signal_id: str = "",
    date_as_str: str = "",
    img_basename: str = None,
    threeD_engine: str = "matplotlib",  # Choices: matplotlib, mayavi
) -> None:
    #
    # Must accept mkpt_lst and image as first 2 arguments, and date_as_str as optional argument
    #
    if not _BackgroundIsValid(background, 3):
        return

    quality_details = _NormalizedQualities(mkpt_lst)

    if (img_basename is not None) and (img_basename != ""):
        output_color = _ColorOutputImage(background, 3)
        _DrawROIinColor(output_color, center_rng, 1, 1.0)
        _DrawMarkedPoints(
            output_color, None, mkpt_lst, quality_details, True, 0, 1, plot_thickness
        )

        if result_folder is None:
            result_folder = "."
        io_.volwrite(
            st_.OutputDocName(pl_path_t(result_folder), img_basename, "tif", date_as_str, signal_id),
            nmpy.around(255.0 * output_color).astype("uint8"),
        )

    if show_figure:
        figure = None
        ShowPendingFigures = lambda: True
        CloseFigure = lambda _: True
        output_grayscale = nmpy.zeros(background.shape[:3], dtype=nmpy.float64, order="C")

        if threeD_engine == "matplotlib":
            _DrawMarkedPoints(
                output_grayscale, None, mkpt_lst, quality_details, False, 0, 0, 0
            )

            figure = mkpt_figure_t.NewFor3D(output_grayscale, mkpt_lst=mkpt_lst)
            figure.PlotIsosurface(output_grayscale)
            figure.AddColorbar(quality_details, 3)
            ShowPendingFigures = pl_.show
            CloseFigure = lambda fig: pl_.close(fig.root)
        elif threeD_engine == "mayavi":
            # import mayavi.mlab as mv_
            _Plot3DObjectsWithMayavi(output_grayscale, background, mkpt_lst)
            # ShowPendingFigures = mv_.show
        else:
            raise ValueError(f"{threeD_engine}{rp_.SEP}Invalid 3-D engine")

        ShowPendingFigures()
        CloseFigure(figure)


def _BackgroundIsValid(image: array_t, expected_dim: int) -> bool:
    #
    if (image.ndim == expected_dim) or (
        (image.ndim == expected_dim + 1) and (image.shape[-1] == 3)
    ):
        return True

    rp_.ReportW(
        "Background",
        f"Invalid dimension: Actual_{image.ndim}; "
        f"Expected_{expected_dim}/Grayscale or {expected_dim+1}/Color. Displaying/Saving cancelled",
    )

    return False


def _NormalizedQualities(mkpt_lst: Sequence[marked_point_t],) -> Dict[str, Any]:
    #
    output = {}

    qualities = nmpy.array(tuple(mkpt.quality for mkpt in mkpt_lst))
    output["original"] = qualities.copy()

    inf_quality_bmap = nmpy.isinf(qualities)
    if inf_quality_bmap.all():
        qualities[qualities == -INFINITY_NUMPY_FLOAT] = 0.0
        qualities[qualities == INFINITY_NUMPY_FLOAT] = 1.0

        min_quality = min(qualities)
        max_quality = max(qualities)
        q_extent = max_quality - min_quality
    elif inf_quality_bmap.any():
        non_inf_qualities = qualities[nmpy.logical_not(inf_quality_bmap)]
        min_quality = min(non_inf_qualities)
        max_quality = max(non_inf_qualities)
        if max_quality == min_quality:
            quality_margin = 1.0
            q_extent = 2.0 * quality_margin
        else:
            q_extent = max_quality - min_quality
            # If qualities.size == 1.0, then max_quality == min_quality,
            # so the previous code path is taken instead.
            quality_margin = q_extent / (qualities.size - 1.0)
            q_extent += 2.0 * quality_margin

        qualities[qualities == -INFINITY_NUMPY_FLOAT] = min_quality - quality_margin
        qualities[qualities == INFINITY_NUMPY_FLOAT] = max_quality + quality_margin

        min_quality -= quality_margin
        max_quality += quality_margin
    else:
        min_quality, max_quality = min(qualities), max(qualities)
        q_extent = max_quality - min_quality

    if q_extent == 0.0:
        q_extent = 1.0
        # Hence, (qualities[idx] - min_quality) / q_extent == 1
        min_quality -= 1.0

    output["uninfinitized"] = qualities
    output["normalized"] = (qualities - min_quality) / q_extent
    output["pushed_to_1"] = 0.7 * output["normalized"] + 0.3

    return output


def _ColorOutputImage(background: array_t, image_dim: int) -> array_t:
    #
    bckgnd_is_grayscale = background.ndim == image_dim
    if bckgnd_is_grayscale:
        output = nmpy.empty((*background.shape, 3), dtype=nmpy.float64, order="C")
        for channel in range(3):
            output[..., channel] = background
    else:
        # Returns a copy, as desired
        output = background.astype(nmpy.float64)

    # noinspection PyArgumentList
    normalization_factor = background.max()
    if normalization_factor > 0.0:
        output /= normalization_factor

    return output


def _DrawMarkedPoints(
    image: array_t,
    labeled_map: Optional[array_t],
    mkpt_lst: Sequence[marked_point_t],
    quality_details: Dict[str, Any],
    in_color: bool,
    on_channel: int,
    off_channel: int,
    plot_thickness: int,
) -> None:
    #
    qualities = quality_details["pushed_to_1"]

    if in_color:
        target_image = image[..., on_channel]
    else:
        target_image = image

    for m_idx, (mkpt, quality) in enumerate(zip(mkpt_lst, qualities), start=1):
        mkpt.DrawInArray(
            target_image, thickness=plot_thickness, level=quality,
        )
        if in_color:
            mkpt.DrawInArray(
                image[..., off_channel], thickness=plot_thickness, level=0.0
            )

        if labeled_map is not None:
            labeled_map[mkpt.bbox.domain][mkpt.raw_region] = m_idx


def _DrawROIinColor(
    image: array_t, roi_rng: tuple, roi_channel: int, roi_value: float
) -> None:
    #
    if isinstance(roi_rng, tuple):
        if image.ndim == 3:
            image[roi_rng[0], roi_rng[2] : (roi_rng[3] + 1), roi_channel] = roi_value
            image[roi_rng[1], roi_rng[2] : (roi_rng[3] + 1), roi_channel] = roi_value
            image[roi_rng[0] : (roi_rng[1] + 1), roi_rng[2], roi_channel] = roi_value
            image[roi_rng[0] : (roi_rng[1] + 1), roi_rng[3], roi_channel] = roi_value
        else:
            image[
                roi_rng[0], roi_rng[2], roi_rng[4] : (roi_rng[5] + 1), roi_channel
            ] = roi_value
            image[
                roi_rng[1], roi_rng[3], roi_rng[4] : (roi_rng[5] + 1), roi_channel
            ] = roi_value
            image[
                roi_rng[0], roi_rng[2] : (roi_rng[3] + 1), roi_rng[4], roi_channel
            ] = roi_value
            image[
                roi_rng[1], roi_rng[2] : (roi_rng[3] + 1), roi_rng[5], roi_channel
            ] = roi_value
            image[
                roi_rng[0] : (roi_rng[1] + 1), roi_rng[2], roi_rng[4], roi_channel
            ] = roi_value
            image[
                roi_rng[0] : (roi_rng[1] + 1), roi_rng[3], roi_rng[5], roi_channel
            ] = roi_value


def _DrawAnnotationsInArray(
    image: array_t, mkpt_lst: Sequence[marked_point_t], locrup: int
) -> None:
    #
    font_size = 11

    for mkpt in mkpt_lst:
        bbox = mkpt.bbox
        array_w_text = _ArrayWithText(mkpt.runtime_uid[locrup:], size=font_size)
        array_w_text = list(nmpy.nonzero(array_w_text))
        array_w_text[0] += (
            bbox.mins[0] + bbox.maxs[0] + font_size
        ) // 2 - array_w_text[0].max()
        array_w_text[1] += bbox.mins[1] + font_size // 2 - array_w_text[1].min()

        out_of_domain = nmpy.logical_or(array_w_text[0] < 0, array_w_text[1] < 0)
        out_of_domain = nmpy.logical_or(out_of_domain, array_w_text[0] >= image.shape[0])
        out_of_domain = nmpy.logical_or(out_of_domain, array_w_text[1] >= image.shape[1])
        within_domain = nmpy.logical_not(out_of_domain)

        array_w_text = (
            array_w_text[0][within_domain],
            array_w_text[1][within_domain],
        )

        image[:, :, 0][array_w_text] = 1.0


def _Plot3DObjectsWithMayavi(
    image: array_t, background: array_t, mkpt_lst: Sequence[marked_point_t]
) -> None:
    #
    print("Mayavi: 3-D engine currently disabled")

    # if background.ndim == 4:
    #     background = background[..., 0]
    #
    # for mkpt in mkpt_lst:
    #     image[mkpt.bbox.rows, mkpt.bbox.cols, mkpt.bbox.deps][
    #         mkpt.raw_region
    #     ] = 255
    #
    # scalar_field_bck = mv_.pipeline.scalar_field(background)
    # scalar_field_res = mv_.pipeline.scalar_field(image)
    #
    # mv_.pipeline.iso_surface(
    #     scalar_field_bck,
    #     contours=[0.5 * nmpy.max(background)],
    #     color=(0, 1, 0),
    #     opacity=0.3,
    #     name="Bck Iso",
    # )
    # mv_.pipeline.iso_surface(
    #     scalar_field_res,
    #     contours=[128],
    #     color=(0, 0, 1),
    #     opacity=0.3,
    #     name="Res Iso",
    # )
    #
    # # mv_.pipeline.image_plane_widget(
    # #     scalar_field_bck,
    # #     plane_orientation="z_axes",
    # #     slice_index=10,
    # #     colormap="gray",
    # #     name="Bck Cut Plane",
    # # )
    # # mv_.outline(color=(0, 0, 1), opacity=0.5, name="Bck Cut Plane Outline")
    # # mv_.pipeline.iso_surface(
    # #     scalar_field_res,
    # #     contours=[128],
    # #     color=(0, 0, 1),
    # #     opacity=0.3,
    # #     name="Res Iso 2",
    # # )
    # # mv_.show_engine()


def _ArrayWithText(text: str, size: int = 10) -> array_t:
    #
    font = ImageFont.truetype("arial.ttf", size)

    image = Image.new(mode="1", size=(size * (text.__len__() + 1), 2 * size), color=0)
    drawer = ImageDraw.Draw(image)
    drawer.text((size // 2, size // 2), text, font=font, fill=1)

    output = nmpy.asarray(image, dtype=nmpy.bool_)

    n_rows, n_cols = output.shape
    row_projection = output.any(axis=1)
    col_projection = output.any(axis=0)
    row_start = row_projection.argmax()
    row_end_p_1 = n_rows - row_projection[::-1].argmax()
    col_start = col_projection.argmax()
    col_end_p_1 = n_cols - col_projection[::-1].argmax()

    return output[row_start:row_end_p_1, col_start:col_end_p_1]
