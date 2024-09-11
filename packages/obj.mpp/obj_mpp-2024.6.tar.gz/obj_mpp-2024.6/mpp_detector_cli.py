#!/usr/bin/env python3

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

import glob as gb_
import sys as sy_
from typing import Callable, Dict, Optional, Sequence, Tuple

import numpy as nmpy

import brick.interface.io.config as iocf
import brick.interface.io.mkpt_list as ioml
import brick.interface.io.reporting as mg_
import brick.interface.io.storage as st_
import brick.interface.ko.console as cl_
import brick.parallel as ll_
import brick.sequential as sq_
import brick.signal.signal_loading as sl_
import brick.structure.checker as ch_
import brick.structure.explorer as ex_
import brick.structure.importer as im_
from brick.signal.constant import INFINITY_NUMPY_FLOAT
from brick.config.config import (
    config_t,
    light_config_h,
    raw_config_h,
)
from brick.data.config.std_labels import std_label_e
from brick.data.type import pl_path_t
from brick.interface.ko.config import CommandLineParser
from brick.marked_point.generic import marked_point_t
from brick.marked_point.sampler import sampler_t
from brick.quality.generic import quality_env_t
from brick.signal.signal_context import signal_context_t


def RunDetector(
    config: raw_config_h, for_deferred_check: light_config_h
) -> Dict[str, Tuple[marked_point_t, ...]]:
    #
    start_as_str = cl_.FormattedDateTime()

    # --- CONFIGURATION -> PARAMETERS
    #
    alg_mpp_prm = config[std_label_e.sct_mpp]
    alg_ref_prm = config[std_label_e.sct_refinement]
    alg_fbk_prm = config[std_label_e.sct_feedback]

    mkt_bth_prm = config[std_label_e.sct_object]  # bth=birth
    mkt_rng_prm = config[std_label_e.sct_object_ranges]
    mkt_qty_prm = config[std_label_e.sct_quality]
    mkt_qpm_prm = config[std_label_e.sct_quality_prm]  # qpm=quality parameters
    mkt_ict_prm = config[std_label_e.sct_incitations]
    mkt_cst_prm = config[std_label_e.sct_constraints]

    sig_ldg_prm = config[std_label_e.sct_signal]  # ldg=loading
    sig_lpm_prm = config[std_label_e.sct_signal_loading_prm]  # lpm=loading parameters
    sig_prg_prm = config[std_label_e.sct_signal_processing_prm]

    out_res_prm = config[std_label_e.sct_output]  # res=result
    out_dsp_prm = config[std_label_e.sct_output_prm]  # dsp=display

    # --- OBJECT CLASS and QUALITY LOADING
    #
    mkpt_t = _MKPTClass(mkt_bth_prm, mkt_rng_prm, alg_ref_prm, for_deferred_check)
    mkpt_quality_env = _MKPTQuality(
        mkt_qty_prm, mkt_qpm_prm, sig_prg_prm, for_deferred_check
    )
    mkpt_dim = mkpt_t.dim

    # --- RAW DATA READING PREPARATION
    #
    SignalLoading_fct = _SignalLoadingFunction(sig_ldg_prm, for_deferred_check)
    signal_context_t.SetSignalLoadingFunction(SignalLoading_fct, sig_lpm_prm, mkpt_dim)
    signal_context_t.PrepareForSignalLoading(sig_ldg_prm["signal_path"])
    signal_context_t.PrepareForValidityMapLoading(sig_ldg_prm["vmap_path"])

    if isinstance(mkt_bth_prm["center_rng"], pl_path_t):
        mkt_bth_prm["center_rng"] = sl_.MKPTCenterMapOrPDF(
            mkt_bth_prm["center_rng"], SignalLoading_fct, mkpt_dim
        )
    else:
        _CheckCenterRange(mkt_bth_prm["center_rng"], mkpt_dim)

    mkpt_prms = (
        mkt_bth_prm,
        mkt_ict_prm,
        mkt_cst_prm,
        mkt_qty_prm,
    )

    # --- RESULT OUTPUT PREPARATION
    #
    SignalOutput_fct, output_folder = _ResultOutputTools(
        out_res_prm, out_dsp_prm, for_deferred_check
    )

    # --- DETECTION PROCEDURE
    #
    # TODO: anything to check with std_label_e.sct_range_units instead of simply deleting it?
    if std_label_e.sct_range_units in for_deferred_check:
        del for_deferred_check[std_label_e.sct_range_units]
    if for_deferred_check.__len__() > 0:
        # TODO: better message: circumstances under which this checklist is not empty?
        raise RuntimeError(
            f"{for_deferred_check}{mg_.SEP}Section checklist should be empty"
        )

    marked_points = {}

    for signal_idx, signal_details in enumerate(
        signal_context_t.LazySequenceOfSignalDetails(), start=1
    ):
        signal_path, signal_id, raw_signal, validity_map, error = signal_details

        mg_.ReportI(f"Signal.{signal_idx}: {signal_path}")
        if raw_signal is None:
            mg_.ReportE(
                "Signal and/or signal validity map",
                f"Unable to load with error:\n{error}\nIgnoring\n",
            )
            continue

        # --- --- DATA PREPARATION
        #
        signals = mkpt_quality_env.SignalsFromRawSignal(
            raw_signal, mkpt_dim, vmap=validity_map, **sig_prg_prm
        )
        sampling_dom_lengths = signals.dom_lengths
        signal_for_qty = signals.signal_for_qty
        signal_for_stat = signals.signal_for_stat
        signal_for_dsp = signals.signal_for_dsp
        signal_context_t.SetSignalsForQualityAndStatistics(
            sampling_dom_lengths,
            signal_for_qty,
            signal_for_stat,
        )
        # Now that signal_context_t is valid, a sampler can be created (see sampler_t documentation)

        sampler = sampler_t.FromSeed(seed=alg_mpp_prm["seed"])
        sampler.SetMarkParameters(mkt_rng_prm, mkpt_t.marks_details)

        MKPTQuality_fct = lambda mkpt_: mkpt_quality_env.MKPTQuality(
            mkpt_, **mkt_qpm_prm
        )

        # --- --- HISTORY
        #
        previous_mkpt_lst = _PreviousDetection(
            alg_mpp_prm, output_folder, signal_id, MKPTQuality_fct
        )

        # --- --- MPP-BASED OBJECT DETECTION
        #
        n_chunks = ll_.NChunksInFirstDimension(alg_mpp_prm["n_parallel_workers"])
        higher_from_tos = sq_.FromTosInHigherDimensions(mkpt_dim, sampling_dom_lengths)

        alg_mpp_prm["n_births_per_iteration"] //= n_chunks
        detection_prms = (
            *mkpt_prms,
            alg_mpp_prm,
            alg_ref_prm,
            alg_fbk_prm,
            previous_mkpt_lst,
            mkpt_t,
            sampler,
            MKPTQuality_fct,
            higher_from_tos,
        )

        if n_chunks > 1:
            from_tos = ll_.FromTosInFirstDimension(n_chunks, sampling_dom_lengths)
            processes, queue = ll_.ProcessesAndQueue(from_tos, detection_prms)

            mg_.ReportI(
                f"Processe(s): {processes.__len__()} with chunks {from_tos}",
            )

            if mkt_ict_prm["area_weight"] > 0.0:
                area_normalization = mkpt_t.AreaNormalization(sampler)
            else:
                area_normalization = None
            mkpt_lst = ll_.DetectedObjectsInAllChunks(
                processes,
                queue,
                mkpt_t,
                area_normalization,
                mkt_ict_prm["area_weight"],
                mkt_cst_prm["overlap_tolerance"],
            )
        else:
            mkpt_lst = sq_.DetectedObjectsInOneChunk(
                *detection_prms, (0, sampling_dom_lengths[0] - 1)
            )
        mkpt_lst.sort(key=lambda mkpt_: mkpt_.quality, reverse=True)

        signal_context_t.Clear()

        # --- --- DETECTION OUTPUT
        #
        if mkpt_lst.__len__() > 0:
            marked_points[signal_path.__str__()] = tuple(mkpt_lst)
        else:
            mg_.ReportI("No MKPTs detected")
            continue

        if out_res_prm["console"]:
            ioml.ReportDetectionResult(mkpt_lst, start_as_str)

        if output_folder is not None:
            output_folder = st_.CreateOutputFolder(output_folder)
            iocf.WriteConfigToINIDocument(
                config,
                st_.OutputDocName(
                    output_folder, "config", "ini", start_as_str, signal_id
                ),
            )
        # The following tests should all fail if output_folder is None. This is verified in _ResultOutputTools.
        # If new tests are added here, update _ResultOutputTools accordingly.
        if out_res_prm["marks_output"]:
            st_.SaveDetectionInCSVFormat(
                mkpt_lst,
                signal_id,
                start_as_str,
                output_folder,
                sep=out_res_prm["marks_separator"],
            )
        if out_res_prm["mkpt_output"]:
            st_.SaveDetectionInFormatForRebuilding(
                mkpt_lst, signal_id, start_as_str, output_folder
            )
        if out_res_prm["contour_output"]:
            st_.SaveDetectionAsContourImage(
                mkpt_dim,
                mkpt_lst,
                signal_id,
                start_as_str,
                output_folder,
            )
        if out_res_prm["region_output"]:
            st_.SaveDetectionAsRegionImage(
                mkpt_dim,
                mkpt_lst,
                signal_id,
                start_as_str,
                output_folder,
            )
        if out_res_prm["region_numpy_output"]:
            st_.SaveDetectionAsRegionNumpyArray(
                mkpt_dim,
                mkpt_lst,
                signal_id,
                start_as_str,
                output_folder,
            )

        # Leave here so that in case it contains blocking instructions (like matplotlib show()),
        # it does not delay saving to files above.
        if isinstance(SignalOutput_fct, Callable):
            if signal_for_dsp is None:
                signal_for_dsp = nmpy.zeros(sampling_dom_lengths)
            SignalOutput_fct(
                mkpt_lst,
                mkt_bth_prm["center_rng"],
                signal_for_dsp,
                result_folder=output_folder,
                signal_id=signal_id,
                date_as_str=start_as_str,
                **out_dsp_prm,
            )

    return marked_points


