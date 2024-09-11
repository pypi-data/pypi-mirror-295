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

import brick.structure.checker as ch_
import brick.structure.explorer as ex_
import brick.interface.io.reporting as mg_
from brick.marked_point.generic import marked_point_t
from brick.data.type import array_t

from abc import ABCMeta, abstractmethod
from collections import namedtuple as namedtuple_t
from typing import Any

import numpy as nmpy


# dom_lengths: the lengths of the sampling domain for marked point positions
signals_t = namedtuple_t(
    "signals_t", "dom_lengths signal_for_qty signal_for_stat signal_for_dsp"
)


class quality_env_t(metaclass=ABCMeta):

    # Note: Using "pass" instead of "raise NotImplementedError" in abstract methods below

    @staticmethod
    @abstractmethod
    def SignalsFromRawSignal(
        raw_signal: Any, mkpt_dim: int, vmap: Any = None, **kwargs,
    ) -> signals_t:
        """
        This function must keep vmap as an optional parameter because, although the vmap will be passed to the signal
        context, it is not known in general how the signal will be affected by vmap. Example: for the gradient-based
        quality, the vmap is used on the gradient components.
        """
        pass

    @staticmethod
    def SignalsFromRawSignalIdentity(
        raw_signal: Any, mkpt_dim: int, vmap: array_t = None
    ) -> signals_t:
        #
        if not isinstance(raw_signal, array_t):
            raise ValueError("Signal domain cannot be determined for non-array signal")

        signal = raw_signal.astype(nmpy.float64)  # Always return a copy, as needed

        if vmap is not None:
            nan_map = nmpy.logical_not(vmap.astype(nmpy.bool_, copy=False))
            if nan_map.ndim == signal.ndim:
                signal[nan_map] = nmpy.nan
            elif nan_map.ndim == signal.ndim - 1:
                # TODO: is there a simpler way?
                slices = (signal.ndim - 1) * (slice(None),)
                for idx in range(signal.shape[-1]):
                    signal[slices + (slice(idx, idx + 1),)][nan_map] = nmpy.nan
            else:
                raise ValueError(
                    f"Signal/Validity map{mg_.SEP}Incompatible dimensions; "
                    f"Signal={signal.ndim}; Validity map={nan_map.ndim}; "
                    f"Expected validity map dimension={signal.ndim} or {signal.ndim-1}"
                )

        signals = signals_t(
            dom_lengths=signal.shape[:mkpt_dim],
            signal_for_qty=signal,
            signal_for_stat=signal,
            signal_for_dsp=signal,
        )

        return signals

    @staticmethod
    @abstractmethod
    def MKPTQuality(mkpt: marked_point_t, **kwargs) -> float:
        pass

    @classmethod
    def CheckEnvironment(cls, sig_prg_prm: dict, mkt_qpm_prm: dict) -> None:
        #
        ch_.CheckPassedParameters(
            cls.SignalsFromRawSignal.__name__,
            ex_.FunctionInfos(cls.SignalsFromRawSignal),
            sig_prg_prm,
            2,
        )
        ch_.CheckPassedParameters(
            cls.MKPTQuality.__name__,
            ex_.FunctionInfos(cls.MKPTQuality),
            mkt_qpm_prm,
            1,
        )
