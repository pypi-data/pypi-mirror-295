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

import csv as cv_
import json as js_
import sys as sy_
from typing import BinaryIO, Sequence, TextIO

import brick.interface.io.reporting as mg_
import brick.marked_point.mkpt_list as ml_
from brick.marked_point.generic import marked_point_t


def LengthOfCommonRuntimeUIDPrefix(mkpt_lst: Sequence[marked_point_t]) -> int:
    #
    output = 1

    if mkpt_lst.__len__() > 1:
        uids = sorted(mkpt.runtime_uid for mkpt in mkpt_lst)
        first = uids[0]
        last = uids[-1]
        while first.startswith(last[:output]):
            output += 1

    return output - 1


def ReportDetectionStatus() -> None:
    #
    pass  # Not sure if this is appropriate here, or better in mpp.py
    # if pid == 1:
    #     if (it_idx is not None) and (it_idx >= 0):
    #         mg_.ReportI(f"it.{it_idx}: {detected_so_far.__len__()}mkpt(s)")
    #
    #     if (it_idx is None) or (it_idx >= 0):
    #         th_.Timer(status_period, ReportDetectionStatus).start()


def ReportDetectionResult(
    mkpt_lst: Sequence[marked_point_t], start_as_str: str
) -> None:
    #
    locrup = LengthOfCommonRuntimeUIDPrefix(mkpt_lst)

    mg_.ReportI(f"MKPT(s) @ {start_as_str}")
    if mg_.TARGET is sy_.stdout:
        for mkpt in mkpt_lst:
            mg_.ReportI(mkpt.AsColoredStr(locrup=locrup))
    else:
        # Any object that has a "write" method (typically, a widget of a GI)
        ReportDetectedMarkedPointsInCSVFormat(mkpt_lst, locrup)


def ReportDetectedMarkedPointsInCSVFormat(
    mkpt_lst: Sequence[marked_point_t], locrup: int
) -> None:
    #
    header_as_list = mkpt_lst[0].__class__.TupledDescriptionHeader(w_prologue=True)
    mg_.ReportI(", ".join(header_as_list))

    for mkpt in mkpt_lst:
        mp_as_lst = (
            elm.__str__()
            for elm in mkpt.TupledDescription(locrup=locrup, w_prologue=True)
        )
        mg_.ReportI(", ".join(mp_as_lst))


def SaveDetectionInCSVFormat(
    mkpt_lst: Sequence[marked_point_t], csv_accessor: TextIO, sep: str = ","
) -> None:
    #
    if mkpt_lst.__len__() == 0:
        return

    # Originally, the code used __class__ and isinstance. But this does not always work as expected!
    # See https://stackoverflow.com/questions/10582774/python-why-can-isinstance-return-false-when-it-should-return-true
    # for example.
    mp_class = mkpt_lst[0].__class__
    mp_class_name = mp_class.__name__
    if any(mkpt.__class__.__name__ != mp_class_name for mkpt in mkpt_lst[1:]):
        types = set(mkpt.__class__.__name__ for mkpt in mkpt_lst)
        mg_.ReportW(
            None, f"Types{mg_.SEP}Mixed types in mkpt list in CSV output: {types}"
        )

    csv_writer = cv_.writer(csv_accessor, delimiter=sep)

    csv_writer.writerow(
        mp_class.TupledDescriptionHeader(w_prologue=True, educated_version=True)
        + mkpt_lst[0].SignalStatistics(header_instead=True)
        + ml_.SignalStatiticsInBackground(None)
    )

    locrup = LengthOfCommonRuntimeUIDPrefix(mkpt_lst)
    bck_stat = ml_.SignalStatiticsInBackground(mkpt_lst)
    for mkpt in mkpt_lst:
        csv_writer.writerow(
            mkpt.TupledDescription(
                locrup=locrup, w_prologue=True, educated_version=True
            )
            + mkpt.SignalStatistics()
            + bck_stat
        )


def SaveDetectionInFormatForRebuilding(
    mkpt_lst: Sequence[marked_point_t],
    doc_accessor: BinaryIO,
) -> None:
    #
    if mkpt_lst.__len__() == 0:
        return

    for mkpt in mkpt_lst:
        json = js_.dumps(mkpt.AsJSONableDict()) + "\n"
        doc_accessor.write(json.encode())
