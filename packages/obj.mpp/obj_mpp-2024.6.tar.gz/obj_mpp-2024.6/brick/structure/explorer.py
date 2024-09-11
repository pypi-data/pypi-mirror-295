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

import brick.data.structure.explorer as ex_
import brick.interface.io.reporting as mg_
from brick.data.type import pl_path_t

import importlib.util as iu_
import inspect as sp_
from collections import namedtuple as namedtuple_t
from enum import Enum as enum_t
from typing import Any, Optional, Union


fct_signature_t = namedtuple_t(
    "fct_signature_t",
    "arg_names arg_types arg_default_values has_var_keyword return_types documentation",
)


def PathsFromPathDict(
    path_dict: Union[dict, str], mode: str  # Choices: 'parts', 'path', 'py_path'
) -> tuple:
    #
    # Returns a list of paths for dictionary-based, hierarchical representation
    #
    if isinstance(path_dict, enum_t):
        path_dict = path_dict.name.lower()
    if isinstance(path_dict, str):  # It is a key in standard_module_paths
        path_dict = ex_.STANDARD_MODULE_PATHS[path_dict]

    paths = [[elm, path_dict[elm]] for elm in path_dict]

    while any(path[-1].__len__() > 0 for path in paths):
        next_paths = []
        for path in paths:
            next_path = path[-1]
            if next_path.__len__() > 0:
                next_paths.extend(
                    [path[:-1] + [key, next_path[key]] for key in next_path]
                )
            else:
                next_paths.append(path)
        paths = next_paths

    base_folder = pl_path_t(__file__).parent.joinpath(
        "..", ".."
    )  # /!\ To be changed if this file is moved

    # Note: last element of each element of paths is {} => path[:-1]
    if mode == "parts":
        paths = (tuple([base_folder] + path[:-1]) for path in paths)
    elif mode == "path":
        paths = (base_folder.joinpath(*(path[:-1])) for path in paths)
    elif mode == "py_path":
        paths = (".".join(path[:-1]) for path in paths)
    else:
        raise ValueError(f"{mode}{mg_.SEP}Invalid mode")

    return tuple(paths)


def StandardModules(category: str, with_path: bool = False) -> tuple:
    #
    modules = []

    for folder in PathsFromPathDict(category, "path"):
        for module in folder.glob("*.??"):
            if (module.suffix.lower() == ".py") and module.is_file():
                if with_path:
                    modules.append((module.stem, module))
                else:
                    modules.append(module.stem)

    return tuple(sorted(modules))


def StandardMarkedPoints(mode: str) -> tuple:  # Choices: 'name', 'type_name', 'class'
    #
    marked_points = []

    for module in StandardModules("marked_point", with_path=True):
        marked_point = MarkedPoint(*module, mode)
        if marked_point is not None:
            marked_points.append(marked_point)

    if mode == "class":
        return tuple(
            sorted(set(marked_points), key=lambda class_type: class_type.__name__)
        )

    return tuple(sorted(set(marked_points)))


def StandardQualityFunctionInfos() -> dict:
    #
    # STANDARD_QUALITIES = (
    #     "contour",
    #     "bright_on_dark_contrast",
    #     "dark_on_bright_contrast",
    #     "bright_on_dark_gradient",
    #     "dark_on_bright_gradient",
    # )
    #
    q_functions = {}

    for module in StandardModules("quality", with_path=True):
        q_functions.update(_QualityFunctionsInfos(*module))

    return q_functions


def MarkedPoint(
    mod_name: str,
    mod_path: pl_path_t,
    mode: str,  # Choices: 'name', 'type_name', 'class'
) -> Optional[Union[str, type]]:
    #
    spec = iu_.spec_from_file_location(mod_name, mod_path)
    module = spec.loader.load_module(spec.name)

    for type_name, class_type in sp_.getmembers(module, sp_.isclass):
        if (
            (class_type.__module__ == mod_name)
            and type_name.endswith("_t")
            and not (type_name.startswith("_") or type_name.startswith("marked_point_"))
        ):
            for mro in sp_.getmro(class_type)[
                1:
            ]:  # First is self => no need to process
                if mro.__name__ == "marked_point_t":
                    if mode == "name":
                        return type_name[:-2]
                    elif mode == "type_name":
                        return type_name
                    elif mode == "class":
                        return class_type
                    else:
                        raise ValueError(f"{mode}{mg_.SEP}Invalid mode")

    return None


def _QualityFunctionsInfos(mod_name: str, mod_path: pl_path_t) -> dict:
    #
    spec = iu_.spec_from_file_location(mod_name, mod_path)
    module = spec.loader.load_module(spec.name)

    infos = {}
    for type_name, class_type in sp_.getmembers(module, sp_.isclass):
        if (
            (class_type.__module__ == mod_name)
            and type_name.endswith("_t")
            and not type_name.startswith("_")
        ):
            # First is self => no need to process
            for mro in sp_.getmro(class_type)[1:]:
                if mro.__name__ == "quality_env_t":
                    try:
                        instance = class_type()
                        infos[mod_name + "." + type_name[:-2]] = (
                            class_type,
                            FunctionInfosFromName(
                                instance.MKPTQuality.__name__, module
                            ),
                        )
                    except TypeError:
                        pass

    return infos


def FunctionInfos(function) -> fct_signature_t:
    #
    signature = sp_.signature(function)
    names, types, defaults, has_var_keyword = [], {}, {}, False

    for arg_name, arg_value in signature.parameters.items():
        names.append(arg_name)
        if arg_value.kind == arg_value.VAR_POSITIONAL:
            # This is only a way to avoid to properly deal with a VAR_POSITIONAL parameter (which must not appear in
            # SignalsFromRawSignal and MKPTQuality functions.
            defaults[arg_name] = None
        elif arg_value.kind == arg_value.VAR_KEYWORD:
            defaults[arg_name] = None
            has_var_keyword = True
        else:
            if arg_value.annotation is not arg_value.empty:
                types[arg_name] = arg_value.annotation
            if arg_value.default is not arg_value.empty:
                defaults[arg_name] = arg_value.default

    fct_signature = fct_signature_t(
        arg_names=names,
        arg_types=types,
        arg_default_values=defaults,
        has_var_keyword=has_var_keyword,
        return_types=signature.return_annotation,
        documentation=sp_.getdoc(function),
    )

    return fct_signature


def FunctionInfosFromName(name: str, module: Any) -> fct_signature_t:
    #
    return FunctionInfos(getattr(module, name))
