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

from brick.data.config.no_circular_import import PARAMETER_RANGE_SUFFIX
from brick.data.config.std_labels import std_label_e
from brick.data.config.type import (
    missing_required_value_t,
    numeric_t,
    parameter_t,
    section_t,
    text_t,
    tuple_t,
)
from brick.data.config.unit import STD_UNIT_CONVERSIONS


_STD_UNIT_CONVERSIONS = tuple(
    parameter_t(
        name=_elm[0],
        definition=_elm[1].title(),
        description=f"Defined as {1.0 / _elm[3]}{_elm[2]}",
        basic=True,
        optional=True,
        types=float,
        default=_elm[3],
    )
    for _elm in STD_UNIT_CONVERSIONS
)


# fmt: off
CONFIG_SPECIFICATION = {
    std_label_e.sct_mpp: (
        section_t(
            category=std_label_e.cat_optimization,
            definition="Main Obj.MPP parameters",
            description="Algorithmic parameters of Obj.MPP.",
            basic=True,
            optional=False,
        ),
        parameter_t(
            name="n_iterations",
            definition="Number of iterations",
            description="Number of rounds (or iterations) of random candidate object generation. "
                        "There is no default value.",
            basic=True,
            optional=False,
            types=numeric_t(min_=1),
            default=missing_required_value_t(),
        ),
        parameter_t(
            name="n_births_per_iteration",
            definition="Number of object \"births\" at each iteration",
            description="Number of new, random candidate objects generated at each iteration. "
                        "This could be set equal to the expected number of objects in the signal "
                        "although there is no guarantee that this order of magnitude is optimal "
                        "in terms of detection_performance-vs-computation_time trade-off. "
                        "The total number of candidate objects generated will be "
                        "\"n_iterations x n_births_per_iteration\". "
                        "The default value is 20.",
            basic=False,
            optional=True,
            types=numeric_t(min_=1),
            default=100,
        ),
        parameter_t(
            name="seed",
            definition="Seed for pseudo-random number generation",
            description="The seed used to initialize the pseudo-random number generator "
                        "used to build random candidate objects. This parameter should usually be ignored. "
                        "It is mainly used to make the randomness in Obj.MPP \"predictable\" "
                        "when testing or debugging. "
                        "If None, there is no specific seeding."
                        "The default value is None.",
            basic=False,
            optional=True,
            types=(None, numeric_t(min_=0, max_=2**32 - 1)),
            default=None,
        ),
        parameter_t(
            name="n_parallel_workers",
            definition="Number of parallel detection subtasks",
            description="Number of subtasks the detection task will be split into to be run in parallel. "
                        "If equal to 1, the detection task will be run sequentially. "
                        "If > 1, that number of subtasks will be used. "
                        "If <= 0, Obj.MPP will choose the number of subtasks based on the number of CPU cores. "
                        "Note that this parameter is ignored on Windows, falling back to sequential processing "
                        "(see the documentation of the \"fork\" start method in the \"multiprocessing\" Python module). "
                        "The default value is 0.",
            basic=False,
            optional=True,
            types=int,
            default=0,
        ),
        parameter_t(
            name="use_history",
            definition="Whether to use a previous detection result",
            description="",
            basic=False,
            optional=True,
            types=bool,
            default=False,
        ),
        parameter_t(
            name="fixed_history",
            definition="Whether to make the previous detection result immutable and unremovable",
            description="",
            basic=False,
            optional=True,
            types=bool,
            default=False,
        ),
    ),
    # --- CHECK ADVANCEMENT MARK ---
    std_label_e.sct_refinement: (
        section_t(
            category=std_label_e.cat_optimization,
            definition="Refinement parameters",
            description="",
            basic=False,
            optional=True,
        ),
        parameter_t(
            name="age_for_refinement",
            definition="",
            description="",
            basic=False,
            optional=True,
            types=(None, numeric_t(min_=0)),
            default=None,
        ),
        parameter_t(
            name="n_refinement_attempts",
            definition="",
            description="",
            basic=False,
            optional=True,
            types=numeric_t(min_=1),
            default=10,
        ),
        parameter_t(
            name="refinement_fraction",
            definition="",
            description="",
            basic=False,
            optional=True,
            types=numeric_t(min_=0.0, min_inclusive = False),
            default=0.1,
        ),
    ),
    std_label_e.sct_feedback: (
        section_t(
            category=std_label_e.cat_optimization,
            definition="",
            description="",
            basic=False,
            optional=True,
        ),
        parameter_t(
            name="status_period",
            definition="Time in seconds between two status feedback (0 -> no feedback)",
            description="",
            basic=False,
            optional=True,
            types=numeric_t(min_=0.0),
            default=2.0,
        ),
    ),
    std_label_e.sct_object: (
        section_t(
            category=std_label_e.cat_object,
            definition="Object type and common properties",
            description="",
            basic=True,
            optional=False,
        ),
        parameter_t(
            name="object_type",
            definition="[Object module:]Object type",
            description="Before the colon: Object module path (absolute or relative to ini file) "
            "or object module name in brick/marked_point/(oneD|twoD|threeD), "
            'with "py" extension chopped off. '
            "E.g. circle for circle.py. "
            "This part, including the colon, is optional. "
            "Since when this part is omitted, a module is searched for in several folders, "
            "these modules should have different names to avoid masking modules in subsequently visited folders. "
            'After the colon: An object type defined in the object module with "_t" suffix chopped off. '
            "E.g. circle for class circle_t",
            basic=True,
            optional=False,
            types=text_t(text_t.MARKED_POINT),
            default=missing_required_value_t(),
        ),
        parameter_t(
            # TODO: check if this can be a path to a folder of center images
            name="center" + PARAMETER_RANGE_SUFFIX,
            definition="",
            description="- None = No constraint on position: it can be anywhere inside image domain"
            "- Bounding box: list/tuple containing min_row, max_row,... in this order"
            "- Path to an image representing a map (image containing 2 distinct values, "
            "the locii of the max being valid points) or "
            "a PDF (image of positive values summing to 1 used to draw points).",
            basic=False,
            optional=True,
            types=(None, tuple_t((4,6), obj_mpp_type=tuple_t.DOMAIN_REGION), text_t(text_t.PATH_DOCUMENT)),
            default=None,
        ),
        parameter_t(
            name="only_uncropped",
            definition="Only retain objects that do not cross domain border",
            description="",
            basic=False,
            optional=True,
            types=bool,
            default=True,
        ),
    ),
    std_label_e.sct_object_ranges: (
        section_t(
            category=std_label_e.cat_object,
            definition="Specific to the selected object type",
            description="",
            basic=True,
            optional=False,
        ),
    ),
    std_label_e.sct_range_units: (
        section_t(
            category=std_label_e.cat_object,
            definition="Unit conversions",
            description="Standard units: "
            "p=pixel, v=voxel, si=sample=site=pixel or voxel, "
            "<prefix>m=metric units (e.g. um; prefix: k, <empty>, c, m, u=micro, n=nano), "
            "mi/yd/ft/in=imperial units, "
            "r=radian, d=degree, "
            "yr/mo/wk/dy/h/mn/<prefix>s (prefix: <empty>, m, u=micro, n=nano)",
            basic=True,
            optional=True,
        ),
    ) + _STD_UNIT_CONVERSIONS,
    std_label_e.sct_quality: (
        section_t(
            category=std_label_e.cat_object,
            definition="Common to any object quality",
            description="",
            basic=True,
            optional=False,
        ),
        parameter_t(
            name="object_quality",
            definition="[Quality module:]Quality class",
            description="Before the colon: Quality module path (absolute or relative to ini file) "
            "or object module name in brick/quality/(oneD|twoD|threeD), "
            'with "py" extension chopped off. '
            "E.g. contrast for contrast.py. "
            "This part, including the colon, is optional. "
            "Since when this part is omitted, a module is searched for in several folders, "
            "these modules should have different names to avoid masking modules in subsequently visited folders. "
            'After the colon: A quality class defined in the quality module with "_t" suffix chopped off. '
            "E.g. bright_on_dark_contrast for class bright_on_dark_contrast_t",
            basic=True,
            optional=False,
            types=text_t(text_t.QUALITY),
            default=missing_required_value_t(),
        ),
        parameter_t(
            name="min_quality",
            definition="",
            description="",
            basic=True,
            optional=False,
            types=float,
            default=missing_required_value_t(),
        ),
    ),
    std_label_e.sct_quality_prm: (
        section_t(
            category=std_label_e.cat_object,
            definition="Specific to the selected object quality",
            description="",
            basic=False,
            optional=True,
        ),
    ),
    std_label_e.sct_incitations: (
        section_t(
            category=std_label_e.cat_object,
            definition="Incentives on Generated Objects",
            description="",
            basic=False,
            optional=True,
        ),
        parameter_t(
            name="area_weight",
            definition="Favors large objects",
            description="The qualities are scaled by this weight times the object areas "
            "when solving object overlapping. "
            "A value of 0 inhibits the weighting.",
            basic=False,
            optional=True,
            types=numeric_t(float),
            default=0.0,
        ),
    ),
    std_label_e.sct_constraints: (
        section_t(
            category=std_label_e.cat_object,
            definition="Constraints on Generated Objects",
            description="",
            basic=False,
            optional=True,
        ),
        parameter_t(
            name="overlap_tolerance",
            definition="As a percentage (0.0 => no overlap allowed)",
            description="",
            basic=False,
            optional=True,
            types=numeric_t(min_=0.0, max_=100.0),
            default=20.0,
        ),
    ),
    std_label_e.sct_signal: (
        section_t(
            category=std_label_e.cat_input,
            definition="Common to any signal loading function",
            description="",
            basic=True,
            optional=False,
        ),
        parameter_t(
            name="signal_path",
            definition="Image path or image folder path",
            description="Path to raw signal (either a single file or a folder (absolute or relative to ini file) "
            "that will be scanned w/o recursion)",
            basic=True,
            optional=False,
            types=text_t(text_t.PATH_ANY),
            default=missing_required_value_t(),
        ),
        parameter_t(
            # TODO: check if this can be a path to a folder of center images
            name="vmap_path",
            definition="Signal validity map image path or signal validity map image folder path",
            description="Path to signal validity map (either a single file or a folder (absolute or relative to ini file) "
            "that will be scanned w/o recursion). For each raw signal, there can be a corresponding "
            "validity map or not",
            basic=False,
            optional=True,
            types=(None,text_t(text_t.PATH_DOCUMENT)),
            default=None,
        ),
        parameter_t(
            name="signal_loading_function",
            definition="",
            description="Raw signal loading module in given folder (absolute or relative to ini file) or "
            "in helper with py extension chopped off. E.g. signal_loading for signal_loading.py. "
            "Optional = signal_loading module in helper. "
            "It must accept a parameter named signal_path",
            basic=False,
            optional=True,
            types=text_t(text_t.FUNCTION),
            default="signal_loading:SingleChannelOfImage",
        ),
    ),
    std_label_e.sct_signal_loading_prm: (
        section_t(
            category=std_label_e.cat_input,
            definition="Specific to the selected signal loading function",
            description="",
            basic=False,
            optional=True,
        ),
    ),
    std_label_e.sct_signal_processing_prm: (
        section_t(
            category=std_label_e.cat_input,
            definition="Specific to the selected object quality: parameters for the function converting "
            "loaded raw signal into signal used by object quality",
            description="",
            basic=False,
            optional=True,
        ),
    ),
    std_label_e.sct_output: (
        section_t(
            category=std_label_e.cat_output,
            definition="",
            description="",
            basic=True,
            optional=True,
        ),
        parameter_t(
            name="console",
            definition="Whether to print the result in the console",
            description="",
            basic=False,
            optional=True,
            types=bool,
            default=True,
        ),
        parameter_t(
            name="output_path",
            definition="Base output folder",
            description="",
            basic=True,
            optional=True,
            types=(None, text_t(text_t.PATH_FOLDER)),
            default=None,
        ),
        parameter_t(
            name="marks_output",
            definition="Whether to output the marks of the detected marked points in a CSV file",
            description="",
            basic=True,
            optional=True,
            types=bool,
            default=False,
        ),
        parameter_t(
            name="mkpt_output",
            definition="Whether to output the detected marked points in a file that can be reloaded to recreate them",
            description="",
            basic=True,
            optional=True,
            types=bool,
            default=False,
        ),
        parameter_t(
            name="contour_output",
            definition="Whether to save the contours of the detected marked points in an image file",
            description="",
            basic=True,
            optional=True,
            types=bool,
            default=False,
        ),
        parameter_t(
            name="region_output",
            definition="Whether to save the regions of the detected marked points in an image file",
            description="",
            basic=True,
            optional=True,
            types=bool,
            default=False,
        ),
        parameter_t(
            name="region_numpy_output",
            definition="Whether to save the regions of the detected marked points in a Numpy file (.npz)",
            description="",
            basic=True,
            optional=True,
            types=bool,
            default=False,
        ),
        parameter_t(
            name="result_output_function",
            definition="",
            description="Result output module in given folder (absolute or relative to ini file) or "
            'in helper with "py" extension chopped off. '
            "E.g. result_output for result_output.py. Optional  =  result_output module in helper. "
            "Result output function: Output2DObjects if processing a single "
            "datum, or None if processing a signal folder",
            basic=False,
            optional=True,
            types=(None, text_t(text_t.FUNCTION)),
            default=None,
        ),
        parameter_t(
            name="marks_separator",
            definition="Marks separator for the CSV format",
            description="",
            basic=True,
            optional=True,
            types=str,
            default=",",
        ),
    ),
    std_label_e.sct_output_prm: (
        section_t(
            category=std_label_e.cat_output,
            definition="Specific to the select result output function",
            description="",
            basic=False,
            optional=True,
        ),
    ),
}
# fmt: on


