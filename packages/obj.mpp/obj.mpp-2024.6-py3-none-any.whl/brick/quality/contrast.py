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

from brick.data.type import array_t
from brick.interface.io import reporting as rp_
from brick.marked_point.generic import marked_point_t
from brick.quality.definition import mp_quality
from brick.quality.generic import quality_env_t
from brick.signal.constant import INFINITY_NUMPY_FLOAT, INFINITY_NUMPY_INT
from brick.signal.signal_context import signal_context_t

from typing import Tuple

import numpy as nmpy


@mp_quality
def _BrightOnDarkContrast(
    mkpt: marked_point_t,
    ring_thickness_ext: int = 1,
    ring_thickness_int: int = INFINITY_NUMPY_INT,
    normalized: bool = False,
    signal: array_t = None,
) -> float:
    #
    # The signal argument gives the option to use the quality function independently of the normal, behind-the-scene
    # management with signal_context_t.
    #
    # The Region method must accept positive and negative (if not nmpy.isinf(ring_thickness_int)) dilation parameters
    #
    mkpt_bmap = mkpt.region
    bmap_dilated, dilated_bbox_domain = mkpt.Region(ring_thickness_ext)
    if signal is None:
        signal = signal_context_t.signal_for_qty

    sum_bmap, area_bmap, sum2_bmap = _SumsAndArea(
        signal[mkpt.bbox.domain], mkpt_bmap, normalized
    )
    sum_dilated, area_dilated, sum2_dilated = _SumsAndArea(
        signal[dilated_bbox_domain], bmap_dilated, normalized
    )
    if area_dilated <= area_bmap:
        # Equality is possible if mkpt is surrounded only by invalid sites
        return -INFINITY_NUMPY_FLOAT

    if ring_thickness_int == INFINITY_NUMPY_INT:
        sum_eroded = area_eroded = sum2_eroded = 0
    else:
        bmap_eroded, eroded_bbox_domain = mkpt.Region(-ring_thickness_int)
        sum_eroded, area_eroded, sum2_eroded = _SumsAndArea(
            signal[eroded_bbox_domain], bmap_eroded, normalized
        )
        if area_eroded >= area_bmap:
            rp_.BugException(f"{area_eroded} >= {area_bmap}")

    area_ext = area_dilated - area_bmap
    area_int = area_bmap - area_eroded
    # At this point, these areas cannot be equal to zero

    average_ext = (sum_dilated - sum_bmap) / area_ext
    average_int = (sum_bmap - sum_eroded) / area_int

    if normalized:
        var_ext = ((sum2_dilated - sum2_bmap) / area_ext) - average_ext ** 2
        var_int = ((sum2_bmap - sum2_eroded) / area_int) - average_int ** 2

        return (average_int - average_ext) / (var_int * var_ext) ** 0.25
    else:
        return average_int - average_ext


@mp_quality
def _DarkOnBrightContrast(
    mkpt: marked_point_t,
    ring_thickness_ext: int = 1,
    ring_thickness_int: int = INFINITY_NUMPY_INT,
    normalized: bool = False,
    signal: array_t = None,
) -> float:
    #
    # The signal argument gives the option to use the quality function independently of the normal, behind-the-scene
    # management with signal_context_t.
    #
    # See _BrightOnDarkContrast for conditions
    #
    contrast = _BrightOnDarkContrast(
        mkpt,
        ring_thickness_ext=ring_thickness_ext,
        ring_thickness_int=ring_thickness_int,
        normalized=normalized,
        signal=signal,
    )
    # TODO: What is this???
    if contrast == -INFINITY_NUMPY_FLOAT:
        return -INFINITY_NUMPY_FLOAT

    return -contrast


def _SumsAndArea(
    local_signal: array_t, mkpt_bmap: array_t, with_sum_of_sq: bool
) -> Tuple[float, float, float]:
    #
    img_values = local_signal[mkpt_bmap]

    area_msk = float(nmpy.count_nonzero(mkpt_bmap))
    sum_bmap = float(img_values.sum())
    if with_sum_of_sq:
        sum_of_sq = float((img_values ** 2).sum())
    else:
        sum_of_sq = None

    return sum_bmap, area_msk, sum_of_sq


# class contrast_t(quality_env_t):
#     # This class could be used to factorize SignalsFromRawSignal, but is it worth it?
#     SignalsFromRawSignal = quality_env_t.SignalsFromRawSignalIdentity


class bright_on_dark_contrast_t(quality_env_t):
    #
    SignalsFromRawSignal = quality_env_t.SignalsFromRawSignalIdentity
    MKPTQuality = _BrightOnDarkContrast


class dark_on_bright_contrast_t(quality_env_t):
    #
    SignalsFromRawSignal = quality_env_t.SignalsFromRawSignalIdentity
    MKPTQuality = _DarkOnBrightContrast
