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
import brick.mpp as mp_
from brick.marked_point.generic import marked_point_t

import multiprocessing as ll_
from typing import List, Optional, Sequence, Tuple


def FromTosInHigherDimensions(
    mkpt_dim: int, signal_size: Sequence[int]
) -> Tuple[int, ...]:
    """
    Higher=for dimensions higher than the first one
    """
    return tuple(
        item
        for sublist in zip(
            (mkpt_dim - 1) * (0,), (size - 1 for size in signal_size[1:])
        )
        for item in sublist
    )


def DetectedObjectsInOneChunk(
    mkt_bth_prm,
    mkt_ict_prm,
    mkt_cst_prm,
    mkt_qty_prm,
    alg_mpp_prm,
    alg_ref_prm,
    alg_fbk_prm,
    previous_mkpt_lst,
    mkpt_t,
    sampler,
    MKPTQuality_fct,
    higher_from_tos,
    from_to: tuple,
    pid: int = 1,
    queue: Optional[ll_.Queue] = None,
) -> Optional[List[marked_point_t]]:
    #
    if mkt_bth_prm["center_rng"] is None:
        local_center_rng = (*from_to, *higher_from_tos)
    elif isinstance(mkt_bth_prm["center_rng"], tuple):
        local_center_rng = (
            max(from_to[0], mkt_bth_prm["center_rng"][0]),
            min(from_to[1], mkt_bth_prm["center_rng"][1]),
            *mkt_bth_prm["center_rng"][2:],
        )
        if local_center_rng[0] > local_center_rng[1]:
            return
    else:
        # isinstance(mkt_bth_prm['center_rng'], array_t)
        local_center_rng = mkt_bth_prm["center_rng"].copy()
        local_center_rng[: from_to[0], ...] = 0
        local_center_rng[(from_to[1] + 1) :, ...] = 0
        if (local_center_rng == 0).all():
            return
    sampler.SetPointParameters(local_center_rng)

    n_iterations = alg_mpp_prm["n_iterations"]
    min_quality = mkt_qty_prm["min_quality"]

    mkpt_lst, journal = mp_.DetectedObjects(
        previous_mkpt_lst,
        mkpt_t,
        MKPTQuality_fct,
        sampler,
        n_iterations=n_iterations,
        n_births_per_iteration=alg_mpp_prm["n_births_per_iteration"],
        only_uncropped=mkt_bth_prm["only_uncropped"],
        age_for_refinement=alg_ref_prm["age_for_refinement"],
        n_refinement_attempts=alg_ref_prm["n_refinement_attempts"],
        refinement_fraction=alg_ref_prm["refinement_fraction"],
        min_quality=min_quality,
        area_weight=mkt_ict_prm["area_weight"],
        overlap_tolerance=mkt_cst_prm["overlap_tolerance"],
        status_period=alg_fbk_prm["status_period"],
        pid=pid,
        queue=queue,
    )

    ct_min, ct_sec = journal.summary["computation_time"]  # ct=computation time
    msg_introduction = f"{pid}-IT.{n_iterations} in {ct_min}m{ct_sec}s: "
    if mkpt_lst.__len__() > 0:
        mg_.ReportI(
            msg_introduction + f"{mkpt_lst.__len__()}mkpt(s) "
            f"with quality in ["
            f"{mkpt_lst[-1].quality:.3f},"
            f"{mkpt_lst[0].quality:.3f}] "
            f">= {min_quality}",
        )
    else:
        mg_.ReportI(msg_introduction + "0mkpt")
    for name, value in journal.summary.items():
        if "computation" not in name:
            mg_.ReportI(f"    {name} = {value}")
    for name, value in journal.metrics.items():
        mg_.ReportI(f"    {name} = {value}")

    if queue is None:
        return mkpt_lst
