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

from brick.marked_point.generic import marked_point_t
from brick.signal.signal_context import signal_context_t
from brick.data.type import array_t

from typing import Optional, Sequence, Tuple, Union

import numpy as nmpy


def ContourMapOfDetection(mkpt_lst: Sequence[marked_point_t]) -> array_t:
    #
    # TODO: wouldn't it be better to take the contour of the region map since it deals with intersections?
    contour_map = nmpy.zeros(signal_context_t.lengths, dtype=nmpy.uint16, order="C")

    max_uint16 = nmpy.iinfo(nmpy.uint16).max
    if (n_mkpts := mkpt_lst.__len__()) > max_uint16:
        _PlotExclamationPoints(contour_map)
        print(
            f"{n_mkpts}: Number of marked points too high for storage as UInt16. Expected<={max_uint16}."
        )
        return contour_map

    for label, mkpt in enumerate(mkpt_lst):  # , start = 1): If not using max_uint16
        contour_map[mkpt.bbox.domain][mkpt.Contour()] = max_uint16 - label

    return contour_map


def RegionMapOfDetection(mkpt_lst: Sequence[marked_point_t]) -> array_t:
    #
    region_map = nmpy.zeros(signal_context_t.lengths, dtype=nmpy.uint16, order="C")

    max_uint16 = nmpy.iinfo(nmpy.uint16).max
    if (n_mkpts := mkpt_lst.__len__()) > max_uint16:
        _PlotExclamationPoints(region_map)
        print(
            f"{n_mkpts}: Number of marked points too high for storage as UInt16. Expected<={max_uint16}."
        )
        return region_map

    distance_map = nmpy.zeros_like(region_map, dtype=nmpy.float64, order="C")
    for label, mkpt in enumerate(mkpt_lst, start=1):
        local_dmp = distance_map[mkpt.bbox.domain]  # dmp=distance map
        mkpt_dmp = mkpt.InnerOneDistanceMap()
        mkpt_sites = mkpt_dmp > local_dmp

        local_dmp[mkpt_sites] = mkpt_dmp[mkpt_sites]
        region_map[mkpt.bbox.domain][mkpt_sites] = label

    return region_map


def SignalStatiticsInBackground(
    mkpt_lst: Optional[Sequence[marked_point_t]],
) -> Tuple[Union[float, str], ...]:
    #
    if mkpt_lst is None:
        return ("Bck Intensity",)

    signal = signal_context_t.signal_for_stat

    if isinstance(signal, array_t) and (signal.ndim == mkpt_lst[0].dim):
        bckgnd = nmpy.ones_like(signal, dtype=nmpy.bool_)
        for mkpt in mkpt_lst:
            bckgnd[mkpt.bbox.domain][mkpt.raw_region] = False
        if signal_context_t.invalidity_map is not None:
            vmap = nmpy.logical_not(signal_context_t.invalidity_map)
            bckgnd = nmpy.logical_and(bckgnd, vmap)

        return (signal[bckgnd].mean().item(),)
    else:
        return (nmpy.NaN,)


def _PlotExclamationPoints(array: array_t, /) -> None:
    """"""
    value = nmpy.iinfo(array.dtype).max

    half_width = array.shape[1] // 2
    half_half_width = half_width // 2
    half_bar_width = max(array.shape[1] // 20, 1)
    separation = max((2 * half_bar_width) // 4, 1)

    for col in (half_half_width, half_width, half_width + half_half_width):
        col_slice = slice(col - half_bar_width, col + half_bar_width)
        array[1 : (-2 * half_bar_width - separation - 1), col_slice] = value
        array[(-2 * half_bar_width - 1) : -1, col_slice] = value