def _MKPTClass(
    mkt_bth_prm, mkt_rng_prm, alg_ref_prm, for_deferred_check_io
) -> marked_point_t:
    """
    Here, the equivalent of ch_.CheckPassedParameters is marked_point.generic.CheckMarkRanges
    """
    mkpt_t = im_.ElementInModule(
        mkt_bth_prm["object_type"],
        mod_name=mkt_bth_prm["object_module"],
        category="marked_point",
    )
    mkpt_t.NormalizeMarkRanges(mkt_rng_prm)
    if std_label_e.sct_object_ranges in for_deferred_check_io:
        del for_deferred_check_io[std_label_e.sct_object_ranges]

    simlar_mkpt_mtd = mkpt_t.SimilarMarkedPoints.__name__
    if (alg_ref_prm["age_for_refinement"] is not None) and (
        not hasattr(mkpt_t, simlar_mkpt_mtd)
    ):
        raise ValueError(
            f"{mkpt_t}{mg_.SEP}MPP refinement cannot be used: "
            f'Missing "{simlar_mkpt_mtd}" method'
        )

    return mkpt_t


def _MKPTQuality(
    mkt_qty_prm, mkt_qpm_prm, sig_prg_prm, for_deferred_check_io
) -> quality_env_t:
    #
    mkpt_quality_env = im_.ElementInModule(
        mkt_qty_prm["object_quality"],
        mod_name=mkt_qty_prm["object_quality_module"],
        category="quality",
    )
    mkpt_quality_env.CheckEnvironment(sig_prg_prm, mkt_qpm_prm)

    # TODO: make the relation between std_label_e.sct_signal_processing_prm and sig_prg_prm clear
    # TODO: same thing anytime for_deferred_check or for_deferred_check_io appears
    if std_label_e.sct_signal_processing_prm in for_deferred_check_io:
        del for_deferred_check_io[std_label_e.sct_signal_processing_prm]
    if std_label_e.sct_quality_prm in for_deferred_check_io:
        del for_deferred_check_io[std_label_e.sct_quality_prm]

    return mkpt_quality_env


