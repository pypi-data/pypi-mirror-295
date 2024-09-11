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
import brick.structure.explorer as ex_
from brick.data.type import pl_path_t

import importlib as il_
import importlib.util as iu_
from typing import Any, Optional


def ModuleUsingAltImport(mod_info: pl_path_t, relative_to: pl_path_t = None) -> Any:
    #
    if relative_to is None:
        base_folder = pl_path_t()  # Equivalent to: os_.curdir => '.'
    elif relative_to.is_dir():
        base_folder = relative_to
    else:
        base_folder = relative_to.parent
    base_folder = base_folder.resolve()

    if mod_info.parts.__len__() > 1:
        mod_name = pl_path_t(mod_info.name)

        if mod_info.is_absolute():
            mod_path = mod_info
        else:
            mod_path = base_folder / mod_info
    else:
        mod_name = mod_info
        mod_path = base_folder / mod_info

    if mod_name.suffix.lower() == ".py":
        mod_name = mod_name.stem
    else:
        mod_path = pl_path_t(mod_path.__str__() + ".py")

    if not mod_path.is_file():
        return None

    # spec_from_file_location does not accept pathlib.PosixPath arguments
    spec = iu_.spec_from_file_location(mod_name.__str__(), mod_path.__str__())
    if spec is None:
        return None

    return spec.loader.load_module(spec.name)


def StandardModuleFromName(
    mod_name: pl_path_t,
    category: str,
    return_type: str = "py_module",  # Choices are: path, py_path, py_module
):
    #
    if mod_name.suffix.lower() != ".py":
        mod_name = pl_path_t(mod_name.__str__() + ".py")

    for path_parts in ex_.PathsFromPathDict(category, "parts"):
        path = path_parts[0].joinpath(*(path_parts[1:]), mod_name)
        if path.is_file():
            if return_type == "path":
                return path
            elif (return_type == "py_path") or (return_type == "py_module"):
                py_path = ".".join(path_parts[1:]) + "." + mod_name.stem
                if return_type == "py_path":
                    return py_path
                else:
                    return il_.import_module(py_path)
            else:
                raise TypeError(f"{return_type}{mg_.SEP}Invalid return type")

    return None


def StandardModuleFromElement(
    elm_name: str,
    category: str,
    elm_is_class: bool = True,
    return_type: str = "py_elm",
) -> Optional[Any]:
    """
    :param elm_name:
    :param category:
    :param elm_is_class:
    :param return_type: Choices are: path, py_path, py_module, py_elm
    :return:
    """
    if elm_is_class and not elm_name.endswith("_t"):
        elm_name += "_t"

    for path_parts in ex_.PathsFromPathDict(category, "parts"):
        for path in pl_path_t().joinpath(*path_parts).glob("*.??"):
            if (path.suffix.lower() == ".py") and path.is_file():
                py_path = ".".join(path_parts[1:]) + "." + path.stem.__str__()
                elm = __ModuleElement__(elm_name, path, py_path, return_type)
                if elm is not None:
                    return elm

    return None


def HelperModuleFromElement(
    elm_name: str,
    return_type: str = "py_elm",  # Choices are: path, py_path, py_module, py_elm
) -> Any:
    #
    return StandardModuleFromElement(
        elm_name, "helper", elm_is_class=False, return_type=return_type
    )


def __ModuleElement__(
    elm_name: str, path: pl_path_t, py_path: str, return_type: str
) -> Any:
    """
    :param elm_name:
    :param path:
    :param py_path:
    :param return_type: Choices are: path, py_path, py_module, py_elm
    :return:
    """
    py_module = il_.import_module(py_path)

    if hasattr(py_module, elm_name):
        if return_type == "path":
            return path
        elif return_type == "py_path":
            return py_path
        elif return_type == "py_module":
            return py_module
        elif return_type == "py_elm":
            return getattr(py_module, elm_name)
        else:
            raise TypeError(f"{return_type}{mg_.SEP}Invalid return type")

    return None


def ElementInModule(
    elm_name: str,
    mod_name: pl_path_t = None,
    category: str = None,
    elm_is_class: bool = True,
) -> Any:
    #
    if mod_name is None:
        # Look among standard modules (category is needed then) or helper modules
        if category is None:
            py_elm = HelperModuleFromElement(elm_name)
        else:
            py_elm = StandardModuleFromElement(
                elm_name, category, elm_is_class=elm_is_class
            )
    else:
        if elm_is_class and not elm_name.endswith("_t"):
            elm_name += "_t"
        if category is None:
            category = "helper"

        if mod_name.is_absolute():
            module = ModuleUsingAltImport(mod_name)
        else:
            module = StandardModuleFromName(mod_name, category)
            if (module is None) or not hasattr(module, elm_name):
                module = ModuleUsingAltImport(mod_name)
            if module is None:
                raise ImportError(f"{mod_name}{mg_.SEP}Module not found")

        py_elm = getattr(module, elm_name)

    if py_elm is None:
        raise ImportError(
            f"CAT_{category}.MOD_{mod_name}.ELM_{elm_name} "
            f"(IS_CLASS_{elm_is_class}){mg_.SEP}Element not found"
        )

    return py_elm
