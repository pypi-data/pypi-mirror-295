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

import brick.interface.ko.text_color as tc_
import brick.interface.io.reporting as mg_
import brick.structure.importer as im_
from brick.signal.signal_context import signal_context_t
from brick.data.config.no_circular_import import PARAMETER_RANGE_SUFFIX
from brick.data.type import BUILTIN_TYPES, IsNumber, array_t, number_h, pl_path_t
from brick.marked_point.sampler import sampler_t

import itertools as it_
import importlib as il_
import inspect as sp_
import json as js_
import math as ma_
import string as sg_
# import sys as sy_
from abc import ABC as abc_t
from abc import abstractmethod
from collections import namedtuple as namedtuple_t
from typing import Any, ClassVar, Dict, Optional, Tuple, Union

import numpy as nmpy
import scipy.ndimage as spim
import skimage.measure as ms_


# domain: to be used in numpy array indexing
bbox_t = namedtuple_t("bbox_t", "lengths mins maxs domain")
dilated_region_t = Tuple[array_t, tuple]
dilated_regions_t = Dict[int, dilated_region_t]


_UID_ALPHABET = sg_.digits + sg_.ascii_uppercase + "$#@&+*%<=>"
_UID_ALPHABET_LENGTH = _UID_ALPHABET.__len__()