def _SignalLoadingFunction(sig_ldg_prm, for_deferred_check_io) -> Callable:
    #
    SignalLoading_fct = im_.ElementInModule(
        sig_ldg_prm["signal_loading_function"],
        mod_name=sig_ldg_prm["signal_loading_module"],
        elm_is_class=False,
    )

    if std_label_e.sct_signal_loading_prm in for_deferred_check_io:
        del for_deferred_check_io[std_label_e.sct_signal_loading_prm]

    return SignalLoading_fct


def _ResultOutputTools(
    out_res_prm, out_dsp_prm, for_deferred_check_io
) -> Tuple[Optional[Callable], pl_path_t]:
    #
    if (out_res_prm["output_path"] is None) and (
        out_res_prm["marks_output"]
        or out_res_prm["mkpt_output"]
        or out_res_prm["contour_output"]
        or out_res_prm["region_output"]
        or out_res_prm["region_numpy_output"]
    ):
        raise ValueError(
            f"Configuration{mg_.SEP}"
            f"Some form of result storage requested w/o output folder specification"
        )

    if out_res_prm["result_output_function"] is None:
        SignalOutput_fct = None
    else:
        SignalOutput_fct = im_.ElementInModule(
            out_res_prm["result_output_function"],
            mod_name=out_res_prm["result_output_module"],
            elm_is_class=False,
        )
        ch_.CheckPassedParameters(
            SignalOutput_fct.__name__,
            ex_.FunctionInfos(SignalOutput_fct),
            out_dsp_prm,
            3,
        )

    if std_label_e.sct_output_prm in for_deferred_check_io:
        del for_deferred_check_io[std_label_e.sct_output_prm]

    return SignalOutput_fct, out_res_prm["output_path"]


