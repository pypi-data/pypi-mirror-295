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

from typing import Union

import brick.interface.io.reporting as mg_
from brick.data.type import array_t
from brick.marked_point.generic import marked_point_t
from brick.signal.signal_context import signal_context_t
from brick.quality.definition import mp_quality
from brick.quality.generic import quality_env_t

import numpy as nmpy

from enum import Enum as enum_t#, auto as EAuto


# noinspection PyArgumentList
# measure_e = enum_t("measure_e", "MEAN STDDEV VARIANCE MEDIAN MIN MAX")
class measure_e(enum_t):
    #
    MEAN=1 #= EAuto()
    STDDEV=2 #= EAuto()
    VARIANCE=3 #= EAuto()
    MEDIAN=4 #= EAuto()
    MIN=5 #= EAuto()
    MAX=6 #= EAuto()


@mp_quality
def _SignalOnContour(
    mkpt: marked_point_t,
    measure: Union[measure_e, str] = measure_e.MEAN,
    signal: array_t = None,
) -> float:
    #
    # The signal argument gives the option to use the quality function independently of the normal, behind-the-scene
    # management with signal_context_t.
    #
    domain = mkpt.bbox.domain
    contour = mkpt.Contour()
    # Cannot be empty (see Contour)
    if signal is None:
        signal = signal_context_t.signal_for_qty[domain][contour]

    if isinstance(measure, str):
        # For example "measure_e.MEAN"
        measure = measure_e(measure[10:])

    if measure == measure_e.MEAN:
        return signal.mean().item()
    elif measure == measure_e.STDDEV:
        return signal.std().item()
    elif measure == measure_e.VARIANCE:
        return signal.var().item()
    elif measure == measure_e.MEDIAN:
        return signal.median().item()
    elif measure == measure_e.MIN:
        return nmpy.min(signal).item()
    elif measure == measure_e.MAX:
        return nmpy.max(signal).item()
    else:
        raise ValueError(f"{measure}{mg_.SEP}Invalid measure")


class contour_t(quality_env_t):
    #
    SignalsFromRawSignal = quality_env_t.SignalsFromRawSignalIdentity
    MKPTQuality = _SignalOnContour
