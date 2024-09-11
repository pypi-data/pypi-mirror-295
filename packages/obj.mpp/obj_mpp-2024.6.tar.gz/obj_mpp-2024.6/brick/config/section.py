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

from typing import Any, ClassVar, Dict, Optional, Sequence, Tuple, Union

from brick.config.parameter import parameter_t
from brick.data.config.specification import CONFIG_SPECIFICATION
from brick.data.config.specification import section_t as static_section_t
from brick.data.config.std_labels import std_label_e


class section_t(list):

    VALID_SECTION_NAMES: ClassVar[Tuple[std_label_e, ...]] = tuple(
        CONFIG_SPECIFICATION.keys()
    )

    __slots__ = ("name",) + static_section_t._fields

    name: std_label_e

    @classmethod
    def FromSpecification(
        cls,
        name: std_label_e,
        specification: static_section_t,
        parameters: Sequence[parameter_t],
    ) -> section_t:
        """"""
        instance = cls()

        for field in static_section_t._fields:
            setattr(instance, field, getattr(specification, field))

        instance.name = name
        instance.extend(parameters)

        return instance

    def ParameterWithName(self, name: str) -> Optional[parameter_t]:
        """"""
        for parameter in self:
            if parameter.name == name:
                return parameter

        return None

    def IndexOf(self, name: str) -> Optional[int]:
        """"""
        for p_idx, parameter in enumerate(self):
            if parameter.name == name:
                return p_idx

        return None

    def AsDict(self) -> Dict[str, str]:
        """"""
        return {_prm.name: _prm.value for _prm in self}

    def __contains__(self, item: Union[parameter_t, str]) -> bool:
        """"""
        if isinstance(item, parameter_t):
            return super().__contains__(parameter_t)
        else:
            for parameter in self:
                if item == parameter.name:
                    return True
            return False

    def __getitem__(self, key: Union[int, str]) -> Optional[Union[parameter_t, Any]]:
        """"""
        if isinstance(key, int):
            return super().__getitem__(key)
        else:
            parameter = self.ParameterWithName(key)
            if parameter is None:
                return None
            else:
                return parameter.value


def SectionLabelFromName(name: Union[str, std_label_e]) -> Optional[std_label_e]:
    """"""
    for valid_name in section_t.VALID_SECTION_NAMES:
        if name == valid_name.value:
            return valid_name

    return None


def NonDefaultUnits(units: section_t) -> section_t:
    """"""
    output = section_t()

    for field in static_section_t._fields:
        setattr(output, field, getattr(units, field))
    output.name = units.name

    for unit in units:
        if unit.value != unit.default:
            output.append(unit)

    return output
