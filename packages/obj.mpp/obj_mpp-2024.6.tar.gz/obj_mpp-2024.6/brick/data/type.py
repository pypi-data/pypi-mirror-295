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

# _t suffix: use in isinstance
# _h suffix: use for static type checking (type hint)

import brick.interface.io.reporting as rp_

import builtins
from os import DirEntry as doc_info_t
from pathlib import Path as pl_path_t
from typing import Tuple, Union

import numpy as nmpy


BUILTIN_TYPES = tuple(getattr(builtins, t) for t in dir(builtins) if isinstance(getattr(builtins, t), type))

# TODO: add types for int and float throughout the code so that int and numpy.ints are not mixed
number_t = (int, float)
number_h = Union[number_t]

lengths_t = Tuple[int, ...]

array_t = nmpy.ndarray

path_t = (str, pl_path_t, doc_info_t)
path_h = Union[path_t]


def IsNumber(value):
    #
    return (
        isinstance(value, int)
        or isinstance(value, nmpy.integer)
        or isinstance(value, float)
        or isinstance(value, nmpy.floating)
    )


def PathAsStr(path: path_h) -> str:
    #
    if isinstance(path, str):
        path_as_str = path
    elif isinstance(path, pl_path_t):
        path_as_str = path.__str__()
    elif isinstance(path, doc_info_t):
        path_as_str = path.path
    else:
        raise TypeError(
            f"{type(path)}{rp_.SEP}Invalid path type; "
            f"Accepted type={str}, {pl_path_t}, {doc_info_t}"
        )

    return path_as_str
