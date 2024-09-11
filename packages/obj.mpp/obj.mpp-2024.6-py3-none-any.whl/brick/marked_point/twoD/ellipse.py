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
from brick.data.type import array_t
from brick.signal.signal_context import signal_context_t
from brick.marked_point.twoD.generic import marked_point_t
from brick.marked_point.twoD.superquadric import superquadric_t

import ctypes as ct_
import math as ma_
from typing import Sequence, Tuple

import numpy as nmpy


_RawRegion_C = ex_.RawRegionImplementationInC(__file__)
if _RawRegion_C is not None:
    _RawRegion_C.argtypes = (
        ct_.c_void_p,
        ct_.c_void_p,
        ct_.c_size_t,
        ct_.c_double,
        ct_.c_double,
        ct_.c_double,
        ct_.c_double,
        ct_.c_double,
        ct_.c_void_p,
    )


class ellipse_t(superquadric_t):

    marks_details = {}
    marks_details["semi_minor_axis"] = superquadric_t.marks_details["semi_minor_axis"]
    marks_details["major_minor_ratio"] = superquadric_t.marks_details[
        "major_minor_ratio"
    ]
    marks_details["angle"] = superquadric_t.marks_details["angle"]

    # --- INSTANTIATE

    def __init__(
        self,
        center: Sequence[int],
        semi_minor_axis: int,
        major_minor_ratio: float,
        angle: float,
        check_marks: bool = True,
    ) -> None:
        #
        super().__init__(
            center,
            semi_minor_axis,
            major_minor_ratio,
            2.0,
            2.0,
            angle,
            check_marks=check_marks,
        )

    @classmethod
    def NormalizeMarkRanges(cls, mk_ranges: dict) -> None:
        #
        # cls._ConvertAngleRangeToRadians("angle", mk_ranges)
        marked_point_t.CheckMarkRanges(
            mk_ranges, cls.marks_details, cls.marks_translations
        )
        marked_point_t.AddDefaultsToMarkRanges(mk_ranges, cls.marks_details)

    def _CoarseBoundingBoxHalfLengths(self) -> Tuple[int, ...]:
        #
        s_min_a_2 = float(self.marks["semi_minor_axis"]) ** 2
        s_maj_a_2 = s_min_a_2 * self.marks["major_minor_ratio"] ** 2

        cos_2 = ma_.cos(self.marks["angle"]) ** 2
        sin_2 = ma_.sin(self.marks["angle"]) ** 2

        half_length_row = ma_.ceil(
            ma_.sqrt(s_min_a_2 * cos_2 + s_maj_a_2 * sin_2)
        ).__int__()
        half_length_col = ma_.ceil(
            ma_.sqrt(s_min_a_2 * sin_2 + s_maj_a_2 * cos_2)
        ).__int__()

        return half_length_row, half_length_col

    # --- REPORT

    def AsColoredStr(self, locrup: int = 0) -> str:
        #
        cache_entry = self.AsColoredStr.__name__

        if cache_entry not in self._cache:
            semi_major_axis = (
                self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"]
            )
            formatted_marks = tc_.ColoredText(
                f'{self.marks["semi_minor_axis"]:.2f}x' f"{semi_major_axis:.2f}", "red"
            )

            self._cache[cache_entry] = (
                self.runtime_uid[locrup:]
                + " "
                + "E+"
                + self.FormattedPosition()
                + formatted_marks
                + self.FormattedAngle("angle")
                + self.FormattedQuality()
            )

        return self._cache[cache_entry] + self.FormattedAge()

    @property
    def educated_marks(self) -> tuple:
        #
        return (
            self.marks["semi_minor_axis"],
            self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"],
            self.marks["angle"],
            self.marks["angle"] * 180.0 / ma_.pi,
        )

    @staticmethod
    def EducatedMarksHeaders() -> Tuple[str, ...]:
        #
        return (
            "Semi Minor Axis",
            "Semi Major Axis",
            "Angle (radian)",
            "Angle (degree)",
        )

    # --- COMPUTE

    def _RawRegion(self) -> array_t:
        #
        sig_grid_coords = signal_context_t.grid_coords
        if _RawRegion_C is None:
            centered_rows = sig_grid_coords[0][self.bbox.domain] - self.position[0]
            centered_cols = sig_grid_coords[1][self.bbox.domain] - self.position[1]

            cos = ma_.cos(self.marks["angle"])
            sin = ma_.sin(self.marks["angle"])
            rotated_rows = sin * centered_cols + cos * centered_rows
            rotated_cols = cos * centered_cols - sin * centered_rows

            semi_major_axis = (
                self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"]
            )
            sq_1_level_map = rotated_rows ** 2 * (
                1.0 / self.marks["semi_minor_axis"] ** 2
            ) + rotated_cols ** 2 * (1.0 / semi_major_axis ** 2)
            region = sq_1_level_map <= 1.0
        else:
            bbox_grid_rows = nmpy.array(
                sig_grid_coords[0][self.bbox.domain], dtype=nmpy.float64, order="C"
            )
            bbox_grid_cols = nmpy.array(
                sig_grid_coords[1][self.bbox.domain], dtype=nmpy.float64, order="C"
            )
            region = nmpy.empty_like(bbox_grid_rows, dtype=nmpy.bool_)
            _RawRegion_C(
                bbox_grid_rows.ctypes.data,
                bbox_grid_cols.ctypes.data,
                bbox_grid_rows.size,
                *self.position,
                self.marks["semi_minor_axis"],
                self.marks["major_minor_ratio"],
                self.marks["angle"],
                region.ctypes.data,
            )

        return region

    def Normals(self) -> Tuple[array_t, ...]:
        #
        cache_entry = self.Normals.__name__

        if cache_entry not in self._cache:
            positions = self.Contour().nonzero()

            rotation = nmpy.empty((2, 2), dtype=nmpy.float64, order="C")
            rotation[0, 0] = nmpy.cos(self.marks["angle"])
            rotation[1, 0] = nmpy.sin(self.marks["angle"])
            rotation[0, 1] = -rotation[1, 0]
            rotation[1, 1] = rotation[0, 0]

            unrotated_coords = (
                nmpy.transpose(positions).astype(nmpy.float64)
                + [
                    [
                        self.bbox.mins[0] - self.position[0],
                        self.bbox.mins[1] - self.position[1],
                    ]
                ]
            ) @ rotation

            normals = unrotated_coords
            normals[:, 0] /= self.marks["semi_minor_axis"] ** 2
            normals[:, 1] /= (
                self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"]
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
