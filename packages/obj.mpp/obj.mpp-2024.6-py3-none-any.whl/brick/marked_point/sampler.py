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

import brick.interface.io.reporting as mg_
from brick.signal.signal_context import signal_context_t
from brick.data.marked_point.type import point_rng_h  # mark_h
from brick.data.type import array_t, number_h

import time as tm_
from abc import ABC as abc_t
from collections import namedtuple as namedtuple_t
from typing import Any, Callable, ClassVar, List, Optional, Sequence, Tuple, Type, Union
from warnings import warn as WarnAbout

import numpy as nmpy


domain_ranges_t = namedtuple_t("domain_ranges_t", "mins maxs")


marked_point_h = Any  # Must have a crosses_border property and an Intersect method
marked_point_class_h = Any


numpy_sampler_t = nmpy.random.Generator


class number_sampler_t:
    #
    singleton: ClassVar[Optional[numpy_sampler_t]] = None

    @classmethod
    def Initialize(cls, seed: Optional[int] = None) -> None:
        #
        if cls.singleton is None:
            if seed is None:
                cls.singleton = nmpy.random.default_rng()
            else:
                cls.singleton = nmpy.random.default_rng(seed=seed)
        else:
            WarnAbout("Number sampler already initialized", category=RuntimeWarning)

    @classmethod
    def RandomIntegers(
        cls, n_integers: int, int_range: Sequence[int, int]
    ) -> Optional[array_t]:
        #
        if int_range[0] == int_range[1]:
            samples = nmpy.full(n_integers, int_range[0], dtype=nmpy.int64, order="C")
        else:
            samples = cls.singleton.integers(
                int_range[0], high=int_range[1] + 1, size=n_integers
            )

        return samples

    @classmethod
    def RandomReals(
        cls, n_reals: int, real_range: Tuple[float, float], precision: float
    ) -> Optional[array_t]:
        #
        if real_range[0] == real_range[1]:
            samples = nmpy.full(n_reals, real_range[0], dtype=nmpy.float64, order="C")
        else:
            samples = cls.singleton.uniform(
                low=real_range[0], high=real_range[1], size=n_reals
            )  # No dtype prm!
            if precision > 0.0:
                samples = precision * nmpy.around((1.0 / precision) * samples)

        return samples


