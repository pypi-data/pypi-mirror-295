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

import sys as sstm
import tempfile as tp_
from typing import Optional, Sequence

import imageio as io_
import numpy as nmpy

import brick.interface.io.mkpt_list as ioml
import brick.interface.io.reporting as mg_
import brick.marked_point.mkpt_list as ml_
from brick.data.type import pl_path_t
from brick.marked_point.generic import marked_point_t


def CreateOutputFolder(output_folder: pl_path_t, /) -> pl_path_t:
    #
    if not output_folder.exists():
        try:
            output_folder.mkdir()
        except Exception as error:
            mg_.ReportE(
                output_folder.__str__(),
                f"Folder creation failed with error:\n" f"{error}",
            )
            output_folder = pl_path_t(tp_.mkdtemp())
            mg_.ReportI(f"{output_folder}: Temporary alternative output folder")

    return output_folder


def OutputDocName(
    output_path: pl_path_t,
    basename: str,
    extension: str,
    start_as_str: Optional[str],
    signal_id: Optional[str],
    /,
) -> pl_path_t:
    #
    if signal_id is None:
        # For interactive workflow where path was chosen by user
        output = output_path
    else:
        # For non-interactive workflow where path is chosen by Obj.MPP
        output = output_path / f"{signal_id}-{basename}-{start_as_str}.{extension}"

    return output


def SaveDetectionInCSVFormat(
    mkpt_lst: Sequence[marked_point_t],
    signal_id: Optional[str],
    start_as_str: Optional[str],
    output_path: pl_path_t,
    /,
    *,
    sep: str = ",",
) -> None:
    #
    fullname = OutputDocName(output_path, "marks", "csv", start_as_str, signal_id)
    with open(fullname, "w", encoding=sstm.getfilesystemencoding()) as csv_accessor:
        ioml.SaveDetectionInCSVFormat(mkpt_lst, csv_accessor, sep=sep)


def SaveDetectionInFormatForRebuilding(
    mkpt_lst: Sequence[marked_point_t],
    signal_id: Optional[str],
    start_as_str: Optional[str],
    output_path: pl_path_t,
    /,
) -> None:
    #
    fullname = OutputDocName(output_path, "mkpt", "json", start_as_str, signal_id)
    with open(fullname, "wb") as doc_accessor:
        ioml.SaveDetectionInFormatForRebuilding(mkpt_lst, doc_accessor)


def SaveDetectionAsContourImage(
    mkpt_dim: int,
    mkpt_lst: Sequence[marked_point_t],
    signal_id: Optional[str],
    start_as_str: Optional[str],
    output_path: pl_path_t,
    /,
) -> None:
    #
    contour_map = ml_.ContourMapOfDetection(mkpt_lst)
    if mkpt_dim == 2:
        fullname = OutputDocName(output_path, "contour", "png", start_as_str, signal_id)
        io_.imwrite(fullname, contour_map)
    elif mkpt_dim == 3:
        fullname = OutputDocName(output_path, "contour", "tif", start_as_str, signal_id)
        io_.volwrite(fullname, contour_map)
    else:
        mg_.ReportW(
            None,
            f"Contour output in {mkpt_dim}-D not implemented",
        )


def SaveDetectionAsRegionImage(
    mkpt_dim: int,
    mkpt_lst: Sequence[marked_point_t],
    signal_id: Optional[str],
    start_as_str: Optional[str],
    output_path: pl_path_t,
    /,
) -> None:
    #
    region_map = ml_.RegionMapOfDetection(mkpt_lst)
    if mkpt_dim == 2:
        fullname = OutputDocName(output_path, "region", "png", start_as_str, signal_id)
        io_.imwrite(fullname, region_map)
    elif mkpt_dim == 3:
        fullname = OutputDocName(output_path, "region", "tif", start_as_str, signal_id)
        io_.volwrite(fullname, region_map)
    else:
        mg_.ReportW(
            None,
            f"Region output in {mkpt_dim}-D not implemented",
        )


def SaveDetectionAsRegionNumpyArray(
    _: int,
    mkpt_lst: Sequence[marked_point_t],
    signal_id: Optional[str],
    start_as_str: Optional[str],
    output_path: pl_path_t,
    /,
) -> None:
    #
    region_map = ml_.RegionMapOfDetection(mkpt_lst)
    fullname = OutputDocName(output_path, "region", "npz", start_as_str, signal_id)
    nmpy.savez_compressed(fullname, detection=region_map)
