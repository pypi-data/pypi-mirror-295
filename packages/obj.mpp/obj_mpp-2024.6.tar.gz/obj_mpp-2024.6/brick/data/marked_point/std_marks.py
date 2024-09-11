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

from collections import namedtuple as named_tuple_t

import numpy as nmpy


mark_details_t = named_tuple_t(
    "mark_details_t",
    "type min max min_inclusive max_inclusive default_range default_precision",
)


STD_DETAILS_RADIUS = mark_details_t(
    type=float,
    min=0.0,
    max=nmpy.finfo(float).max,
    min_inclusive=False,
    max_inclusive=True,
    default_range=(1.0, 2.0),#None, # TODO: if None, mark is not recognized as a potential tuple
    default_precision=0.5,
)

STD_DETAILS_RADII_RATIO = mark_details_t(
    type=float,
    min=1.0,
    max=nmpy.finfo(float).max,
    min_inclusive=True,
    max_inclusive=True,
    default_range=(1.0, 2.0),
    default_precision=None,
)


STD_DETAILS_ANGLE_0_5PI = mark_details_t(
    type=float,
    min=0.0,
    max=0.5 * nmpy.pi,
    min_inclusive=True,
    max_inclusive=False,
    default_range=(0.0, 0.5 * nmpy.pi),
    default_precision=0.25 * 5.0 * nmpy.pi / 180.0,
)

STD_DETAILS_ANGLE_PI = mark_details_t(
    type=float,
    min=0.0,
    max=nmpy.pi,
    min_inclusive=True,
    max_inclusive=False,
    default_range=(0.0, nmpy.pi),
    default_precision=0.5 * 5.0 * nmpy.pi / 180.0,
)

STD_DETAILS_ANGLE_2PI = mark_details_t(
    type=float,
    min=0.0,
    max=2.0 * nmpy.pi,
    min_inclusive=True,
    max_inclusive=False,
    default_range=(0.0, 2.0 * nmpy.pi),
    default_precision=5.0 * nmpy.pi / 180.0,
)
