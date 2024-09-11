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

import brick.interface.ko.text_color as tc_
import brick.interface.io.reporting as mg_
from brick.structure.explorer import fct_signature_t


# TODO: check also returned objects, but maybe not here, because here the parameters in the INI file are checked, while
# the return type is a verification of the function definition (not the function call).
def CheckPassedParameters(
    fct_name: str, fct_signature: fct_signature_t, passed_prms: dict, n_v_excluded: int = 0
) -> None:
    #
    # Quality functions all have their first parameter in common: a marked point.
    # SignalsFromRawSignal functions all have their first two parameters in common: the signal and the mkpt dimension.
    # fct_signature contains all parameters, including common ones. However, in the above contexts, passed_prms
    # only describe the parameters after these common ones. n_v_excluded allows to ignore such common
    # parameters in fct_signature since they are missing from passed_prms.
    #
    # This function is not meant to be a general parameter-passing validator. It applies to the following cases:
    # POSITIONAL_ONLY or POSITIONAL_OR_KEYWORD parameters, optionally followed by KEYWORD_ONLY parameters, optionally
    # followed by a VAR_KEYWORD parameter (**kwargs). It cannot deal with a VAR_POSITIONAL parameter (*args).
    #
    mg_.ReportI(tc_.ColoredText(f"Function \"{fct_name}\":\n"
                                f"Checking parameters set in configuration...", "blue"))

    valid_names = fct_signature.arg_names
    valid_types = fct_signature.arg_types
    valid_defaults = fct_signature.arg_default_values
    has_var_keyword = fct_signature.has_var_keyword

    valid_names = valid_names[n_v_excluded:]

    any_errors = False

    for valid_name in valid_names:
        if valid_name in passed_prms:
            if not isinstance(passed_prms[valid_name], valid_types[valid_name]):
                mg_.ReportE(
                    valid_name,
                    f"Incorrect parameter type: "
                    f"Passed={passed_prms[valid_name]} "
                    f"with type {type(passed_prms[valid_name])}; "
                    f"Expected={valid_types[valid_name]}"
                )
                any_errors = True
        elif not valid_name in valid_defaults:
            # print("--------- IN CHECKER")
            mg_.ReportE(valid_name, 'Missing required parameter')
            any_errors = True

    passed_names = tuple(passed_prms)
    for passed_name in passed_names:
        if not ((passed_name in valid_names) or has_var_keyword):
            mg_.ReportIP(passed_name, 'parameter', valid_names)
            any_errors = True

    if any_errors:
        mg_.ReportI(f"Valid parameter(s) for this function: {', '.join(valid_names)}")
        raise mg_.silent_exception_t()
    else:
        mg_.ReportI(tc_.ColoredText("Check PASSED", "green"))
