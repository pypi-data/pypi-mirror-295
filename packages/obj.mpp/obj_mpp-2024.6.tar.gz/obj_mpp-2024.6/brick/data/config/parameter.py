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
from brick.data.config.std_labels import std_label_e


# --- Access the following constants through the dedicated, section and parameter classes

PARAMETER_WORD_SEPARATOR = "_"
PARAMETER_UID_SEPARATOR = "."

# PARAMETER_RANGE_MARKER = "range"
# PARAMETER_PATH_MARKER = "path"
# PARAMETER_FUNCTION_MARKER = "function"

OUTPUT_PARAMETERS = {
    std_label_e.sct_output: tuple(
        _prm.name for _prm in CONFIG_SPECIFICATION[std_label_e.sct_output][1:]
    )
}
_OUTPUT_PARAMETERS = []
for key, values in OUTPUT_PARAMETERS.items():
    for value in values:
        _OUTPUT_PARAMETERS.append((key, value))
OUTPUT_PARAMETERS = tuple(_OUTPUT_PARAMETERS)

# fmt: off
# Key=elm i.e. element (of the config) i.e. parameter name
# Value=(section, module parameter to be added to the config)
DOC_ELM_SPLITABLE_PRMS = {
    "object_type":             (std_label_e.sct_object,  "object_module"),
    "object_quality":          (std_label_e.sct_quality, "object_quality_module"),
    "signal_loading_function": (std_label_e.sct_signal,  "signal_loading_module"),
    "result_output_function":  (std_label_e.sct_output,  "result_output_module"),
}
# fmt: on

PATH_PARAMETERS = (
    (std_label_e.sct_signal, "signal_path"),
    (std_label_e.sct_signal, "vmap_path"),
    (std_label_e.sct_object, "center_rng"),
    (std_label_e.sct_output, "output_path"),
)