class point_sampler_t:
    #
    __slots__ = (
        # --- About the whole signal
        "signal_dim",
        "signal_lengths",
        "signal_domain_center",
        # --- About the signal subdomain to be sampled
        "precision",  # Only for size or domain
        "domain_slices",  # Only for size or domain
        "pdf_grid_coords",  # Only for pdf
        "cdf",  # Only for pdf
        "NewAny",
        "Validities",
    )
    signal_dim: int
    signal_lengths: Tuple[int, ...]
    signal_domain_center: Tuple[float, ...]
    precision: float
    domain_slices: Tuple[slice, ...]
    pdf_grid_coords: Tuple[array_t, ...]
    cdf: array_t
    NewAny: Callable[[int], Tuple[array_t, ...]]
    Validities: Callable[[array_t], array_t]

    def __init__(self, signal_lengths: Sequence[int]) -> None:
        #
        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in point_sampler_t.__slots__:
            setattr(self, slot, None)

        self.signal_dim = signal_lengths.__len__()
        self.signal_lengths = tuple(signal_lengths)  # Ensure a copy is made
        self.signal_domain_center = tuple(0.5 * extent for extent in signal_lengths)

    def PrepareForDomain(self, domain_and_precision: Sequence[number_h]) -> None:
        #
        twice_dim = 2 * self.signal_dim
        domain = domain_and_precision[:twice_dim]

        self.precision = (
            domain_and_precision[twice_dim]
            if domain_and_precision.__len__() > twice_dim
            else 0.0
        )
        self.domain_slices = tuple(
            slice(domain[idx], domain[idx + 1] + 1) for idx in range(0, twice_dim, 2)
        )

        number_sampler = number_sampler_t.singleton
        domain_ranges = domain_ranges_t(mins=domain[0::2], maxs=domain[1::2])
        if self.precision == 1.0:
            self.NewAny = lambda n_points: tuple(
                number_sampler.integers(
                    domain_ranges.mins[d_idx],
                    high=domain_ranges.maxs[d_idx] + 1,
                    size=n_points,
                )
                for d_idx in range(self.signal_dim)
            )
        elif self.precision > 0.0:
            max_per_dim = tuple(
                int(
                    (domain_ranges.maxs[d_idx] - domain_ranges.mins[d_idx])
                    / self.precision
                )
                for d_idx in range(self.signal_dim)
            )

            self.NewAny = lambda n_points: tuple(
                self.precision
                * number_sampler.integers(0, high=max_per_dim[d_idx] + 1, size=n_points)
                + domain_ranges.mins[d_idx]
                for d_idx in range(self.signal_dim)
            )
        else:
            self.NewAny = lambda n_points: tuple(
                number_sampler.uniform(
                    low=domain_ranges.mins[d_idx],
                    high=domain_ranges.maxs[d_idx],
                    size=n_points,
                )
                for d_idx in range(self.signal_dim)
            )

        # Sample coordinates can have non-integer values
        self.Validities = lambda samples: self._ValiditiesForSizeOrDomain(
            samples, domain_ranges
        )

    def PrepareForMap(
        self, pmap: array_t, true_value: number_h  # pmap=map for generating points
    ) -> None:
        #
        map_shape = pmap.shape
        valid_indices = nmpy.flatnonzero(pmap == true_value)
        n_valid_indices = valid_indices.__len__()

        number_sampler = number_sampler_t.singleton
        self.NewAny = lambda n_points: nmpy.unravel_index(
            valid_indices[number_sampler.integers(n_valid_indices, size=n_points)],
            map_shape,
        )
        self.Validities = lambda samples: self.__class__._ValiditiesForMap(
            samples, map_shape, valid_indices
        )

    def PrepareForPDF(self, pdf: array_t) -> None:
        #
        self.cdf = pdf.cumsum()
        self.cdf /= self.cdf[-1]

        self.pdf_grid_coords = tuple(
            coords.flatten() for coords in signal_context_t.grid_coords
        )

        self.NewAny = self._NewPointsFromPDF
        self.Validities = lambda samples: nmpy.array(
            samples[0].__len__() * [True], dtype=nmpy.bool_, order="C"
        )

    def _ValiditiesForSizeOrDomain(
        self, samples: Sequence[array_t], domain_ranges: domain_ranges_t
    ) -> array_t:
        #
        # Must accept sample coordinates with non-integer values
        #
        validities = nmpy.logical_and(
            samples[0] >= domain_ranges.mins[0], samples[0] <= domain_ranges.maxs[0]
        )
        for d_idx in range(1, self.signal_dim):
            local_validities = nmpy.logical_and(
                samples[d_idx] >= domain_ranges.mins[d_idx],
                samples[d_idx] <= domain_ranges.maxs[d_idx],
            )
            validities = nmpy.logical_and(validities, local_validities)

        return validities

    @staticmethod
    def _ValiditiesForMap(
        samples: Sequence[array_t], map_shape: Tuple[int, ...], valid_indices: array_t
    ) -> array_t:
        #
        if nmpy.issubdtype(samples[0].dtype, nmpy.floating):
            samples = tuple(nmpy.around(elm).astype(nmpy.int64) for elm in samples)

        return nmpy.fromiter(
            map(
                lambda idx: idx in valid_indices,
                nmpy.ravel_multi_index(samples, map_shape),
            ),
            dtype=nmpy.bool_,
            count=samples[0].__len__(),
        )

    def _NewPointsFromPDF(self, n_samples: int) -> Tuple[array_t, ...]:
        #
        uniform_samples = number_sampler_t.singleton.uniform(size=n_samples)
        indices = nmpy.searchsorted(self.cdf, uniform_samples)

        return tuple(coords[indices] for coords in self.pdf_grid_coords)

    def NewSimilar(
        self, ref_point: Sequence, n_points: int, rng_size: float
    ) -> Tuple[array_t, ...]:
        """
        """
        points = []

        if self.precision is None:
            rand_fct = number_sampler_t.RandomIntegers
            rand_prms = [n_points, None]  # Needs to be mutable
        else:
            rand_fct = number_sampler_t.RandomReals
            rand_prms = [n_points, None, self.precision]  # Needs to be mutable

        for idx in range(ref_point.__len__()):
            coord_rng = tuple(ref_point[idx] + sign * rng_size for sign in (-1.0, 1.0))
            if self.precision is None:
                coord_rng = nmpy.around(coord_rng).astype(nmpy.int64)
            if self.domain_slices is None:
                coord_rng = (
                    max(coord_rng[0], 0),
                    min(coord_rng[1], self.signal_lengths[idx] - 1),
                )
            else:
                coord_rng = (
                    max(coord_rng[0], self.domain_slices[idx].start),
                    min(coord_rng[1], self.domain_slices[idx].stop - 1),
                )

            rand_prms[1] = coord_rng
            points.append(rand_fct(*rand_prms))

        point_validities = self.Validities(points)

        return tuple(components[point_validities] for components in points)


