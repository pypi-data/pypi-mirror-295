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
from brick.interface.io.journal import journal_t
from brick.marked_point.generic import marked_point_t
from brick.marked_point.sampler import sampler_t
from brick.quality.definition import mkpt_quality_fct_t
from brick.data.type import array_t
from brick.signal.constant import INFINITY_NUMPY_FLOAT

import threading as th_
from multiprocessing import Queue as mp_queue_t
from typing import List, Sequence, Tuple, cast

import networkx as gr_
import numpy as nmpy


def DetectedObjects(
    previous_mkpt_lst: Sequence[marked_point_t],
    mkpt_type: marked_point_t,
    MKPTQuality_fct: mkpt_quality_fct_t,
    sampler: sampler_t,
    n_iterations: int = 1,
    n_births_per_iteration: int = 1,
    only_uncropped: bool = True,
    age_for_refinement: int = None,
    n_refinement_attempts: int = 0,
    refinement_fraction: float = 0.0,
    min_quality: float = None,
    area_weight: float = 0.0,
    overlap_tolerance: float = 0.0,
    status_period: float = 0.0,
    pid: int = 1,
    queue: mp_queue_t = None,
) -> Tuple[List[marked_point_t], journal_t]:
    """
    Detects marked points using a function for measuring their quality.
    It seems to me that mkpt_type should be of type Type[marked_point_t] and not marked_point_t. But PyCharm complains
    in this case.
    """

    def _ReportStatus() -> None:
        #
        if (it_idx is not None) and (it_idx >= 0):
            mg_.ReportI(f"it.{it_idx}: {detected_so_far.__len__()}mkpt(s)")
        if (it_idx is None) or (it_idx >= 0):
            th_.Timer(status_period, _ReportStatus).start()

    if age_for_refinement is None:
        age_for_refinement = n_iterations + 1

    journal = journal_t()
    journal.CreateMetric("n_refinement_attempts", 0)
    journal.CreateMetric("n_refinements", 0)
    journal.NoteDownComputationStartTime()
    if (status_period > 0.0) and (pid == 1):
        it_idx = None  # Tells _ReportStatus that the main loop has not started yet
        _ReportStatus()

    if previous_mkpt_lst is None:
        detected_so_far = sampler.NonIntersectingSamples(
            mkpt_type,
            n_births_per_iteration,
            MKPTQuality_fct,
            min_quality,
            overlap_tolerance,
        )
    else:
        detected_so_far = previous_mkpt_lst

    n_non_blank_its = 0
    birth_efficiency = 0.0
    if area_weight > 0.0:
        area_normalization = mkpt_type.AreaNormalization(sampler)
    else:
        area_normalization = None
    for it_idx in range(n_iterations):
        newly_detected = sampler.NonIntersectingSamples(
            mkpt_type,
            n_births_per_iteration,
            MKPTQuality_fct,
            min_quality,
            overlap_tolerance,
        )
        n_newly_detected = newly_detected.__len__()
        if n_newly_detected == 0:
            continue
        n_non_blank_its += 1
        birth_efficiency += n_newly_detected / n_births_per_iteration

        UpdateDetectedSoFar(
            detected_so_far,
            newly_detected,
            area_normalization,
            area_weight,
            overlap_tolerance,
        )

        # Since detected_so_far can change (in some way; see below) inside the loop, it might be preferable
        # not to use enumerate below. However, it does not change length, so that "range on length" should be ok.
        for det_idx in range(detected_so_far.__len__()):
            detected_mkpt = detected_so_far[det_idx]
            detected_mkpt.age += 1
            if detected_mkpt.age < age_for_refinement:
                continue

            _RefineMKPT(
                detected_mkpt,
                det_idx,
                detected_so_far,
                overlap_tolerance,
                sampler,
                n_refinement_attempts,
                refinement_fraction,
                MKPTQuality_fct,
                journal,
            )

    # Partial mkpts were initially not considered at all (filtered out in NonIntersectingSamples and
    # SimilarMarkedPoints). However, this can lead to bad (but still "good" enough) mkpts touching or almost touching a
    # border. Instead, the partial mkpts are now kept to prevent such bad, border-touching mkpts, and removed only at
    # the end here.
    if only_uncropped:
        detected_so_far = [mkpt for mkpt in detected_so_far if not mkpt.crosses_border]
    detected_so_far.sort(key=lambda mkpt: mkpt.quality, reverse=True)

    if status_period > 0.0:
        it_idx = -1  # Tells _ReportStatus to stop reporting
    journal.NoteDownComputationEndTime()
    journal.AddToSummary("n_non_blank_iterations", n_non_blank_its)
    journal.CreateMetric(
        "birth_efficiency",
        f"{round(100.0 * birth_efficiency / max(1, n_non_blank_its))}%",
    )

    if queue is not None:
        queue.put(
            [
                (mkpt.position, *mkpt.raw_marks, mkpt.quality, mkpt.age)
                for mkpt in detected_so_far
            ]
        )

    return detected_so_far, journal