for value in CONFIG_SPECIFICATION.values():
    for parameter in value[1:]:
        if not isinstance(parameter.types, tuple):
            parameter.types = (parameter.types,)
        if isinstance(parameter.default, missing_required_value_t):
            parameter.default.SetTypes(parameter.types)


# TODO: re-arrange the following (taken from config.py)
# Some coherence contraints:
#     section_is_basic or cs_.SectionIsOptional(sct_label)
#     section_is_basic and (n_parameters > 0) and (n_basic_prms == 0)
#
# if (not section_is_basic) and (prm_details.basic):
#     raise ValueError(
#         f"{sct_label}.{prm_details.name}{mg_.SEP}Basic parameter in a non-basic section"
#     )
# if not (prm_details.basic or prm_details.optional):
#     raise ValueError(
#         f"{sct_label}.{prm_details.name}{mg_.SEP}Parameter is not basic but not optional"
#     )
# if isinstance(prm_details.default, missing_required_prm_t):
#     if prm_details.optional:
#         raise ValueError(
#             f"{sct_label}.{prm_details.name}{mg_.SEP}Required parameter declared optional"
#         )
#     # TODO: revert to equality when multiple types allowed
#     # if prm_details.default.type != prm_details.type:
#     if prm_details.default.type not in prm_details.type:
