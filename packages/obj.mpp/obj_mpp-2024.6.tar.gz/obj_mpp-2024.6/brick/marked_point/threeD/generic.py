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

import brick.interface.io.reporting as rp_
from brick.marked_point.generic import bbox_t
from brick.marked_point.generic import marked_point_t as marked_point_anyD_t
from brick.signal.signal_context import signal_context_t
from brick.data.type import array_t

from abc import ABC as abc_t
from typing import ClassVar, Tuple

import numpy as nmpy
import skimage.morphology as mp_


class marked_point_t(marked_point_anyD_t, abc_t):

    dim: ClassVar[int] = 3

    # --- COMPUTE

    def _ContourIfConvex(self, thickness: int = 1) -> array_t:
        #
        region = self.region

        left_to_right = region.cumsum(axis=1)
        right_to_left = nmpy.fliplr(nmpy.fliplr(region).cumsum(axis=1))
        top_to_bottom = region.cumsum(axis=0)
        bottom_to_top = nmpy.flipud(nmpy.flipud(region).cumsum(axis=0))
        shallow_to_deep = region.cumsum(axis=2)
        deep_to_shallow = region[:, :, ::-1].cumsum(axis=2)[:, :, ::-1]

        # Anding with region automatically invalidates sites if needed
        contour = nmpy.logical_and(
            left_to_right.__le__(thickness)
            .__or__(right_to_left.__le__(thickness))
            .__or__(top_to_bottom.__le__(thickness))
            .__or__(bottom_to_top.__le__(thickness))
            .__or__(shallow_to_deep.__le__(thickness))
            .__or__(deep_to_shallow.__le__(thickness)),
            region,
        )
        # To remove fake contour pixels on the domain borders, if any
        cropping_indicator = self.cropping_indicator
        if cropping_indicator[0]:
            contour[:thickness, :, :] = False
        if cropping_indicator[1]:
            contour[-thickness:, :, :] = False
        if cropping_indicator[2]:
            contour[:, :thickness, :] = False
        if cropping_indicator[3]:
            contour[:, -thickness:, :] = False
        if cropping_indicator[4]:
            contour[:, :, :thickness] = False
        if cropping_indicator[5]:
            contour[:, :, -thickness:] = False

        return contour

    @staticmethod
    def _BallOfRadius(radius: int) -> array_t:
        #
        if radius not in marked_point_t._ball_of_radius:
            marked_point_t._ball_of_radius[radius] = mp_.ball(radius, dtype=nmpy.bool_)

        return marked_point_t._ball_of_radius[radius]

    def _DilatedBboxSlices(self, dilation: int) -> Tuple[slice, ...]:  # Can be negative
        #
        bbox: bbox_t = self.bbox

        min_row = bbox.mins[0] - dilation
        min_col = bbox.mins[1] - dilation
        min_dep = bbox.mins[2] - dilation
        if min_row < 0:
            min_row = 0
        if min_col < 0:
            min_col = 0
        if min_dep < 0:
            min_dep = 0

        max_row = bbox.maxs[0] + dilation
        max_col = bbox.maxs[1] + dilation
        max_dep = bbox.maxs[2] + dilation
        if max_row >= signal_context_t.lengths[0]:
            max_row = signal_context_t.lengths[0] - 1
        if max_col >= signal_context_t.lengths[1]:
            max_col = signal_context_t.lengths[1] - 1
        if max_dep >= signal_context_t.lengths[2]:
            max_dep = signal_context_t.lengths[2] - 1

        row_slice = slice(min_row, max_row + 1)
        col_slice = slice(min_col, max_col + 1)
        dep_slice = slice(min_dep, max_dep + 1)

        return row_slice, col_slice, dep_slice

    # --- ANALYZE

    def Intersects(self, mkpt: marked_point_t, overlap_tolerance: float) -> bool:
        #
        bbox_1 = self.bbox
        bbox_2 = mkpt.bbox
        if (
            (bbox_1.mins[0] > bbox_2.maxs[0])
            or (bbox_2.mins[0] > bbox_1.maxs[0])
            or (bbox_1.mins[1] > bbox_2.maxs[1])
            or (bbox_2.mins[1] > bbox_1.maxs[1])
            or (bbox_1.mins[2] > bbox_2.maxs[2])
            or (bbox_2.mins[2] > bbox_1.maxs[2])
        ):
            return False

        region_1 = self.region
        region_2 = mkpt.region
        area_1 = self.area
        area_2 = mkpt.area
        if (area_1 == 0) or (area_2 == 0):
            raise rp_.BugException()

        inter_min_row = max(bbox_1.mins[0], bbox_2.mins[0])
        inter_max_row = min(bbox_1.maxs[0], bbox_2.maxs[0])
        inter_min_col = max(bbox_1.mins[1], bbox_2.mins[1])
        inter_max_col = min(bbox_1.maxs[1], bbox_2.maxs[1])
        inter_min_dep = max(bbox_1.mins[2], bbox_2.mins[2])
        inter_max_dep = min(bbox_1.maxs[2], bbox_2.maxs[2])

        region_1_min_row = max(inter_min_row - bbox_1.mins[0], 0)
        region_1_max_row = min(inter_max_row - bbox_1.mins[0] + 1, region_1.shape[0])
        region_1_min_col = max(inter_min_col - bbox_1.mins[1], 0)
        region_1_max_col = min(inter_max_col - bbox_1.mins[1] + 1, region_1.shape[1])
        region_1_min_dep = max(inter_min_dep - bbox_1.mins[2], 0)
        region_1_max_dep = min(inter_max_dep - bbox_1.mins[2] + 1, region_1.shape[2])

        region_2_min_row = max(inter_min_row - bbox_2.mins[0], 0)
        region_2_max_row = min(inter_max_row - bbox_2.mins[0] + 1, region_2.shape[0])
        region_2_min_col = max(inter_min_col - bbox_2.mins[1], 0)
        region_2_max_col = min(inter_max_col - bbox_2.mins[1] + 1, region_2.shape[1])
        region_2_min_dep = max(inter_min_dep - bbox_2.mins[2], 0)
        region_2_max_dep = min(inter_max_dep - bbox_2.mins[2] + 1, region_2.shape[2])

        domain_1 = (
            slice(region_1_min_row, region_1_max_row),
            slice(region_1_min_col, region_1_max_col),
            slice(region_1_min_dep, region_1_max_dep),
        )
        domain_2 = (
            slice(region_2_min_row, region_2_max_row),
            slice(region_2_min_col, region_2_max_col),
            slice(region_2_min_dep, region_2_max_dep),
        )

        return self.__class__._FinallyIntersects(
            region_1,
            domain_1,
            area_1,
            region_2,
            domain_2,
            area_2,
            overlap_tolerance,
        )

    # --- REPORT

    @staticmethod
    def CoordsHeader() -> Tuple[str, ...]:
        #
        return "Center Row", "Center Col", "Center Dep"

    # def DrawInArray(
    #     self,
    #     array: array_t,
    #     level: number_h = 255,
    #     thickness: int = 1,
    #     bbox_level: number_h = -1,
    # ) -> None:
    #     #
    #     bbox: bbox_t = self.bbox
    #
    #     if bbox_level >= 0:
    #         array[bbox.mins[0], bbox.domain[1], bbox.domain[2]] = bbox_level
    #         array[bbox.maxs[0], bbox.domain[1], bbox.domain[2]] = bbox_level
    #         array[bbox.domain[0], bbox.mins[1], bbox.domain[2]] = bbox_level
    #         array[bbox.domain[0], bbox.maxs[1], bbox.domain[2]] = bbox_level
    #         array[bbox.domain[0], bbox.domain[1], bbox.mins[2]] = bbox_level
    #         array[bbox.domain[0], bbox.domain[1], bbox.maxs[2]] = bbox_level
    #
    #     if thickness > 0:
    #         array[bbox.domain][self.Contour(thickness=thickness)] = level
    #     else:
    #         array[bbox.domain][self.region] = level

    # def _ComputeBoundingBox(
    #     self, half_height: float, half_width: float, half_depth: float
    # ) -> None:
    #     #
    #     # Compute the cube just big enough to contain the ellipsoid and set the appropriate member variables
    #     #
    #     cropping_indicator = 2 * self.dim * [False]
    #
    #     min_row = self.position[0] - half_height
    #     if min_row < 0:
    #         min_row = 0
    #         cropping_indicator[1] = True
    #     else:
    #         min_row = int(nmpy.floor(min_row))
    #
    #     min_col = self.position[1] - half_width
    #     if min_col < 0:
    #         min_col = 0
    #         cropping_indicator[2] = True
    #     else:
    #         min_col = int(nmpy.floor(min_col))
    #
    #     min_dep = self.position[2] - half_depth
    #     if min_dep < 0:
    #         min_dep = 0
    #         cropping_indicator[4] = True
    #     else:
    #         min_dep = int(nmpy.floor(min_dep))
    #
    #     max_row = self.position[0] + half_height
    #     if max_row > signal_context_t.lengths[0] - 1:
    #         max_row = signal_context_t.lengths[0] - 1
    #         cropping_indicator[3] = True
    #     else:
    #         max_row = int(nmpy.ceil(max_row))
    #
    #     max_col = self.position[1] + half_width
    #     if max_col > signal_context_t.lengths[1] - 1:
    #         max_col = signal_context_t.lengths[1] - 1
    #         cropping_indicator[0] = True
    #     else:
    #         max_col = int(nmpy.ceil(max_col))
    #
    #     max_dep = self.position[2] + half_depth
    #     if max_dep > signal_context_t.lengths[2] - 1:
    #         max_dep = signal_context_t.lengths[2] - 1
    #         cropping_indicator[5] = True
    #     else:
    #         max_dep = int(nmpy.ceil(max_dep))
    #
    #     row_slice = slice(min_row, max_row + 1)
    #     col_slice = slice(min_col, max_col + 1)
    #     dep_slice = slice(min_dep, max_dep + 1)
    #     self.bbox = bbox_t(
    #         mins=(min_row,min_col,min_dep),
    #         maxs=(max_row,max_col,max_dep),
    #         lengths=(max_row - min_row + 1, max_col - min_col + 1, max_dep - min_dep + 1),
    #         domain=(row_slice, col_slice, dep_slice),
    #     )
    #     self.cropping_indicator = tuple(cropping_indicator)
    #     self.crosses_border = any(self.cropping_indicator)
