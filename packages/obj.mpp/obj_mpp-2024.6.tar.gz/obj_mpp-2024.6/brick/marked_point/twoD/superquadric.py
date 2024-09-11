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
    STD_DETAILS_ANGLE_PI,
    STD_DETAILS_RADII_RATIO,
    STD_DETAILS_RADIUS,
    mark_details_t,
)
from brick.data.type import array_t
from brick.signal.signal_context import signal_context_t
from brick.marked_point.twoD.generic import marked_point_t

import ctypes as ct_
import math as ma_
from typing import Tuple

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
        ct_.c_double,
        ct_.c_double,
        ct_.c_void_p,
    )


class superquadric_t(marked_point_t):

    marks_details = {
        "semi_minor_axis": STD_DETAILS_RADIUS,
        "major_minor_ratio": STD_DETAILS_RADII_RATIO,
        "minor_exponent": mark_details_t(  # "Minor" is not in the sense of "smallest"; It means "corresponding to the minor axis"
            type=float,
            min=0.0,
            max=nmpy.finfo(float).max,
            min_inclusive=False,
            max_inclusive=True,
            default_range=(1.0, 2.0),#None, # TODO: if None, mark is not recognized as a potential tuple
            default_precision=None,
        ),
        "major_exponent": None,  # To guarantee the same order of marks as in __init__ (/!\ It relies on dict respecting this order)
        "angle": STD_DETAILS_ANGLE_PI,
    }
    marks_details["major_exponent"] = marks_details["minor_exponent"]
    # Define only if class derives from marked_point_t. Only for such classes does this property "matches" the
    # marks details. For derived classes, the marks details concerns only the marks specific to the class.
    # Only use in generic.__init__.
    mark_names = tuple(marks_details.keys())

    # --- INSTANTIATE

    @classmethod
    def NormalizeMarkRanges(cls, mk_ranges: dict) -> None:
        #
        if "exponent_rng" in mk_ranges:
            mk_ranges["minor_exponent_rng"] = mk_ranges["exponent_rng"]
            mk_ranges["major_exponent_rng"] = mk_ranges["exponent_rng"]
            del mk_ranges["exponent_rng"]

        # cls._ConvertAngleRangeToRadians("angle", mk_ranges)
        marked_point_t.CheckMarkRanges(
            mk_ranges, cls.marks_details, cls.marks_translations
        )
        marked_point_t.AddDefaultsToMarkRanges(mk_ranges, cls.marks_details)

    def _CoarseBoundingBoxHalfLengths(self) -> Tuple[int, ...]:
        #
        semi_major_axis = ma_.ceil(
            self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"]
        ).__int__()

        return semi_major_axis, semi_major_axis

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
                + "Q+"
                + self.FormattedPosition()
                + formatted_marks
                + self.FormattedExponent("minor_exponent")
                + self.FormattedExponent("major_exponent")
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
            self.marks["minor_exponent"],
            self.marks["major_exponent"],
            self.marks["angle"],
            self.marks["angle"] * 180.0 / ma_.pi,
        )

    @staticmethod
    def EducatedMarksHeaders() -> Tuple[str, ...]:
        #
        return (
            "Semi Minor Axis",
            "Semi Major Axis",
            "Exp of S.Min.A",
            "Exp of S.Maj.A",
            "Angle (radian)",
            "Angle (degree)",
        )

    # --- COMPUTE

    def _RawRegion(self) -> array_t:
        #
        # Alternative, faster or not, implementation: compute only in the first quadrant, then copy 2 times by flipping,
        # then rotate with scipy.ndimage.rotate or skimage.transform.rotate. Put max value in pixels outside the domain.
        # This alternative is valid because the bbox is a square corresponding to the unrotated superquadric. (Does it
        # change anything to the management of out-of-domain pixels?)
        #
        sig_grid_coords = signal_context_t.grid_coords
        if _RawRegion_C is None:
            centered_rows = sig_grid_coords[0][self.bbox.domain] - self.position[0]
            centered_cols = sig_grid_coords[1][self.bbox.domain] - self.position[1]

            cos = ma_.cos(self.marks["angle"])
            sin = ma_.sin(self.marks["angle"])
            rotated_rows = sin * centered_cols + cos * centered_rows
            rotated_cols = cos * centered_cols - sin * centered_rows

            minor_power = nmpy.power(
                nmpy.fabs(rotated_rows), self.marks["minor_exponent"]
            )
            major_power = nmpy.power(
                nmpy.fabs(rotated_cols), self.marks["major_exponent"]
            )
            minor_factor = (
                1.0 / self.marks["semi_minor_axis"] ** self.marks["minor_exponent"]
            )
            major_factor = (
                1.0
                / (self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"])
                ** self.marks["major_exponent"]
            )

            sq_1_level_map = minor_power * minor_factor + major_power * major_factor
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
                self.marks["minor_exponent"],
                self.marks["major_exponent"],
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
            row_signs = nmpy.sign(normals[:, 0])
            col_signs = nmpy.sign(normals[:, 1])
            normals[:, 0] = (
                nmpy.power(nmpy.fabs(normals[:, 0]), self.marks["minor_exponent"] - 1.0)
                * row_signs
            )
            normals[:, 1] = (
                nmpy.power(nmpy.fabs(normals[:, 1]), self.marks["major_exponent"] - 1.0)
                * col_signs
            )
            normals[:, 0] *= (
                self.marks["minor_exponent"]
                / self.marks["semi_minor_axis"] ** self.marks["minor_exponent"]
            )
            normals[:, 1] *= (
                self.marks["major_exponent"]
                / (self.marks["semi_minor_axis"] * self.marks["major_minor_ratio"])
                ** self.marks["major_exponent"]
            )

            normals = normals @ rotation.transpose()
            normal_norms = nmpy.sqrt((normals ** 2).sum(axis=1, keepdims=True))
            # When the analytical normal expression is evaluated at (0,0), it results in a null normal. This
            # occurs whenever the contour "passes through the center" (very thick contour and/or very thin object).
            normal_norms[normal_norms == 0.0] = 1.0
            normals /= normal_norms

            self._cache[cache_entry] = (positions, normals)

        return self._cache[cache_entry]

    # --- GENERATE

    def _RangeSizeForSimilarPoints(self, fraction: float = 0.1) -> float:
        #
        return (
            0.5
            * fraction
            * self.marks["semi_minor_axis"]
            * (1.0 + self.marks["major_minor_ratio"])
        )
