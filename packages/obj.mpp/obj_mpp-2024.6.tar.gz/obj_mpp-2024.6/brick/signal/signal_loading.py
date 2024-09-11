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

import brick.interface.io.reporting as mg_
from brick.data.type import array_t, path_h

from os import DirEntry as doc_info_t
from pathlib import Path as pl_path_t
from typing import Any, Callable, Optional, Sequence, Tuple, Union

import numpy as nmpy


# Some object defining the signal and a validity map
signal_details_t = Tuple[Any, Optional[array_t]]


def MKPTCenterMapOrPDF(
    path: pl_path_t, SignalLoading_fct: Callable, mkpt_dim: int
) -> array_t:
    #
    output, _ = SignalLoading_fct(path, mkpt_dim=mkpt_dim)

    if isinstance(output, array_t):
        pass
    elif isinstance(output, nmpy.lib.npyio.NpzFile):
        # Typically when SignalLoading_fct is helper.signal_loading.NumpySignal
        keys = tuple(output.keys())
        output = output[keys[0]]
    else:
        raise TypeError(
            f"{type(output)}{mg_.SEP}Invalid signal type; "
            f"Expected={array_t}, {nmpy.lib.npyio.NpzFile}"
        )
    CheckCenterMapOrPDF(output, mkpt_dim)

    return output


def CheckPathExtension(
    path: path_h, valid_extension: Union[str, Sequence[str]]
) -> None:
    #
    if isinstance(valid_extension, str):
        valid_extension = tuple(valid_extension)
    valid_extension = tuple("." + extension.lower() for extension in valid_extension)

    if isinstance(path, str):
        validities = (path.lower().endswith(extension) for extension in valid_extension)
    elif isinstance(path, pl_path_t):
        validities = (path.suffix.lower() == extension for extension in valid_extension)
    elif isinstance(path, doc_info_t):
        validities = (
            path.name.lower().endswith(extension) for extension in valid_extension
        )
    else:
        raise TypeError(
            f"{type(path)}{mg_.SEP}Invalid path type; "
            f"Expected={str}, {pl_path_t}, {doc_info_t}"
        )

    if not any(validities):
        raise ValueError(
            f"{path}{mg_.SEP}Invalid extension; Expected={valid_extension}"
        )


# The functions below are provided as helpers for actual signal loading functions.
# For this reason, they are placed here instead of being part of the signal_context module.


def CheckRawSignal(raw_signal: array_t, mkpt_dim: int) -> None:
    #
    signal_dim = raw_signal.ndim
    if (signal_dim < mkpt_dim) or (signal_dim > mkpt_dim + 1):
        raise ValueError(
            f"Raw signal{mg_.SEP}Invalid dimension; "
            f"Actual={signal_dim}; Expected={mkpt_dim} or {mkpt_dim+1}"
        )


# TODO: currently CheckValidityMap and CheckCenterMapOrPDF are identical up to the execption message "title"
# This could change since the validity map could be more general than just an array of the same
# dimension of mkpt position domain
def CheckValidityMap(validity_map: array_t, mkpt_dim: int) -> None:
    #
    if validity_map.ndim != mkpt_dim:
        raise ValueError(
            f"Validity map{mg_.SEP}Invalid dimension; "
            f"Actual={validity_map.ndim}; Expected={mkpt_dim}"
        )


def CheckRawSignalAndVMapCoherence(
    raw_signal: array_t, validity_map: array_t, mkpt_dim: int
) -> None:
    #
    if validity_map.shape != raw_signal.shape[:mkpt_dim]:
        if raw_signal.ndim == mkpt_dim:
            image_lenths_as_str = raw_signal.shape.__str__()
        else:
            image_lenths_as_str = f"{raw_signal.shape[:-1]}[,{raw_signal.shape[-1]}]"
        raise ValueError(
            f"Raw signal/Validity map{mg_.SEP}Size mismatch; "
            f"Image={image_lenths_as_str}; Validity map={validity_map.shape}"
        )


def CheckCenterMapOrPDF(map_or_pdf: array_t, mkpt_dim: int) -> None:
    #
    if map_or_pdf.ndim != mkpt_dim:
        raise ValueError(
            f"Center PDF{mg_.SEP}Invalid dimension; "
            f"Actual={map_or_pdf.ndim}; Expected={mkpt_dim}"
        )
