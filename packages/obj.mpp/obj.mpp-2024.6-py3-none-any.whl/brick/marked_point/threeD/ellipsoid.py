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

import brick.interface.ko.text_color as tc_
import brick.structure.extension as ex_
from brick.data.marked_point.std_marks import (
    STD_DETAILS_ANGLE_2PI,
    STD_DETAILS_ANGLE_PI,
    STD_DETAILS_RADII_RATIO,
    STD_DETAILS_RADIUS,
    mark_details_t,
)
from brick.data.type import array_t
from brick.signal.signal_context import signal_context_t
from brick.marked_point.threeD.generic import marked_point_t

import ctypes as ct_
import math as ma_
from typing import Tuple

import numpy as nmpy


_RawRegion_C = ex_.RawRegionImplementationInC(__file__)
if _RawRegion_C is not None:
    _RawRegion_C.argtypes = (
        ct_.c_void_p,
        ct_.c_void_p,
        ct_.c_void_p,
        ct_.c_size_t,
        ct_.c_double,
        ct_.c_double,
        ct_.c_double,
        ct_.c_double,
        ct_.c_double,
        ct_.c_double,
        ct_.c_double,
        ct_.c_double,
        ct_.c_void_p,
    )


class ellipsoid_t(marked_point_t):

    marks_details = {
        "semi_minor_axis": STD_DETAILS_RADIUS,
        "major_minor_ratio": STD_DETAILS_RADII_RATIO,
        "third_minor_ratio": mark_details_t(
            type=float,
            min=0.0,
            max=nmpy.finfo(float).max,
            min_inclusive=False,
            max_inclusive=True,
            default_range=(1.0, 1.0),
            default_precision=None,
        ),
        "rc_angle": STD_DETAILS_ANGLE_PI,  # Rotation in rowxcol-plane
        "rd_angle": STD_DETAILS_ANGLE_2PI,  # Rotation in rowxdep-plane
    }
    # TODO: The sampling is probably not uniform due to absence of constraint on third_minor_ratio
    # Define only if class derives from marked_point_t. Only for such classes does this property "matches" the
    # marks details. For derived classes, the marks details concerns only the marks specific to the class.
    # Only use in generic.__init__.
    mark_names = tuple(marks_details.keys())

    # --- INSTANTIATE

    @classmethod
    def NormalizeMarkRanges(cls, mk_ranges: dict) -> None:
        #
        # cls._ConvertAngleRangeToRadians("rc_angle", mk_ranges)
        # cls._ConvertAngleRangeToRadians("rd_angle", mk_ranges)
        marked_point_t.CheckMarkRanges(
            mk_ranges, cls.marks_details, cls.marks_translations
        )
        marked_point_t.AddDefaultsToMarkRanges(mk_ranges, cls.marks_details)

    def _CoarseBoundingBoxHalfLengths(self) -> Tuple[int, ...]:
        #
        semi_major_axis = ma_.ceil(
            self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"]
        ).__int__()
        semi_third_axis = ma_.ceil(
            self.marks["semi_minor_axis"] * self.marks["third_minor_ratio"]
        ).__int__()
        radius = max(semi_major_axis, semi_third_axis)

        return radius, radius, radius

    # --- REPORT

    def AsColoredStr(self, locrup: int = 0) -> str:
        #
        cache_entry = self.AsColoredStr.__name__

        if cache_entry not in self._cache:
            semi_major_axis = (
                self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"]
            )
            semi_third_axis = (
                self.marks["semi_minor_axis"] * self.marks["third_minor_ratio"]
            )
            self._cache[cache_entry] = (
                self.runtime_uid[locrup:]
                + " "
                + "E+"
                + self.FormattedPosition()
                + tc_.ColoredText(
                    f'{self.marks["semi_minor_axis"]}x'
                    f"{semi_major_axis:.2f}x"
                    f"{semi_third_axis:.2f}",
                    "red",
                )
                + self.FormattedAngle("rc_angle")
                + self.FormattedAngle("rd_angle")
                + self.FormattedQuality()
            )

        return self._cache[cache_entry] + self.FormattedAge()

    @property
    def educated_marks(self) -> tuple:
        #
        return (
            self.marks["semi_minor_axis"],
            self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"],
            self.marks["semi_minor_axis"] * self.marks["third_minor_ratio"],
            self.marks["rc_angle"],
            self.marks["rc_angle"] * 180.0 / ma_.pi,
            self.marks["rd_angle"],
            self.marks["rd_angle"] * 180.0 / ma_.pi,
        )

    @staticmethod
    def EducatedMarksHeaders() -> Tuple[str, ...]:
        #
        return (
            "Semi Minor Axis",
            "Semi Major Axis",
            "Semi Third Axis",
            "Angle (radian)",
            "Angle (degree)",
            "Second Angle (radian)",
            "Second Angle (degree)",
        )

    # --- COMPUTE

    def _RawRegion(self) -> array_t:
        #
        sig_grid_coords = signal_context_t.grid_coords
        if _RawRegion_C is None:
            centered_rows = sig_grid_coords[0][self.bbox.domain] - self.position[0]
            centered_cols = sig_grid_coords[1][self.bbox.domain] - self.position[1]
            centered_deps = sig_grid_coords[2][self.bbox.domain] - self.position[2]

            cos = ma_.cos(self.marks["rc_angle"])
            sin = ma_.sin(self.marks["rc_angle"])
            rotated_rows = sin * centered_cols + cos * centered_rows
            rotated_cols = cos * centered_cols - sin * centered_rows
            rotated_deps = centered_deps

            cos = ma_.cos(self.marks["rd_angle"])
            sin = ma_.sin(self.marks["rd_angle"])
            re_rotated_rows = sin * rotated_deps + cos * rotated_rows
            re_rotated_cols = rotated_cols
            re_rotated_deps = cos * rotated_deps - sin * rotated_rows

            semi_minor_axis = self.marks["semi_minor_axis"]
            semi_major_axis = semi_minor_axis * self.marks["major_minor_ratio"]
            semi_third_axis = semi_minor_axis * self.marks["third_minor_ratio"]
            sq_1_level_map = (
                re_rotated_rows ** 2 * (1.0 / semi_minor_axis ** 2)
                + re_rotated_cols ** 2 * (1.0 / semi_major_axis ** 2)
                + re_rotated_deps ** 2 * (1.0 / semi_third_axis ** 2)
            )
            region = sq_1_level_map <= 1.0
        else:
            bbox_grid_rows = nmpy.array(
                sig_grid_coords[0][self.bbox.domain], dtype=nmpy.float64, order="C"
            )
            bbox_grid_cols = nmpy.array(
                sig_grid_coords[1][self.bbox.domain], dtype=nmpy.float64, order="C"
            )
            bbox_grid_deps = nmpy.array(
                sig_grid_coords[2][self.bbox.domain], dtype=nmpy.float64, order="C"
            )
            region = nmpy.empty_like(bbox_grid_rows, dtype=nmpy.bool_)
            _RawRegion_C(
                bbox_grid_rows.ctypes.data,
                bbox_grid_cols.ctypes.data,
                bbox_grid_deps.ctypes.data,
                bbox_grid_rows.size,
                *self.position,
                self.marks["semi_minor_axis"],
                self.marks["major_minor_ratio"],
                self.marks["third_minor_ratio"],
                self.marks["rc_angle"],
                self.marks["rd_angle"],
                region.ctypes.data,
            )

        return region

    def Normals(self) -> Tuple[array_t, ...]:
        #
        cache_entry = self.Normals.__name__

        if cache_entry not in self._cache:
            positions = self.Contour().nonzero()

            rd_rotation = nmpy.zeros((3, 3), dtype=nmpy.float64, order="C")
            rd_rotation[0, 0] = nmpy.cos(self.marks["rd_angle"])
            rd_rotation[2, 0] = nmpy.sin(self.marks["rd_angle"])
            rd_rotation[0, 2] = -rd_rotation[2, 0]
            rd_rotation[2, 2] = rd_rotation[0, 0]
            rd_rotation[1, 1] = 1.0

            rc_rotation = nmpy.zeros((3, 3), dtype=nmpy.float64, order="C")
            rc_rotation[0, 0] = nmpy.cos(self.marks["rc_angle"])
            rc_rotation[1, 0] = nmpy.sin(self.marks["rc_angle"])
            rc_rotation[0, 1] = -rc_rotation[1, 0]
            rc_rotation[1, 1] = rc_rotation[0, 0]
            rc_rotation[2, 2] = 1.0

            rotation = rd_rotation @ rc_rotation

            unrotated_coords = (
                nmpy.transpose(positions).astype(nmpy.float64)
                + [
                    [
                        self.bbox.mins[0] - self.position[0],
                        self.bbox.mins[1] - self.position[1],
                        self.bbox.mins[2] - self.position[2],
                    ]
                ]
            ) @ rotation

            normals = unrotated_coords
            normals[:, 0] /= self.marks["semi_minor_axis"] ** 2
            normals[:, 1] /= (
                self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"]
            ) ** 2
            normals[:, 2] /= (
                self.marks["semi_minor_axis"] * self.marks["third_minor_ratio"]
            ) ** 2

            normals = normals @ rotation.transpose()
            normal_norms = nmpy.sqrt((normals ** 2).sum(axis=1, keepdims=True))
            # When the analytical normal expression is evaluated at (0,0), it results in a null normal. This
            # occurs whenever the contour "passes through the center" (very thick contour and/or very thin object).
            normal_norms[normal_norms == 0.0] = 1.0
            normals /= normal_norms

            self._cache[cache_entry] = (positions, normals)

        return self._cache[cache_entry]

    def Contour(self, thickness: int = 1) -> array_t:
        #
        cache_entry = self.Contour.__name__

        if cache_entry not in self._cache:
            self._cache[cache_entry] = {}

        if thickness not in self._cache[cache_entry]:
            self._cache[cache_entry][thickness] = self._ContourIfConvex(
                thickness=thickness
            )
            # It is useless to apply self.__class__.data_validity_bmap since _ContourIfConvex builds on Region
            # (/!\ check _ContourIfConvex for potential changes).

        return self._cache[cache_entry][thickness]

    # --- GENERATE

    def _RangeSizeForSimilarPoints(self, fraction: float = 0.1) -> float:
        #
        return (
            0.34
            * fraction
            * self.marks["semi_minor_axis"]
            * (1.0 + self.marks["major_minor_ratio"] + self.marks["third_minor_ratio"])
        )
