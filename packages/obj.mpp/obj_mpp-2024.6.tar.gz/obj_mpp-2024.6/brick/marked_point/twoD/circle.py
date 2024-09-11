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
from brick.marked_point.twoD.ellipse import ellipse_t
from brick.marked_point.twoD.generic import marked_point_t

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
        ct_.c_void_p,
    )


class circle_t(ellipse_t):

    marks_details = {"semi_minor_axis": ellipse_t.marks_details["semi_minor_axis"]}
    marks_translations = {"radius": "semi_minor_axis"}

    # --- INSTANTIATE

    def __init__(
        self, center: Sequence[int], radius: int, check_marks: bool = True
    ) -> None:
        #
        super().__init__(center, radius, 1.0, 0.0, check_marks=check_marks)

    @classmethod
    def NormalizeMarkRanges(cls, mk_ranges: dict) -> None:
        #
        marked_point_t.CheckMarkRanges(
            mk_ranges, cls.marks_details, cls.marks_translations
        )
        marked_point_t.AddDefaultsToMarkRanges(mk_ranges, cls.marks_details)

    def _CoarseBoundingBoxHalfLengths(self) -> Tuple[int, ...]:
        #
        radius = ma_.ceil(self.marks["semi_minor_axis"]).__int__()

        return radius, radius

    # --- REPORT

    def AsColoredStr(self, locrup: int = 0) -> str:
        #
        cache_entry = self.AsColoredStr.__name__

        if cache_entry not in self._cache:
            formatted_marks = tc_.ColoredText(
                f'{self.marks["semi_minor_axis"]:.2f}', "red"
            )

            self._cache[cache_entry] = (
                self.runtime_uid[locrup:]
                + " "
                + "C+"
                + self.FormattedPosition()
                + formatted_marks
                + self.FormattedQuality()
            )

        return self._cache[cache_entry] + self.FormattedAge()

    @property
    def educated_marks(self) -> tuple:
        #
        return self.marks["semi_minor_axis"],

    @staticmethod
    def EducatedMarksHeaders() -> Tuple[str, ...]:
        #
        return "Radius",

    # --- COMPUTE

    def _RawRegion(self) -> array_t:
        #
        # enclosing_radius = ma_.ceil(self.marks["semi_minor_axis"]).__int__()
        # coarse_domain = self._CoarseDomainFromEnclosingRadius(enclosing_radius)
        #
        sig_grid_coords = signal_context_t.grid_coords
        if _RawRegion_C is None:
            centered_rows = sig_grid_coords[0][self.bbox.domain] - self.position[0]
            centered_cols = sig_grid_coords[1][self.bbox.domain] - self.position[1]

            sq_1_level_map = (centered_rows ** 2 + centered_cols ** 2) * (
                1.0 / self.marks["semi_minor_axis"] ** 2
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
                region.ctypes.data,
            )

        return region

    def Normals(self) -> Tuple[array_t, ...]:
        #
        cache_entry = self.Normals.__name__

        if cache_entry not in self._cache:
            positions = self.Contour().nonzero()
            # Cannot be empty since contour cannot be empty

            normals = nmpy.transpose(positions).astype(nmpy.float64) + [
                [
                    self.bbox.mins[0] - self.position[0],
                    self.bbox.mins[1] - self.position[1],
                ]
            ]

            normal_norms = nmpy.sqrt((normals ** 2).sum(axis=1, keepdims=True))
            # When the analytical normal expression is evaluated at (0,0), it results in a null normal. This
            # occurs whenever the contour "passes through the center" (very thick contour and/or very thin object).
            normal_norms[normal_norms == 0.0] = 1.0
            normals /= normal_norms

            self._cache[cache_entry] = (positions, normals)

        return self._cache[cache_entry]
