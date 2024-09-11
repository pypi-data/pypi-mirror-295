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

import brick.mpp as mp_
import brick.sequential as sq_

import multiprocessing as ll_
from typing import Any, Sequence


def NChunksInFirstDimension(n_parallel_workers: int) -> int:
    #
    if (n_parallel_workers != 1) and (ll_.get_start_method(allow_none=False) == "fork"):
        if n_parallel_workers > 0:
            n_chunks = n_parallel_workers
        else:
            n_chunks = (3 * ll_.cpu_count()) // 2
    else:
        # Disables parallel computation if requested or if using Windows, since pickle cannot handle it
        n_chunks = 1

    return n_chunks


def FromTosInFirstDimension(n_chunks: int, signal_lengths: Sequence[int]) -> Sequence:
    #
    chunk_size = signal_lengths[0] // n_chunks
    remainder = signal_lengths[0] % n_chunks
    chunk_sizes = n_chunks * [chunk_size]
    for chunk_idx in range(remainder):
        chunk_sizes[chunk_idx] += 1

    from_tos = [(0, chunk_sizes[0] - 1)]
    for chunk_idx, chunk_size in enumerate(chunk_sizes[1:]):
        last_to = from_tos[chunk_idx][1]
        from_tos.append((last_to + 1, last_to + chunk_size))
    from_tos = tuple(from_tos)

    return from_tos


def ProcessesAndQueue(from_tos, detection_prms) -> tuple:
    #
    queue = ll_.Queue()
    processes = tuple(
        ll_.Process(
            target=sq_.DetectedObjectsInOneChunk,
            args=(*detection_prms, from_to, pid, queue),
        )
        for pid, from_to in enumerate(from_tos, start=1)
    )

    return processes, queue


def DetectedObjectsInAllChunks(
    processes, queue, mkpt_t, area_normalization, area_weight, overlap_tolerance
) -> list:
    #
    mkpt_lst = []

    for process in processes:
        process.start()

    # From: https://stackoverflow.com/questions/31708646/process-join-and-queue-dont-work-with-large-numbers
    # Answer by: Patrick Maupin (answered Jul 29 '15 at 19:59, edited Dec 8 '15 at 23:45)
    while True:
        running = any(process.is_alive() for process in processes)
        while not queue.empty():
            partial_lst = queue.get()
            partial_lst = list(map(lambda info: RebuiltMKPT(info, mkpt_t), partial_lst))
            mp_.UpdateDetectedSoFar(
                mkpt_lst,
                partial_lst,
                area_normalization,
                area_weight,
                overlap_tolerance,
            )
        if not running:
            break
    # Alternative (by same author):
    # liveprocs = list(processes)
    # while liveprocs:
    #     try:
    #         while 1:
    #             process_queue_data(q.get(False))
    #     except Queue.Empty:
    #         pass
    #
    #     time.sleep(0.5)    # Give tasks a chance to put more data in
    #     if not q.empty():
    #         continue
    #     liveprocs = [p for p in liveprocs if p.is_alive()]

    for process in processes:
        process.join()

    return mkpt_lst


def RebuiltMKPT(info: tuple, mkpt_t) -> Any:
    #
    mkpt = mkpt_t(*info[:-2], check_marks=False)
    mkpt.quality = info[-2]
    mkpt.age = info[-1]

    return mkpt