def UpdateDetectedSoFar(
    detected_so_far: list,
    newly_detected: list,
    area_normalization: Sequence[float],
    area_weight: float,
    overlap_tolerance: float,
) -> None:
    #
    graph = gr_.Graph()

    for mkpt_new in newly_detected:
        so_far_w_inter = tuple(
            mkpt_so_far
            for mkpt_so_far in detected_so_far
            if mkpt_new.Intersects(mkpt_so_far, overlap_tolerance)
        )
        if so_far_w_inter.__len__() == 0:
            continue

        # SFR=so far
        for mkpt_so_far in so_far_w_inter:
            if mkpt_so_far not in graph:
                weighted_quality = _AreaWeightedQuality(
                    mkpt_so_far, area_normalization, area_weight
                )
                graph.add_edge("ChooseSFRNode", mkpt_so_far, capacity=weighted_quality)
                graph.add_edge("ChooseNewNode", mkpt_so_far, capacity=-weighted_quality)
            graph.add_edge(mkpt_new, mkpt_so_far, capacity=INFINITY_NUMPY_FLOAT)

        weighted_quality = _AreaWeightedQuality(
            mkpt_new, area_normalization, area_weight
        )
        graph.add_edge("ChooseSFRNode", mkpt_new, capacity=-weighted_quality)
        graph.add_edge("ChooseNewNode", mkpt_new, capacity=weighted_quality)

    if graph.number_of_nodes() > 0:
        isolated_mkpts = set(detected_so_far + newly_detected).difference(graph.nodes())

        # Note: do not write detected_so_far = ... since it will leave the original list unchanged, assigning to
        # a new, local list. Hence the deletions below.
        _, (so_far_better, new_better) = gr_.minimum_cut(
            graph, "ChooseSFRNode", "ChooseNewNode"
        )
        bad_so_far = tuple(map(lambda mkpt: mkpt not in so_far_better, detected_so_far))
        for idx in range(bad_so_far.__len__() - 1, -1, -1):
            if bad_so_far[idx]:
                del detected_so_far[idx]
        detected_so_far.extend(mkpt for mkpt in newly_detected if mkpt in new_better)
        detected_so_far.extend(isolated_mkpts)
        # Note: below line is useful only when seeding pseudo-random number generation. Indeed, in that case,
        # the object detection is requested to be reproducible. However, either "gr_.minimum_cut" or "set" above
        # (or both) does not return sequences in deterministic order. (note that this is not useful in other parts of
        # the code where detected_so_far is updated deterministically)
        detected_so_far.sort(key=lambda mkpt: mkpt.uid)
    else:
        detected_so_far.extend(newly_detected)


def _AreaWeightedQuality(
    mkpt: marked_point_t, area_normalization: Sequence[float], area_weight: float
) -> float:
    """
    area_normalization: (scaling, min_area) where scaling should be
    1 / (max_area - min_area).
    """
    if (area_weight != 0.0) and (mkpt.area > area_normalization[0]):
        # The value to be raised to the power of area_weight must, and should always, be >= 0. However, when the mkpt
        # crosses the signal domain border, its area can be < the min area. Testing mkpt.crosses_border might be
        # enough, but because the area is a discrete version (=> rounding errors), it is safer to simply check if
        # mkpt.area >= area_normalization[0] (actually > to avoid unnecessary 0^x).
        normalized_area = area_normalization[1] * (mkpt.area - area_normalization[0])

        return mkpt.quality * pow(normalized_area, area_weight)

    return mkpt.quality


def _RefineMKPT(
    detected_mkpt: marked_point_t,
    det_idx: int,
    detected_so_far: list,
    overlap_tolerance: float,
    sampler: sampler_t,
    n_refinement_attempts: int,
    refinement_fraction: float,
    MKPTQuality_fct: mkpt_quality_fct_t,
    journal: journal_t,
) -> None:
    #
    journal.UpdateMetric("n_refinement_attempts", 1)
    similar_mkpts = detected_mkpt.SimilarMarkedPoints(
        sampler, n_refinement_attempts, fraction=refinement_fraction,
    )
    qualities_of_similars = [MKPTQuality_fct(mkpt) for mkpt in similar_mkpts]

    for qty_idx in cast(array_t, nmpy.flipud(nmpy.argsort(qualities_of_similars))):
        if qualities_of_similars[qty_idx] <= detected_mkpt.quality:
            break

        similar_mkpt = similar_mkpts[qty_idx]
        has_intersections = False
        for other_det in detected_so_far:
            if other_det is detected_mkpt:
                continue
            if similar_mkpt.Intersects(other_det, overlap_tolerance):
                has_intersections = True
                break

        if not has_intersections:
            detected_so_far[det_idx] = similar_mkpt
            journal.UpdateMetric("n_refinements", 1)
            return

    detected_mkpt.age = 0  # Reset its age so that the algorithm does not try to improve it at each next iteration
