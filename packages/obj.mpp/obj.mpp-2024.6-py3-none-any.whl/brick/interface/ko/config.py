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

import argparse as ap_

from brick.config.config import config_t
from brick.config.parameter import parameter_t
from brick.data.config.type import missing_required_value_t,text_t, tuple_t, numeric_t
from brick.data.config.specification import CONFIG_SPECIFICATION



def CommandLineParser() -> ap_.ArgumentParser:
    #
    description = "Obj.MPP: Object detection using a Marked Point Process"

    parser = ap_.ArgumentParser(description=description, allow_abbrev=False)
    parser.add_argument(
        type=str,
        dest=config_t.INI_DOCUMENT_OPTION,
        help="Path to INI configuration file",
        default=None,
        nargs="?",
        metavar="INI_config_file",
    )

    for section_name, elements in CONFIG_SPECIFICATION.items():
        for specification in elements[1:]:
            non_none_types = specification.types[int(specification.types[0] is None):]
            main_type = non_none_types[0]
            if isinstance(main_type, numeric_t):
                main_type = main_type.python_type
            elif isinstance(main_type, tuple_t):
                main_type = tuple
            elif isinstance(main_type, text_t):
                main_type = str
            # missing_required_value_t: To avoid overwriting by default value in OverwriteConfigWithArgs
            parser.add_argument(
                f"--{section_name}-{specification.name}",
                type=main_type,
                dest=parameter_t.ParameterUId(section_name, specification.name),
                help=specification.definition,
                default=missing_required_value_t(non_none_types),
            )

    return parser