mark_sampler_t = namedtuple_t("mark_sampler_t", "range NewAny NewSimilar")  # caster")


class sampler_t(dict, abc_t):
    """
    A valid signal_context_t is required starting from the call to FromSeed.
    """

    __slots__ = (
        "uid",
        "_mark_names",
        "SimilarPoints",
    )

    def __init__(self):
        #
        super().__init__({})
        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in sampler_t.__slots__:
            setattr(self, slot, None)
        self.uid = tm_.monotonic_ns()

    @classmethod
    def FromSeed(cls, seed: Optional[int] = None) -> sampler_t:
        #
        instance = cls()

        number_sampler_t.Initialize(seed=seed)

        instance["point"] = point_sampler_t(signal_context_t.lengths)
        instance.SimilarPoints = instance[
            "point"
        ].NewSimilar  # For external access only
        instance._mark_names = []

        return instance

    def SetPointParameters(self, dom_or_map_or_pdf: point_rng_h) -> None:
        #
        # /!\ Do not pass an array_t to specify a size or domain. It is reserved to map and PDF.
        #
        point_sampler = self["point"]
        signal_dim = point_sampler.signal_dim
        signal_lengths = point_sampler.signal_lengths

        # TODO: allow passing a restricted search domain when passing a map or a pdf (or not)
        #
        if (dom_or_map_or_pdf is None) or isinstance(dom_or_map_or_pdf, tuple):
            if dom_or_map_or_pdf is None:
                dom_or_map_or_pdf = (2 * signal_dim) * [0]
                for idx in range(signal_dim):
                    dom_or_map_or_pdf[2 * idx + 1] = signal_lengths[idx] - 1

            for idx in range(signal_dim):
                if dom_or_map_or_pdf[2 * idx] < 0:
                    raise ValueError(
                        f"Domain dimension {idx}{mg_.SEP}Invalid lower bound: "
                        f"Actual_{dom_or_map_or_pdf[2*idx]} < min_0"
                    )
                if dom_or_map_or_pdf[2 * idx + 1] >= signal_lengths[idx]:
                    raise ValueError(
                        f"Domain dimension {idx}{mg_.SEP}Invalid higher bound: "
                        f"Actual_{dom_or_map_or_pdf[2*idx+1]} >= strict_max_{signal_lengths[idx]}"
                    )

            point_sampler.PrepareForDomain(dom_or_map_or_pdf)

            if (signal_context_t.invalidity_map is not None) and (
                signal_context_t.invalidity_map[point_sampler.domain_slices]
            ).any():
                mg_.ReportW(
                    "Marked point position domain",
                    "Contains invalid signal; Generating a proper map instead",
                )
                proper_map = nmpy.zeros(signal_lengths, dtype=nmpy.bool_)
                proper_map[point_sampler.domain_slices] = True
                proper_map[signal_context_t.invalidity_map] = False
                self.SetPointParameters(proper_map)
        #
        elif isinstance(dom_or_map_or_pdf, array_t):
            if dom_or_map_or_pdf.shape != tuple(signal_lengths):
                raise ValueError(
                    f"Center map or PDF{mg_.SEP}Invalid size: "
                    f"Actual_{dom_or_map_or_pdf.shape}; Expected_{tuple(signal_lengths)}"
                )

            unique_values = nmpy.unique(dom_or_map_or_pdf)
            input_is_map = unique_values.__len__() == 2
            has_invalidity_map = signal_context_t.invalidity_map is not None
            if input_is_map:
                if has_invalidity_map:
                    dom_or_map_or_pdf = dom_or_map_or_pdf == unique_values[-1]
                    true_value = True
                else:
                    true_value = unique_values[-1]
                if (
                    has_invalidity_map
                    and (signal_context_t.invalidity_map[dom_or_map_or_pdf]).any()
                ):
                    mg_.ReportW(
                        "Map for marked point positions",
                        "Contains invalid signal; Correcting the map",
                    )
                    # dom_or_map_or_pdf is a copy, so it can be modified w/o side effecting
                    dom_or_map_or_pdf[signal_context_t.invalidity_map] = False
                point_sampler.PrepareForMap(dom_or_map_or_pdf, true_value)
            else:
                if (
                    has_invalidity_map
                    and (signal_context_t.invalidity_map[dom_or_map_or_pdf > 0.0]).any()
                ):
                    mg_.ReportW(
                        "PDF for marked point positions",
                        "Contains invalid signal; Correcting the PDF",
                    )
                    dom_or_map_or_pdf = dom_or_map_or_pdf.copy()
                    dom_or_map_or_pdf[signal_context_t.invalidity_map] = 0.0
                point_sampler.PrepareForPDF(
                    dom_or_map_or_pdf.astype(nmpy.float64, copy=False)
                )
        #
        else:
            raise TypeError(
                f"{type(dom_or_map_or_pdf)}{mg_.SEP}Invalid point range type; "
                f"Expected={type(None)}, {array_t}, {tuple}"
            )

    def SetMarkParameters(self, mk_ranges: dict, marks_details: dict) -> None:
        #
        if self._mark_names.__len__() > 0:
            raise RuntimeError(
                f"MKPT Sampler{mg_.SEP}Marks cannot be updated; "
                f"Instantiate a new sampler instead"
            )

        for rng_name, value in mk_ranges.items():
            name = rng_name[:-4]
            details = marks_details[name]

            mark_range = value[:2]
            precision = value[2] if value.__len__() > 2 else 0.0
            self._CreateEntryForMark(
                name,
                details.type,
                mark_range,
                precision,
                details.min,
                details.max,
                details.min_inclusive,
                details.max_inclusive,
            )

    def _CreateEntryForMark(
        self,
        mark: str,
        mark_type: Type[float],
        mark_rng: Union[Tuple[int, int], Tuple[float, float]],
        precision: float,
        range_min: float,
        range_max: Union[float, float],
        min_inclusive: bool,
        max_inclusive: bool,
    ) -> None:
        #
        if mark == "point":
            # TODO: still useful, or outdated?
            # Mark name "point" is reserved for point sampling
            raise mg_.BugException()

        if mark_type is int:
            mark_sampler = lambda n_marks: number_sampler_t.RandomIntegers(
                n_marks, mark_rng
            )
        elif mark_type is float:
            # Copy to avoid side effect if modified below (and error if tuple)
            mark_rng = list(mark_rng)

            if (mark_rng[0] == range_min) and not min_inclusive:
                mark_rng[0] = nmpy.nextafter(mark_rng[0], mark_rng[0] + 1.0)

            if (mark_rng[1] < range_max) or max_inclusive:
                # Since numpy uniform generates in [a,b[
                mark_rng[1] = nmpy.nextafter(mark_rng[1], mark_rng[1] + 1.0)

            mark_sampler = lambda n_marks: number_sampler_t.RandomReals(
                n_marks, mark_rng, precision
            )
        else:
            raise TypeError(f'{mark_type}{mg_.SEP}Invalid type for mark "{mark}"')

        sim_sampler = lambda ref_mark, n_marks, fraction: self.__class__._SimilarMarksForOneMark(
            ref_mark, mark_type, mark_rng, precision, n_marks, fraction=fraction
        )
        # caster = lambda value: self.__class__._CastedMark(value, mark_rng)

        self[mark] = mark_sampler_t(
            range=mark_rng,
            NewAny=mark_sampler,
            NewSimilar=sim_sampler,  # , caster=caster
        )
        self._mark_names.append(mark)

    def CenterPointAndExtremeMarks(self) -> Tuple[list, list]:
        #
        min_marks = [self["point"].signal_domain_center]
        max_marks = [self["point"].signal_domain_center]
        for mark_name in self._mark_names:
            mk_range = self[mark_name].range
            min_marks.append(mk_range[0])
            max_marks.append(mk_range[1])

        return min_marks, max_marks

    @classmethod
    def _SimilarMarksForOneMark(
        cls,
        ref_mark,
        mark_type,
        mark_rng,
        precision,
        n_marks: int,
        fraction: float = 0.1,
    ) -> Sequence:
        #
        mini_rng = (
            max(ref_mark * (1 - fraction), mark_rng[0]),
            min(ref_mark * (1 + fraction), mark_rng[1]),
        )
        if mark_type == int:
            mini_rng = nmpy.around(mini_rng).astype(nmpy.int64)
            rdm_marks = number_sampler_t.RandomIntegers(n_marks, mini_rng)
        else:  # Type checking has been done in _CreateEntryForMark
            rdm_marks = number_sampler_t.RandomReals(n_marks, mini_rng, precision)

        return rdm_marks

    def SimilarMarks(self, ref_marks, n_marks: int, fraction: float = 0.1) -> Sequence:
        #
        return tuple(
            self[mark].NewSimilar(ref_marks[mark], n_marks, fraction)
            for mark in self._mark_names
        )

    def NonIntersectingSamples(
        self,
        mkpt_t: marked_point_class_h,
        n_mkpts: int,
        MKPTQuality_fct: Callable[[marked_point_h], float],
        min_quality: float,
        overlap_tolerance: float,
        sampling_map: array_t = None,
    ) -> List[marked_point_h]:
        """
        Generate a list of non-intersecting marked point candidates based on the passed position-and-mark sampler.
        Note that a list, as opposed to a tuple, must be returned (see ???). This list can be empty due to the
        validity and min_quality filtering.
        Returns a list of non-intersecting marked point candidates
        """
        mkpt_dim = self["point"].signal_dim
        points = self["point"].NewAny(n_mkpts)
        marks = tuple(self[mark].NewAny(n_mkpts) for mark in self._mark_names)

        if sampling_map is not None:
            sites_coords = tuple(
                nmpy.rint(coords).astype(nmpy.int64, copy=False) for coords in points
            )
            sampling_map[sites_coords] += 1

        samples = []

        for position_and_marks in zip(*points, *marks):
            new_sample = mkpt_t(
                position_and_marks[:mkpt_dim],
                *position_and_marks[mkpt_dim:],
                check_marks=False,
            )
            if not new_sample.is_valid:
                continue

            intersect = False
            for sample in samples:
                if new_sample.Intersects(sample, overlap_tolerance):
                    intersect = True
                    break
            if not intersect:
                samples.append(new_sample)

        samples = [
            sample for sample in samples if MKPTQuality_fct(sample) >= min_quality
        ]

        return samples

    # @staticmethod
    # def _CastedMark(value: mark_h, mark_rng) -> mark_h:
    #     #
    #     if value < mark_rng[0]:
    #         return mark_rng[0]
    #     elif value > mark_rng[1]:
    #         return mark_rng[1]
    #
    #     return value
