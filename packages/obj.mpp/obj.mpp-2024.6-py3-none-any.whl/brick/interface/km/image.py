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

from typing import Optional, Tuple

import numpy as nmpy

from brick.data.type import array_t
from brick.interface.km.library.pyqt5 import image_widget_t


class image_container_t(image_widget_t):
    #
    # Defining __slots__ makes Qt crash (or might be a bug with self.__class__.__slots__ on derived class)
    __slots__ = ("np_image",)

    # def __init__(self, parent: qw_.QWidget = None, image: array_t = None) -> None:
    #     #
    #     super().__init__(parent=parent)
    #     # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
    #     for slot in image_container_t.__slots__:
    #         setattr(self, slot, None)
    #
    #     if image is not None:
    #         self.SetImage(image)
    #     self.SetBackgroundRole(BASE_PALETTE)

    def SetImage(self, image: array_t) -> Optional[str]:
        #
        if image.ndim == 2:
            pass
        elif image.ndim == 3:
            if image.shape[2] not in (3, 4):
                # The 4th channel is assumed to be transparency
                return (
                    f"{self.__class__.__name__}: "
                    f"Accepts only single-channel, 3-channel and 3+alpha-channel images; "
                    f"Passed image has {image.shape[2]}"
                )
        else:
            return (
                f"{self.__class__.__name__}: Accepts only 2-D images; "
                f"Passed image is {image.ndim}-D"
            )

        self.np_image = image.copy()
        self.ResetImage()

        return None

    def ResetImage(self) -> None:
        """"""
        # No need to copy as it will automatically point to a new image below
        image = self.np_image
        if image.ndim == 2:
            rgb_image = nmpy.dstack((image, image, image))
        else:
            rgb_image = image[:, :, :3]
        img_min = nmpy.min(rgb_image)
        rgb_image = (255.0 / (nmpy.max(rgb_image) - img_min)) * (
            rgb_image.astype(nmpy.float64) - img_min
        )
        rgb_image = nmpy.rint(rgb_image).astype(nmpy.uint8)

        self.SetWidgetImage(rgb_image)

    def _RowColFromEventXY(self, evt_x: int, evt_y: int) -> Tuple[int, int]:
        #
        lengths = self.np_image.shape
        row = round(lengths[0] * evt_y / self.height())
        col = round(lengths[1] * evt_x / self.width())

        return row, col
