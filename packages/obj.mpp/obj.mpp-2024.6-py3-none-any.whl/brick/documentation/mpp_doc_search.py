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

from brick.data.config.specification import CONFIG_SPECIFICATION
from brick.data.config.type import missing_required_value_t, parameter_t, section_t
import brick.interface.ko.text_color as tc_

import re as re_


def QueryResult(query: str) -> None:
    #
    query = query.lower()

    for sct_label, sct_prms in CONFIG_SPECIFICATION.items():
        sct_name = sct_label.value
        if query in sct_name.lower():
            print(tc_.ColoredText(f"[{sct_name}]", "blue"), end="")
            __PrintSectionDetails__(sct_prms[0], query)
            for prm in sct_prms[1:]:
                __PrintParameterDetails__(prm, query)
            print("")
        else:
            for prm in sct_prms[1:]:
                if any(
                    query in elm
                    for elm in prm.AsDict().values()
                    if isinstance(elm, str)
                ):
                    print(tc_.ColoredText(f"[{sct_name}]", "blue"), end="")
                    __PrintSectionDetails__(sct_prms[0], query)
                    __PrintParameterDetails__(prm, query)
                    print("")


def __PrintSectionDetails__(section: section_t, query: str) -> None:
    #
    print(
        f" {__WithEmphasizedWord__(section.definition, query)} / "
        f"cat={section.category.value} / "
        f"adv.opt={not section.basic}.{section.optional}"
    )


def __PrintParameterDetails__(prm: parameter_t, query: str) -> None:
    #
    type_for_dsp = list(prm.types)
    for idx in range(type_for_dsp.__len__()):
        if type_for_dsp[idx] is None:
            type_for_dsp[idx] = "None"
        else:
            type_for_dsp[idx] = type(type_for_dsp[idx]).__name__
    type_for_dsp = " or ".join(type_for_dsp)
    if isinstance(prm.default, missing_required_value_t):
        prm_default = "No defaults"
    else:
        prm_default = prm.default
    print(
        f"\n    {tc_.ColoredText(prm.name, 'magenta')}: "
        f"{__WithEmphasizedWord__(prm.definition, query)}\n"
        f"        def={prm_default}\n"
        f"        type={type_for_dsp}\n"
        f"        adv.opt={not prm.basic}.{prm.optional}"
    )


def __WithEmphasizedWord__(sentence: str, word: str) -> str:
    #
    return re_.sub(
        word,
        lambda wrd: tc_.ColoredText(wrd[0], "green"),
        sentence,
        flags=re_.IGNORECASE,
    )
