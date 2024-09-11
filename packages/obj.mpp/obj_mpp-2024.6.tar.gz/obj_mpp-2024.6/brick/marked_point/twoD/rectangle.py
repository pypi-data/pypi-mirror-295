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

import brick.structure.extension as ex_
from brick.data.type import array_t
from brick.signal.constant import INFINITY_NUMPY_FLOAT
from brick.signal.signal_context import signal_context_t
from brick.marked_point.twoD.ellipse import ellipse_t
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


class rectangle_t(ellipse_t):

    marks_details = ellipse_t.marks_details  # Otherwise it will be inherited from upper

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
        superquadric_t.__init__(
            self,
            center,
            semi_minor_axis,
            major_minor_ratio,
            INFINITY_NUMPY_FLOAT,
            INFINITY_NUMPY_FLOAT,
            angle,
            check_marks=check_marks,
        )

    def _CoarseBoundingBoxHalfLengths(self) -> Tuple[int, ...]:
        #
        s_min_a_2 = float(self.marks["semi_minor_axis"])
        s_maj_a_2 = s_min_a_2 * self.marks["major_minor_ratio"]

        abs_cos = abs(ma_.cos(self.marks["angle"]))
        abs_sin = abs(ma_.sin(self.marks["angle"]))

        half_length_row = ma_.ceil(s_min_a_2 * abs_cos + s_maj_a_2 * abs_sin).__int__()
        half_length_col = ma_.ceil(s_min_a_2 * abs_sin + s_maj_a_2 * abs_cos).__int__()

        return half_length_row, half_length_col

    # --- REPORT

    def AsColoredStr(self, locrup: int = 0) -> str:
        #
        cache_entry = self.AsColoredStr.__name__

        if cache_entry not in self._cache:
            self._cache[cache_entry] = super().AsColoredStr(locrup=locrup).replace("E+", "R+", 1)

        return self._cache[cache_entry]

    @staticmethod
    def EducatedMarksHeaders() -> Tuple[str, ...]:
        #
        return (
            "Half Small Length",
            "Half Large Length",
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
            sq_1_level_map = nmpy.fmax(
                nmpy.fabs(rotated_rows * (1.0 / self.marks["semi_minor_axis"])),
                nmpy.fabs(rotated_cols * (1.0 / semi_major_axis)),
            )
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
            coord_norms = nmpy.sqrt((unrotated_coords ** 2).sum(axis=1))
            if self.crosses_border:
                # The line below is useless in general. It is necessary when the shape is partially outside the image
                # domain, with its center on the border. In this case, the analytical normal expression is evaluated
                # at (0,0), which results in a null normal.
                coord_norms[coord_norms == 0.0] = 1.0

            coord_angles = nmpy.arccos(unrotated_coords[:, 0] / coord_norms)
            limit_angle = ma_.atan(self.marks["major_minor_ratio"])
            col_edges = nmpy.logical_or(
                coord_angles < limit_angle, coord_angles > ma_.pi - limit_angle
            )
            row_edges = nmpy.logical_not(col_edges)

            normals = nmpy.empty_like(unrotated_coords)
            normals[col_edges, 0] = nmpy.sign(unrotated_coords[col_edges, 0])
            normals[col_edges, 1] = 0.0
            normals[row_edges, 0] = 0.0
            normals[row_edges, 1] = nmpy.sign(unrotated_coords[row_edges, 1])

            normals = normals @ rotation.transpose()

            self._cache[cache_entry] = (positions, normals)

        return self._cache[cache_entry]
