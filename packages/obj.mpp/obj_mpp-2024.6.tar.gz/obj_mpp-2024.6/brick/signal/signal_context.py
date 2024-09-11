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

from __future__ import annotations

import brick.structure.checker as ch_
import brick.structure.explorer as ex_
import brick.interface.io.reporting as mg_
from brick.data.type import array_t, pl_path_t

from typing import Any, Callable, ClassVar, Optional, Sequence, Tuple

import numpy as nmpy


class signal_context_t:
    #
    __slots__ = ()

    _locked: ClassVar[bool] = False

    signal_base_path: ClassVar[pl_path_t] = None
    signal_path_is_folder: ClassVar[bool] = None
    signal_paths: ClassVar[Sequence] = None
    SignalLoading_fct: ClassVar[Callable] = None
    sig_lpm_prm: ClassVar[dict] = None
    mkpt_dim: ClassVar[int] = None

    signal_has_vmap: ClassVar[bool] = False  # Do not initialize with None
    vmap_base_path: ClassVar[pl_path_t] = None
    vmap_path_is_folder: ClassVar[bool] = None

    # Size of the domain the marked points will be superimposed on
    lengths: ClassVar[tuple] = None
    grid_coords: ClassVar[Tuple[array_t, ...]] = None
    raw_signal: ClassVar[Any] = None
    signal_for_qty: ClassVar[Any] = None
    signal_for_stat: ClassVar[array_t] = None
    validity_map: ClassVar[array_t] = None
    invalidity_map: ClassVar[array_t] = None  # Wherever the signal is NaN

    def __init__(self, *args, **kwargs) -> None:
        #
        raise RuntimeError(
            f"{self.__class__.__name__}{mg_.SEP}Not meant to be instantiated"
        )

    @classmethod
    def PrepareForSignalLoading(cls, signal_path: str) -> None:
        #
        signal_base_path = pl_path_t(signal_path)
        signal_path_is_folder = signal_base_path.is_dir()

        if signal_path_is_folder:
            # TODO: see if interesting to replace with rglob (will require hierarchy mirroring between signal and vmap)
            signal_paths = signal_base_path.glob("*.*")
        else:
            signal_paths = (signal_base_path,)

        cls.signal_base_path = signal_base_path
        cls.signal_path_is_folder = signal_path_is_folder
        cls.signal_paths = signal_paths

    @classmethod
    def PrepareForValidityMapLoading(cls, vmap_path: str) -> None:
        #
        if (cls.signal_base_path is None) or (cls.signal_path_is_folder is None):
            raise RuntimeError(
                f"{cls.__name__}{mg_.SEP}Preparation for signal loading "
                f"must precede preparation for validity map loading"
            )

        vmap_base_path = vmap_path
        if vmap_base_path is None:
            signal_has_vmap = False
            vmap_path_is_folder = False
        else:
            vmap_base_path = pl_path_t(vmap_base_path)
            signal_has_vmap = True
            vmap_path_is_folder = vmap_base_path.is_dir()

            if vmap_path_is_folder and not cls.signal_path_is_folder:
                raise ValueError(
                    f"Validity map{mg_.SEP}Path cannot be a folder if signal path refers to a single datum; "
                    f"Validity map path: {vmap_base_path}; "
                    f"Signal path: {cls.signal_base_path}"
                )

        cls.signal_has_vmap = signal_has_vmap
        cls.vmap_base_path = vmap_base_path
        cls.vmap_path_is_folder = vmap_path_is_folder
        # cls.validity_map = None  # Already done in class definition

    @classmethod
    def LazySequenceOfSignalDetails(cls) -> tuple:
        #
        for signal_path in cls.signal_paths:
            signal_id = f"{signal_path.stem}_{signal_path.suffix[1:]}"
            raw_signal, validity_map, error = cls._RawSignalAndValidityMap(
                signal_path
            )
            cls.SetRawSignalAndValidityMap(raw_signal, validity_map)

            yield signal_path, signal_id, raw_signal, validity_map, error

    @classmethod
    def _RawSignalAndValidityMap(
        cls, signal_path: pl_path_t,
    ) -> Tuple[Any, array_t, Optional[str]]:
        #
        # If signal_path_is_folder, raw signal need not have the same shape, unless mkt_bth_prm['center_rng'] is an array_t.
        # In this latter case, shape compatibility is checked in CreateCenterGenerator.
        # Can be used w/o prior PrepareFor... calls if no validity map is needed.
        #
        validity_map_previous = cls.validity_map

        try:
            if cls.signal_has_vmap and (
                cls.vmap_path_is_folder or (validity_map_previous is None)
            ):
                if cls.vmap_path_is_folder:
                    vmap_path = cls.vmap_base_path / signal_path.relative_to(
                        cls.signal_base_path
                    )
                else:
                    vmap_path = cls.vmap_base_path

                raw_signal, validity_map = cls.SignalLoading_fct(
                    signal_path,
                    vmap_path=vmap_path,
                    mkpt_dim=cls.mkpt_dim,
                    **cls.sig_lpm_prm,
                )
            #
            else:
                raw_signal, _ = cls.SignalLoading_fct(
                    signal_path, mkpt_dim=cls.mkpt_dim, **cls.sig_lpm_prm
                )
                validity_map = validity_map_previous
            error = None
        #
        except Exception as exception:
            raw_signal = None
            validity_map = None
            error = exception

        return raw_signal, validity_map, error

    @classmethod
    def SetSignalLoadingFunction(
        cls, SignalLoading_fct: Callable, sig_lpm_prm: dict, mkpt_dim: int,
    ) -> None:
        #
        # Do not modify sig_lpm_prm afterwards since no copy is made
        #
        ch_.CheckPassedParameters(
            SignalLoading_fct.__name__,
            ex_.FunctionInfos(SignalLoading_fct),
            sig_lpm_prm,
            3,
        )

        cls.SignalLoading_fct = SignalLoading_fct
        cls.sig_lpm_prm = sig_lpm_prm
        cls.mkpt_dim = mkpt_dim

    @classmethod
    def SetRawSignalAndValidityMap(cls, raw_signal: Any, validity_map: array_t) -> None:
        #
        # /!\ validity_map might be referenced directly: it must not be modified externally from then on
        #
        cls.raw_signal = raw_signal

        if validity_map is None:
            cls.validity_map = None
            cls.invalidity_map = None
        else:
            cls.validity_map = validity_map.astype(nmpy.bool_, copy=False)
            cls.invalidity_map = nmpy.logical_not(validity_map)

    @classmethod
    def SetSignalsForQualityAndStatistics(
        cls,
        lengths: Sequence[int],
        signal_for_qty: Any,
        signal_for_stat: Optional[array_t],
    ) -> None:
        #
        # Probably do not add signal_for_dsp here since display can be considered as a task external to Obj.MPP
        #
        if cls._locked:
            raise RuntimeError(
                f'{cls.__name__}{mg_.SEP}Class is locked; Call "Clear" to unlock'
            )
        cls._locked = True

        cls.lengths = tuple(lengths)
        cls.grid_coords = nmpy.indices(lengths)
        cls.signal_for_qty = signal_for_qty
        cls.signal_for_stat = signal_for_stat

    @classmethod
    def Clear(cls) -> None:
        #
        cls._locked = False