def _CheckCenterRange(center_rng, mkpt_dim: int) -> None:
    #
    if isinstance(center_rng, tuple):
        center_rng_len = center_rng.__len__()
        if center_rng_len // 2 != mkpt_dim:
            raise ValueError(
                f"center_rng{mg_.SEP}"
                f"Must have length {2*mkpt_dim} or {2*mkpt_dim+1}; "
                f"Actual={center_rng_len}"
            )


def _PreviousDetection(
    alg_mpp_prm: dict,
    output_folder: pl_path_t,
    signal_id: str,
    MKPTQuality_fct: Callable,
) -> Sequence[marked_point_t]:
    #
    output = None

    if alg_mpp_prm["use_history"]:
        path = st_.OutputDocName(output_folder, "mkpt", "json", "*", signal_id)
        history_documents = sorted(gb_.glob(path.__str__()))
        if history_documents.__len__() > 0:
            output = []
            history_document = history_documents[-1]

            with open(history_document) as json_accessor:
                for json in json_accessor.readlines():
                    mkpt = marked_point_t.FromJSON(json)
                    if alg_mpp_prm["fixed_history"]:
                        mkpt.quality = INFINITY_NUMPY_FLOAT
                    else:
                        _ = MKPTQuality_fct(mkpt)
                    output.append(mkpt)

            if output.__len__() == 0:
                output = None

            print(
                f"Using history from {history_document} "
                f"having {output.__len__()} object(s)."
            )

    return output


def Main() -> None:
    """"""
    parser = CommandLineParser()
    arguments = parser.parse_args()
    ini_document = getattr(arguments, config_t.INI_DOCUMENT_OPTION)

    config, config_is_valid, for_deferred_check = config_t.NewFromRawVersion(
        iocf.RawConfigFromINIDocument, from_file=ini_document, arguments=arguments
    )
    if (config is None) or not config_is_valid:
        sy_.exit(1)

    iocf.Print(config)
    _ = RunDetector(config.AsRawDict(), for_deferred_check)


if __name__ == "__main__":
    #
    Main()
