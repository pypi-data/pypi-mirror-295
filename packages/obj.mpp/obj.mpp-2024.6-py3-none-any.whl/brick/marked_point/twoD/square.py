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
from brick.data.marked_point.std_marks import STD_DETAILS_ANGLE_0_5PI
from brick.marked_point.twoD.generic import marked_point_t
from brick.marked_point.twoD.rectangle import rectangle_t

from typing import Sequence, Tuple

import numpy as nmpy


class square_t(rectangle_t):

    marks_details = {
        "semi_minor_axis": None,  # To guarantee the same order of marks as in __init__ (/!\ It relies on dict respecting this order)
        "angle": STD_DETAILS_ANGLE_0_5PI,
    }
    marks_details["semi_minor_axis"] = rectangle_t.marks_details["semi_minor_axis"]
    marks_translations = {"half_side": "semi_minor_axis"}

    # --- INSTANTIATE

    def __init__(
        self,
        center: Sequence[int],
        half_side: int,
        angle: float,
        check_marks: bool = True,
    ) -> None:
        #
        super().__init__(center, half_side, 1.0, angle, check_marks=check_marks)

    @classmethod
    def NormalizeMarkRanges(cls, mk_ranges: dict) -> None:
        #
        # cls._ConvertAngleRangeToRadians("angle", mk_ranges)
        marked_point_t.CheckMarkRanges(
            mk_ranges, cls.marks_details, cls.marks_translations
        )
        marked_point_t.AddDefaultsToMarkRanges(mk_ranges, cls.marks_details)

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
                + "S+"
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
            self.marks["angle"],
            self.marks["angle"] * 180.0 / nmpy.pi,
        )

    @staticmethod
    def EducatedMarksHeaders() -> Tuple[str, ...]:
        #
        return "Radius", "Angle (radian)", "Angle (degree)"
