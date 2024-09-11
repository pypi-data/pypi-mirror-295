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

import time as tm_
from typing import Any, Dict, List, Tuple


class journal_t:
    #
    __slots__ = ("summary", "metrics", "contents", "material")
    summary: Dict[str, Any]
    metrics: Dict[str, Any]
    # Tuple=time as returned by time.time and note
    contents: List[Tuple[float, str]]
    material: Dict[str, Any]

    def __init__(self) -> None:
        #
        self.summary = {}
        self.metrics = {}
        self.contents = []
        self.material = {}

    def NoteDownComputationStartTime(self) -> None:
        #
        self.summary["computation_start"] = tm_.time()

    def NoteDownComputationEndTime(self) -> None:
        #
        self.summary["computation_end"] = tm_.time()
        # Computation time in minutes and seconds
        self.summary["computation_time"] = divmod(
            round(tm_.time() - self.summary["computation_start"]), 60
        )

    def AddToSummary(self, entry: str, contents: Any) -> None:
        #
        self.summary[entry] = contents

    def CreateMetric(self, name: str, initial_value: Any) -> None:
        #
        self.metrics[name] = initial_value

    def UpdateMetric(self, name: str, increment: Any) -> None:
        #
        self.metrics[name] += increment

    def AddNote(self, note: str) -> None:
        #
        self.contents.append((tm_.time(), note))

    def AddMaterial(self, name: str, contents: Any) -> None:
        #
        self.material[name] = contents
