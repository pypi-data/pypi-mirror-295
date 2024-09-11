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
from brick.marked_point.generic import marked_point_t
from brick.signal.constant import INFINITY_NUMPY_FLOAT
from brick.signal.signal_context import signal_context_t
from brick.quality.definition import mp_quality
from brick.quality.generic import quality_env_t, signals_t
from brick.data.type import array_t

from abc import abstractmethod

import numpy as nmpy
import skimage.morphology as mp_


@mp_quality
def _DarkOnBrightGradient(
    mkpt: marked_point_t,
    max_hole_size: float = 1.0,  # in [0.0, 1.0]
    signal: array_t = None,
    _called_from_bod: bool = False,
) -> float:
    #
    # The signal argument gives the option to use the quality function independently of the normal, behind-the-scene
    # management with signal_context_t.
    #
    positions, normals = mkpt.Normals()
    n_positions = positions[0].__len__()
    # TODO: Normally this test is not necessary since Normals is never empty
    if n_positions == 0:
        return -INFINITY_NUMPY_FLOAT

    bbox = mkpt.bbox
    if signal is None:
        gradient = signal_context_t.signal_for_qty
    else:
        gradient = signal

    # print(gradient.__len__(), bbox.domain, positions.__len__(), normals.shape)
    qualities = nmpy.zeros(positions[0].shape, dtype=nmpy.float64, order="C")
    for idx in range(gradient.__len__()):
        qualities += normals[:, idx] * gradient[idx][bbox.domain][positions]
    if _called_from_bod:
        qualities *= -1.0
    quality = qualities.mean()

    if nmpy.isnan(quality):
        raise rp_.BugException()

    if max_hole_size == 1.0:
        return quality

    # TODO: check what happens at the frontier of validity

    percentile_low = nmpy.percentile(qualities, 33)
    percentile_hgh = nmpy.percentile(qualities, 66)
    hq_threshold = nmpy.mean(
        qualities[
            nmpy.logical_and(qualities >= percentile_low, qualities <= percentile_hgh)
        ]
    )
    high_quality_idc = qualities >= hq_threshold
    high_quality_points = tuple(
        positions[idx][high_quality_idc] for idx in range(positions.__len__())
    )

    contour = nmpy.zeros(bbox.lengths, dtype=nmpy.uint8)
    contour[high_quality_points] = 1

    max_hole_radius = nmpy.round(0.5 * max_hole_size * n_positions).__int__()
    if max_hole_radius > 0:
        contour = mp_.binary_dilation(contour, mp_.disk(max_hole_radius))

    if (contour[positions] == 1).all():
        return quality

    return -INFINITY_NUMPY_FLOAT


@mp_quality
def _BrightOnDarkGradient(mkpt: marked_point_t, max_hole_size: float = 1.0, signal: array_t = None) -> float:
    #
    # The signal argument gives the option to use the quality function independently of the normal, behind-the-scene
    # management with signal_context_t.
    #
    # See _DarkOnBrightGradient for conditions
    #
    return _DarkOnBrightGradient(
        mkpt, max_hole_size=max_hole_size, signal=signal, _called_from_bod=True
    )


class gradient_t(quality_env_t):
    #
    @staticmethod
    def SignalsFromRawSignal(
        raw_signal: array_t,
        mkpt_dim: int,
        vmap: array_t = None,
        unitary: bool = False,
    ) -> signals_t:
        #
        # CFD=Central Finite Differences
        # Even when unitary is False, the gradients are scaled so that the mean of their norm is 1
        #
        if raw_signal.ndim != mkpt_dim:
            raise ValueError(f"Raw signal{rp_.SEP}Invalid dimension: "
                             f"Actual_{raw_signal.ndim}; Expected_{mkpt_dim}")

        raw_signal = raw_signal.astype(nmpy.float64)
        gradient = list(nmpy.gradient(raw_signal))

        sq_gradient_sum = gradient[0] ** 2
        for grad_cmp in gradient[1:]:
            sq_gradient_sum += grad_cmp ** 2
        norm = nmpy.sqrt(sq_gradient_sum)

        if vmap is None:
            nan_map = None
        else:
            if vmap.ndim != mkpt_dim:
                raise ValueError(f"Validity map{rp_.SEP}Invalid dimension: "
                                 f"Actual_{vmap.ndim}; Expected_{mkpt_dim}")

            nan_map = nmpy.logical_not(vmap.astype(nmpy.bool_, copy=False))

        if unitary:
            norm[norm == 0.0] = 1.0
            for idx in range(gradient.__len__()):
                gradient[idx] /= norm
                if nan_map is not None:
                    gradient[idx][nan_map] = nmpy.nan
        else:
            mean_norm = norm.mean()
            if mean_norm == 0.0:
                mean_norm = 1.0
            for idx in range(gradient.__len__()):
                gradient[idx] /= mean_norm  # Normally never zero
                if nan_map is not None:
                    gradient[idx][nan_map] = nmpy.nan

        signals = signals_t(
            dom_lengths=raw_signal.shape,
            signal_for_qty=gradient,
            signal_for_stat=raw_signal,
            signal_for_dsp=raw_signal,
        )

        return signals

    @staticmethod
    @abstractmethod
    def MKPTQuality(mkpt: marked_point_t, **kwargs) -> float:
        pass


class bright_on_dark_gradient_t(gradient_t):
    #
    MKPTQuality = _BrightOnDarkGradient


class dark_on_bright_gradient_t(gradient_t):
    #
    MKPTQuality = _DarkOnBrightGradient
