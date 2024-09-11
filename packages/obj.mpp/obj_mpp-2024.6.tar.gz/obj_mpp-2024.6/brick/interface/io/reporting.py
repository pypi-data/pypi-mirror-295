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

import difflib as df_
import os.path as ph_
import sys as sy_
from os import environ as ENVIRONMENT
from typing import Optional, Sequence


# TODO: when using "print": currently unused (check if needed to deal with QT widget encoding)
# console_encoding = sy_.stdout.encoding if console == sy_.stdout \
#                    else sy_.getfilesystemencoding()

# file argument in print function (type=typing.TextIO or io.TextIOWrapper)


TARGET = sy_.stdout
END_CHARACTER = "\n"  # end argument in print function

SEP = "#"


# TODO: explain what are they used for
class silent_exception_t(Exception):
    pass


def SetTarget(target, end_character: str = None) -> None:
    #
    global TARGET, END_CHARACTER

    TARGET = target
    if end_character is not None:
        END_CHARACTER = end_character


def ReportI(message: str) -> None:
    """
    Information
    """
    print(message, end=END_CHARACTER, file=TARGET)


def ReportW(what: Optional[str], how: str, wtype=RuntimeWarning) -> None:
    """
    Warning
    """
    _Report(what, f"[{wtype.__name__}] {how}", how_color="magenta")


def ReportE(what: Optional[str], how: str) -> None:
    """
    Error
    """
    _Report(what, how, how_color="red")


def ReportIP(what: str, how: str, valid_parameters: Sequence[str]):
    """
    Invalid Parameter
    """
    close_matches = df_.get_close_matches(what, valid_parameters)
    if close_matches.__len__() > 0:
        close_matches = f"Close matche(s): {', '.join(close_matches)}"
    else:
        close_matches = "No Close matches"

    ReportE(what, f"Invalid {how}; {close_matches}")


def ReportX(etype, message, trace) -> None:
    """
    eXception
    """
    if etype.__name__ == silent_exception_t.__name__:
        return

    while trace.tb_next is not None:
        trace = trace.tb_next
    frame = trace.tb_frame

    module = ph_.basename(frame.f_code.co_filename)
    function = frame.f_code.co_name
    line = frame.f_lineno.__str__()

    message = message.__str__()
    if SEP in message:
        what, message = message.split(sep=SEP, maxsplit=1)
        message = f"[{etype.__name__}] {message}"
    else:
        what = message
        message = etype.__name__

    module = tc_.ColoredText(module, "blue")
    function = tc_.ColoredText(function, "blue")
    line = tc_.ColoredText(line, "blue")
    what = tc_.ColoredText(what, "red")
    message = tc_.ColoredText(message, "cyan")

    print(
        f"{tc_.ColoredText('*** ERROR ***', 'magenta')}\n"
        f"WHERE={module}.{function}@{line}\n"
        f"WHAT= {what}\n"
        f"HOW=  {message}",
        end=END_CHARACTER,
        file=TARGET,
    )


def BugException(message: str = None) -> Exception:
    #
    standard_msg = "INVALID RUNTIME CONTEXT; YOU MAY WANT TO CONTACT THE DEVELOPER"
    if message is None:
        message = standard_msg
    else:
        message = f"{message}: {standard_msg}"

    return RuntimeError(message)


def _Report(what: Optional[str], how: str, how_color: str = None) -> None:
    #
    if how_color is not None:
        how = tc_.ColoredText(how, how_color)

    if what is None:
        print(how, end=END_CHARACTER, file=TARGET)
    else:
        print(what + ": " + how, end=END_CHARACTER, file=TARGET)


if "PYTHONDEBUG" not in ENVIRONMENT:
    sy_.excepthook = ReportX