class marked_point_t(abc_t):
    """
    Note: "pass" is used in abstract methods instead of "raise NotImplementedError"

    TBO=To be OVERRIDDEN
    TBIm=To be IMPLEMENTED (mandatory)
    TBIo=To be IMPLEMENTED (optional)

    marks_details: Only for marks that are specific to the marked point (see raw_marks method)

    marks: All marks, i.e., including marks set in potential parent classes (see raw_marks method)
    quality: Cached but computed externally and accessed directly (hence, no _ prefix).
    It must be None by default (see mp_quality in brick.quality.definition)
    cropping_indicator: top, bottom, left, right, [front, back] (i.e., row, col, dep)
    """

    dim: ClassVar[int] = 0
    mark_names: ClassVar[Tuple[str, ...]] = None
    marks_details: ClassVar[Dict[str, Any]] = None
    # From ranges given in INI configuration document to ellipsoid marks for use in ellipsoid-derived classes
    marks_translations: ClassVar[Dict[str, str]] = {}

    _ball_of_radius: ClassVar[Dict[int, array_t]] = {}
    _class_cache: ClassVar[Dict[str, Any]] = {}

    __slots__ = (
        "is_valid",
        "position",
        "marks",
        "age",
        "raw_region",
        "region",
        "quality",
        "bbox",
        "cropping_indicator",
        "crosses_border",
        "_cache",
    )
    is_valid: bool
    position: Tuple[number_h, ...]
    marks: Dict[str, Any]
    age: int
    raw_region: array_t
    region: array_t
    quality: float
    bbox: bbox_t
    cropping_indicator: Tuple[bool, ...]
    crosses_border: bool
    _cache: Dict[str, Any]

    # --- INSTANTIATE

    def __init__(self, position, *marks, check_marks: bool = True) -> None:
        #
        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in marked_point_t.__slots__:
            setattr(self, slot, None)

        self.position = tuple(position)  # In case an iterator, or not a tuple
        self.marks = {}
        for name, value in zip(self.__class__.mark_names, marks):
            self.marks[name] = value
        # TODO: add a (mandatory but partial) position check:
        # isinstance(position[0], (nmpy.integer, nmpy.float))
        if check_marks:
            self.CheckMarks()

        self.age = 0
        self._cache = {}

        self._ComputeBoundingBox(*self._CoarseBoundingBoxHalfLengths())
        # TODO: rename region into valid_region, and raw_region to region (maybe)
        self.raw_region = self._RawRegion()
        if signal_context_t.invalidity_map is None:
            self.region = self.raw_region
        else:
            self.region = self.raw_region.copy()
            self.region[signal_context_t.invalidity_map[self.bbox.domain]] = False
        self.is_valid = self.region.any()

    @classmethod
    def FromJSON(cls, json: str) -> marked_point_t:
        #
        json_decoder = js_.JSONDecoder()
        json_as_dict = json_decoder.decode(json)

        module = im_.ModuleUsingAltImport(pl_path_t(json_as_dict["where"]))
        mkpt_class = getattr(module, json_as_dict["what"])

        position_and_marks = []
        for what, where, how in json_as_dict["how"].values():
            if where is None:
                value = how
            else:
                module = il_.import_module(where)
                type_ = getattr(module, what)
                value = type_(how)

            position_and_marks.append(value)

        position = position_and_marks[0]
        if isinstance(position[0], int):
            position = (nmpy.int64(coord) for coord in position)
        else:
            position = (nmpy.float64(coord) for coord in position)
        instance = mkpt_class(position, *position_and_marks[1:], check_marks=False)

        return instance

    def CheckMarks(self) -> None:
        #
        for name, value in self.marks.items():
            # IsNumber should work for numpy.uint8 (unlike isinstance)
            if not IsNumber(value):
                raise TypeError(
                    f'{value}{mg_.SEP}Invalid type for mark "{name}"; '
                    f"Type={type(value)}; Expected=int or float"
                )

            if name not in self.__class__.marks_details:
                continue  # marks_details lists the strict marks while marks may be filled by a parent class
                # with extra, fixed marks.

            details = self.__class__.marks_details[name]

            if details.min_inclusive and (value < details.min):
                raise ValueError(
                    f"{name}{mg_.SEP}Range start out-of-bound: "
                    f"Actual_{value} < min_{details.min}"
                )
            elif (not details.min_inclusive) and (value <= details.min):
                raise ValueError(
                    f"{name}{mg_.SEP}Range start out-of-bound: "
                    f"Actual_{value} <= strict_min_{details.min}"
                )

            if details.max_inclusive and (value > details.max):
                raise ValueError(
                    f"{name}{mg_.SEP}Range start out-of-bound: "
                    f"Actual_{value} > max_{details.max}"
                )
            elif (not details.max_inclusive) and (value >= details.max):
                raise ValueError(
                    f"{name}{mg_.SEP}Range start out-of-bound: "
                    f"Actual_{value} >= strict_max_{details.max}"
                )

    @staticmethod
    def CheckMarkRanges(
        mk_ranges: dict, marks_details: dict, marks_translations: dict
    ) -> None:
        #
        for ini_name, cls_name in marks_translations.items():
            ini_name += PARAMETER_RANGE_SUFFIX
            cls_name += PARAMETER_RANGE_SUFFIX
            if ini_name in mk_ranges:
                mk_ranges[cls_name] = mk_ranges[ini_name]
                del mk_ranges[ini_name]

        valid_names = set(marks_details.keys()).union(marks_translations.keys())
        valid_names = tuple(elm + PARAMETER_RANGE_SUFFIX for elm in valid_names)

        is_invalid = False
        for rng_name, value in mk_ranges.items():
            # name = rng_name[: -PARAMETER_RANGE_SUFFIX.__len__()]
            # if name not in marks_details:
            if rng_name not in valid_names:
                mg_.ReportIP(rng_name, "mark range", valid_names)
                is_invalid = True
                continue

            name = rng_name[: -PARAMETER_RANGE_SUFFIX.__len__()]
            if name not in marks_details:
                name = marks_translations[name]
            details = marks_details[name]

            # If type is int, following tests will just test for ints;
            # Otherwise type is float, and following tests will test for either ints or floats
            if (
                (not isinstance(value, tuple))
                or ((value.__len__() != 2) and (value.__len__() != 3))
                or (
                    not all(
                        isinstance(elm, int) or isinstance(elm, details.type)
                        for elm in value
                    )
                )
            ):
                mg_.ReportE(
                    f"{value}",
                    f'Invalid type for range "{name}"; '
                    f"Actual={type(value).__name__}; "
                    f"Expected=(int_or_float, int_or_float[, int_or_float])",
                )
                is_invalid = True
                continue

            if value[0] > value[1]:
                mg_.ReportE(name, f"Invalid range: From_{value[0]} !>! to_{value[1]}")
                is_invalid = True
                continue

            if details.type is int:
                if value[0] < details.min:
                    mg_.ReportE(
                        name,
                        f"Range start out-of-bound: "
                        f"Actual_{value[0]} < min_{details.min}",
                    )
                    is_invalid = True
                    continue
                if (value[0] == details.min) and not details.min_inclusive:
                    mg_.ReportE(
                        name,
                        f"Range start out-of-bound: "
                        f"Actual_{value[0]} <= strict_min_{details.min}",
                    )
                    is_invalid = True
                    continue

                if value[1] > details.max:
                    mg_.ReportE(
                        name,
                        f"Range end out-of-bound: "
                        f"Actual_{value[1]} > max_{details.max}",
                    )
                    is_invalid = True
                    continue
                if (value[1] == details.max) and not details.max_inclusive:
                    mg_.ReportE(
                        name,
                        f"Range end out-of-bound: "
                        f"Actual_{value[1]} >= strict_max_{details.max}",
                    )
                    is_invalid = True
                    continue
            elif details.type is float:
                if value[0] < details.min:
                    mg_.ReportE(
                        name,
                        f"Range start out-of-bound: "
                        f"Actual_{value[0]} < min_{details.min}",
                    )
                    is_invalid = True
                    continue
                if value[1] > details.max:
                    mg_.ReportE(
                        name,
                        f"Range end out-of-bound: "
                        f"Actual_{value[1]} > max_{details.max}",
                    )
                    is_invalid = True
                    continue
            else:
                mg_.ReportE(f"{details.type}", f'Invalid type for range "{name}"')
                is_invalid = True
                continue

        if is_invalid:
            raise mg_.silent_exception_t()

    @staticmethod
    def AddDefaultsToMarkRanges(mk_ranges: dict, marks_details: dict) -> None:
        #
        for mark in marks_details:
            range_name = mark + PARAMETER_RANGE_SUFFIX
            if range_name not in mk_ranges:
                default_range = marks_details[mark].default_range
                if default_range is None:
                    raise ValueError(f"{range_name}{mg_.SEP}Missing required range")
                mk_ranges[range_name] = default_range

    def _ComputeBoundingBox(self, *uncropped_half_lengths) -> None:
        #
        # Compute the rectangle just big enough to contain the marked point and set the appropriate member variables
        #
        signal_lengths = signal_context_t.lengths

        mins = []
        maxs = []
        cropping_indicator = 2 * self.dim * [False]

        ci_idx = 0
        for d_idx in range(self.dim):
            min_coord = self.position[d_idx] - uncropped_half_lengths[d_idx]
            if min_coord < 0:
                min_coord = 0
                cropping_indicator[ci_idx] = True
            else:
                min_coord = int(nmpy.floor(min_coord))

            max_coord = self.position[d_idx] + uncropped_half_lengths[d_idx]
            if max_coord > signal_lengths[d_idx] - 1:
                max_coord = signal_lengths[d_idx] - 1
                cropping_indicator[ci_idx + 1] = True
            else:
                max_coord = int(nmpy.ceil(max_coord))

            mins.append(min_coord)
            maxs.append(max_coord)
            ci_idx += 2

        self.bbox = bbox_t(
            lengths=tuple(
                max_coord - min_coord + 1 for min_coord, max_coord in zip(mins, maxs)
            ),
            mins=tuple(mins),
            maxs=tuple(maxs),
            domain=tuple(
                slice(min_coord, max_coord + 1)
                for min_coord, max_coord in zip(mins, maxs)
            ),
        )
        self.cropping_indicator = tuple(cropping_indicator)
        self.crosses_border = any(self.cropping_indicator)

    @classmethod
    @abstractmethod
    def NormalizeMarkRanges(cls, mkt_rng_prm):
        #
        pass

    # --- COMPUTE

    def Region(self, dilation: int) -> Union[array_t, dilated_region_t]:
        #
        # Returns the boolean map of the dilated MP and the slices for each bbox dimension.
        # Dilation can be negative (erosion then).
        # This version is a default implementation that requires the optional _BallOfRadius and
        # _DilatedBboxSlices methods to be implemented.
        #
        cache_entry = self.Region.__name__

        if cache_entry not in self._cache:
            self._cache[cache_entry] = {}

        if dilation not in self._cache[cache_entry]:
            struct_elm = self.__class__._BallOfRadius(nmpy.fabs(dilation))
            if dilation > 0:
                padded_region = nmpy.pad(self.raw_region, dilation, "constant")
                dilated_region = spim.binary_dilation(
                    padded_region, structure=struct_elm
                )
                sub_domain = signal_context_t.lengths.__len__() * [slice(0)]
                for axis, length in enumerate(signal_context_t.lengths):
                    start = max(dilation - self.bbox.domain[axis].start, 0)
                    stop = dilated_region.shape[axis] - max(
                        self.bbox.domain[axis].stop + dilation - length, 0
                    )
                    sub_domain[axis] = slice(start, stop)
                dilated_region = dilated_region[tuple(sub_domain)]
                dilated_domain = self._DilatedBboxSlices(dilation)
            else:
                # TODO: is it possible to use a distance map instead? Would be faster?
                dilated_region = spim.binary_erosion(
                    self.raw_region, structure=struct_elm
                )
                dilated_domain = self.bbox.domain

            if signal_context_t.invalidity_map is not None:
                dilated_region[signal_context_t.invalidity_map[dilated_domain]] = False
            self._cache[cache_entry][dilation] = (
                dilated_region,
                dilated_domain,
            )

        return self._cache[cache_entry][dilation]

    def InnerOneDistanceMap(self) -> array_t:
        #
        return spim.morphology.distance_transform_edt(self.raw_region)

    @classmethod
    def ExtremeAreas(cls, sampler: sampler_t) -> Tuple[number_h, number_h]:
        #
        if "extreme_areas" not in cls._class_cache:
            cls._class_cache["extreme_areas"] = {}

        # sampler is not hashable (/!\ unfortunately, another, later object can have the same id)
        sampler_id = id(sampler)
        if sampler_id not in cls._class_cache["extreme_areas"]:
            min_marks, max_marks = sampler.CenterPointAndExtremeMarks()
            small_mkpt = cls(*min_marks, check_marks=False)
            large_mkpt = cls(*max_marks, check_marks=False)

            cls._class_cache["extreme_areas"][sampler_id] = (
                small_mkpt.area,
                large_mkpt.area,
            )

        return cls._class_cache["extreme_areas"][sampler_id]

    @classmethod
    def AreaNormalization(cls, sampler: sampler_t) -> Tuple[float, float]:
        #
        # (min_area, 1 / (max_area - min_area))
        #
        if "area_normalization" not in cls._class_cache:
            cls._class_cache["area_normalization"] = {}

        sampler_id = sampler.uid
        if sampler_id not in cls._class_cache["area_normalization"]:
            extreme_areas = cls.ExtremeAreas(sampler)

            cls._class_cache["area_normalization"][sampler_id] = (
                extreme_areas[0],
                1.0 / (extreme_areas[1] - extreme_areas[0]),
            )

        return cls._class_cache["area_normalization"][sampler_id]

    @property
    def area(self) -> float:
        #
        # This area INcludes invalid portions of the mkpt
        #
        cache_entry = "area"

        if cache_entry not in self._cache:
            self._cache[cache_entry] = nmpy.count_nonzero(self.raw_region)

        return self._cache[cache_entry]

    def Property(self, name: str) -> Any:
        #
        rprops_entry = f"{ms_.__name__}.{ms_.regionprops.__name__}"
        cache_entry = f"{rprops_entry}.{name}"

        if cache_entry not in self._cache:
            if rprops_entry not in self._cache:
                self._cache[rprops_entry] = ms_.regionprops(
                    self.raw_region.astype(nmpy.uint8)
                )[0]

            self._cache[cache_entry] = self._cache[rprops_entry][name]

        return self._cache[cache_entry]

    @abstractmethod
    def _CoarseBoundingBoxHalfLengths(self) -> Tuple[int, ...]:
        #
        pass

    @abstractmethod
    def _RawRegion(self) -> array_t:  # TBIm
        # Must be equal to one (as opposed to zero) on the marked point frontier
        pass

    def Contour(self, thickness: int = 1) -> array_t:
        #
        raise NotImplementedError  # TBIo

    def Normals(self) -> Tuple[array_t, ...]:
        #
        raise NotImplementedError

    @staticmethod
    def _BallOfRadius(radius: int) -> array_t:
        """
        Disk structuring element used for dilation???erosion??? in which function???
        TBIo
        :param radius: Radius of the disk
        :return: Disk structuring element
        """
        raise NotImplementedError

    def _DilatedBboxSlices(self, dilation: int) -> Tuple[slice, ...]:  # TBIo
        #
        raise NotImplementedError

    def SignalStatistics(
        self, header_instead: bool = False,
    ) -> Tuple[Union[float, str], ...]:
        #
        if header_instead:
            return "Min Intensity", "Max Intensity", "Mean Intensity", "SDev Intensity"

        signal = signal_context_t.signal_for_stat

        if isinstance(signal, array_t) and (signal.ndim == self.dim):
            signal_values = signal[self.bbox.domain][self.region]

            return (
                signal_values.min().item(),
                signal_values.max().item(),
                signal_values.mean().item(),
                signal_values.std().item(),
            )
        else:
            return 4 * (nmpy.NaN,)

    # --- GENERATE

    def SimilarMarkedPoints(
        self,
        sampler: sampler_t,
        n_mkpts: int,
        fraction: float = 0.1,
    ) -> Tuple[Optional[marked_point_t], ...]:
        #
        rng_size = self._RangeSizeForSimilarPoints(fraction=fraction)
        points = sampler.SimilarPoints(self.position, n_mkpts, rng_size)
        marks = sampler.SimilarMarks(self.marks, points[0].__len__(), fraction=fraction)
        mkpt_dim = points.__len__()

        sim_mkpts = (
            self.__class__(
                pos_and_marks[:mkpt_dim], *pos_and_marks[mkpt_dim:], check_marks=False
            )
            for pos_and_marks in zip(*points, *marks)
        )

        return tuple(sim_mkpt for sim_mkpt in sim_mkpts if sim_mkpt.is_valid)

    def _RangeSizeForSimilarPoints(self, fraction: float = 0.1) -> float:  # TBIo
        #
        # Optional since refinement is optional, hence not abstract
        #
        raise NotImplementedError

    # --- ANALYZE

    @abstractmethod
    def Intersects(
        self, mkpt: marked_point_t, overlap_tolerance: float  # TBIm
    ) -> bool:
        #
        pass

    @staticmethod
    def _FinallyIntersects(
        region_1,
        domain_1,
        area_1,
        region_2,
        domain_2,
        area_2,
        overlap_tolerance: float,
    ) -> bool:
        #
        region_1_inter = region_1[domain_1]
        region_2_inter = region_2[domain_2]
        intersection_area = nmpy.count_nonzero(
            nmpy.logical_and(region_1_inter, region_2_inter)
        )

        if intersection_area == 0:
            return False

        min_area = min(area_1, area_2)
        if intersection_area == min_area:
            # Total inclusion
            return True

        # Always true when overlap_tolerance = 0
        return 100.0 * intersection_area / min_area > overlap_tolerance

    # --- REPORT

    def __repr__(self) -> str:
        #
        return f"{self.__class__.__name__}({self.uid})"

    def __str__(self) -> str:
        #
        output = []

        for name, value in zip(
            self.__class__.TupledDescriptionHeader(), self.TupledDescription()
        ):
            output.append(f"{name}: {value}")

        return ", ".join(output)

    @property
    def educated_name(self) -> str:
        # Could be a class method, but property "prefers" methods
        return self.__class__.__name__.capitalize()[:-2]

    @property
    def raw_marks(self) -> tuple:
        #
        # Marks that are specific to the marked point, independently of its implementation which might add fixed marks
        # from parent classes to its marks member variable. Ex. a disk has only its radius as a mark, but it might be
        # implemented as special case of a superquadric.
        #
        output = (self.marks[name] for name in self.__class__.marks_details.keys())

        return tuple(output)

    @property
    def educated_marks(self) -> tuple:
        raise NotImplementedError  # TBIo

    @property
    def uid(self) -> str:
        """
        An easy solution would be to use id(self). However, the only serious use of this uid is in sorting mkpts
        to guarantee reproducibility of the detection (for debugging for example). Hence, the uid cannot depend on
        runtime-dependent quantities.
        A float representation can be (costly) computed as: hex(nmpy.float64(real).view(nmpy.uint64).item())
        :return: Unique marked point instance identifier
        """
        cache_entry = "uid"

        if cache_entry not in self._cache:
            # output = []
            #
            # # Note: integer and real hex representations can include a leading minus sign. Do not blindly remove the
            # # first 2 characters with the intent to strip the "0x" out.
            # for coord in self.position:
            #     if isinstance(coord, (int, nmpy.integer)):
            #         output.append(hex(coord)[2:])
            #     else:
            #         # If not an int, then a float (or a numpy float)
            #         if isinstance(coord, nmpy.floating):
            #             coord = float(coord)
            #         output.append(coord.hex()[2:])
            #
            # for mark in self.marks.values():
            #     if isinstance(mark, (int, nmpy.integer)):
            #         output.append(hex(mark))
            #     elif isinstance(mark, (float, nmpy.floating)):
            #         if isinstance(mark, nmpy.floating):
            #             mark = float(mark)
            #         output.append(mark.hex())
            #     elif isinstance(mark, str):
            #         output.append(mark)
            #     else:
            #         output.append(mark.__str__())
            #
            # self._cache[cache_entry] = "".join(output)
            self._cache[cache_entry] = (*self.position, *self.marks.values())
            # TODO: check which option is the fastest (uid computation + sorting using uid)

        return self._cache[cache_entry]

    @property
    def runtime_uid(self):
        #
        output = []

        py_uid = id(self)
        while py_uid > 0:
            py_uid, remainder = divmod(py_uid, _UID_ALPHABET_LENGTH)
            output.insert(0, _UID_ALPHABET[remainder])

        if output.__len__() > 0:
            return "".join(output)
        else:
            # This will never happen with id(self); Only for correctness.
            return "0"

    @staticmethod
    def CoordsHeader() -> Tuple[str, ...]:
        raise NotImplementedError  # TBIo

    @classmethod
    def RawMarksHeaders(cls) -> Tuple[str, ...]:
        #
        # Marks that are specific to the marked point, independently of its implementation which might add fixed marks
        # from parent classes to its marks member variable. Ex. a disk has only its radius as a mark, but it might be
        # implemented as special case of a superquadric.
        #
        output = []

        for impl_name in cls.marks_details.keys():
            mark_name = impl_name
            for ini_name, class_name in cls.marks_translations.items():
                if mark_name == class_name:
                    mark_name = ini_name
                    break

            output.append(mark_name.capitalize())

        return tuple(output)

    @staticmethod
    def EducatedMarksHeaders() -> Tuple[str, ...]:
        raise NotImplementedError  # TBIo

    @classmethod
    def TupledDescriptionHeader(
        cls, w_prologue: bool = False, educated_version: bool = False
    ) -> Tuple[str, ...]:
        #
        if w_prologue:
            prologue = ("Type", "UID", "Runtime UID")
        else:
            prologue = ()

        if educated_version:
            middle_description = (
                *cls.EducatedMarksHeaders(),
                "Area",
            )
        else:
            middle_description = cls.RawMarksHeaders()

        return (
            *prologue,
            *cls.CoordsHeader(),
            *middle_description,
            "Quality",
            "Age",
        )

    def TupledDescription(
        self, locrup: int = 0, w_prologue: bool = False, educated_version: bool = False
    ) -> tuple:
        """
        locrup=length of common runtime uid prefix
        """
        cache_entry = self.TupledDescription.__name__

        if cache_entry not in self._cache:
            if w_prologue:
                output = [
                    self.educated_name,
                    self.uid,
                    self.runtime_uid[locrup:],
                ]
            else:
                output = []

            if educated_version:
                middle_description = (*self.educated_marks, self.area)
            else:
                middle_description = self.raw_marks
            output.extend([*self.position, *middle_description])

            if self.quality is None:
                output.append(nmpy.nan)
            else:
                output.append(self.quality)

            self._cache[cache_entry] = tuple(output)

        # Age might change between 2 calls
        return self._cache[cache_entry] + (self.age,)

    @classmethod
    def ININameOf(cls, class_name: str) -> str:
        """"""
        for ini_name, cls_name in cls.marks_translations.items():
            if cls_name == class_name:
                return ini_name

        return class_name

    @classmethod
    def ClassNameOf(cls, ini_name: str) -> Optional[str]:
        """"""
        return cls.marks_translations.get(ini_name, ini_name)

    def AsJSONableDict(self) -> dict:
        #
        cache_entry = self.AsJSONableDict.__name__

        if cache_entry not in self._cache:
            cached_class = self.__class__
            output = {
                "what": cached_class.__name__,
                "where": sp_.getfile(cached_class),
                "how": {},
            }
            output_how = output["how"]

            translations = cached_class.marks_translations
            if translations.__len__() == 0:
                translations = None

            # self.position is composed of nmpy.int64 or nmpy.float64 (which cannot be JSONed)
            position = tuple(coord.item() for coord in self.position)

            for name in it_.chain(("position",), cached_class.marks_details.keys()):
                if name == "position":
                    value = position
                else:
                    value = self.marks[name]

                type_ = type(value)
                if type_ in BUILTIN_TYPES:
                    # TODO: will not work if the type is a builtin container of non-JSONable objects
                    module_path = None
                else:
                    try:
                        v_as_int = int(value)
                        value = v_as_int
                    except ValueError:
                        try:
                            v_as_float = float(value)
                            value = v_as_float
                        except ValueError:
                            # TODO: will not work if the type cannot create an object from its string representation
                            value = str(value)
                    # getfile is not adapted to modules with relative imports (e.g., numpy)
                    module_path = sp_.getmodule(type_).__name__
                mark_type_and_value = (type_.__name__, module_path, value)

                if (name == "position") or (translations is None):
                    output_how[name] = mark_type_and_value
                else:
                    for true_name, impl_name in translations.items():
                        if name == impl_name:
                            output_how[true_name] = mark_type_and_value
                            break

            self._cache[cache_entry] = output

        return self._cache[cache_entry]

    def AsColoredStr(self, locrup: int = 0) -> str:
        #
        raise NotImplementedError  # TBIo

    def FormattedPosition(self) -> str:
        #
        coord_len = tuple(
            (size - 1).__str__().__len__() + 3 for size in signal_context_t.lengths
        )
        coords = ",".join(
            f"{self.position[idx]:{coord_len[idx]}.2f}"
            for idx in range(self.position.__len__())
        )

        return tc_.ColoredText("(" + coords + ")", "cyan") + "_"

    def FormattedAngle(self, mark_name: str) -> str:
        #
        return "/_" + tc_.ColoredText(
            f"{self.marks[mark_name] * 180.0 / ma_.pi:5.1f}", "blue"
        )

    def FormattedExponent(self, mark_name: str) -> str:
        #
        return "^" + tc_.ColoredText(f"{self.marks[mark_name]:.2f}", "magenta")

    def FormattedQuality(self) -> str:
        #
        if self.quality is None:
            quality_as_str = "?"
        else:
            quality_as_str = f"{self.quality:.3f}"

        return "=" + tc_.ColoredText(quality_as_str, "green")

    def FormattedAge(self) -> str:
        return "@" + tc_.ColoredText(self.age.__str__(), "magenta")

    def DrawInArray(
        self,
        array: array_t,
        level: number_h = 255,
        thickness: int = 2,
        bbox_level: number_h = -1,
    ) -> None:
        #
        bbox = self.bbox

        if bbox_level >= 0:
            slices = list(bbox.domain)
            for d_idx in range(self.dim):
                domain_for_dim = slices[d_idx]

                slices[d_idx] = bbox.mins[d_idx]
                array[tuple(slices)] = bbox_level

                slices[d_idx] = bbox.maxs[d_idx]
                array[tuple(slices)] = bbox_level

                slices[d_idx] = domain_for_dim

        if thickness > 0:
            array[bbox.domain][self.Contour(thickness=thickness)] = level
        else:
            array[bbox.domain][self.region] = level
