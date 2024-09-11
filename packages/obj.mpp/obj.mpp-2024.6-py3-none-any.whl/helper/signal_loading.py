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
import brick.signal.signal_loading as sl_
from brick.data.type import PathAsStr, array_t, path_h

import numpy as nmpy
import skimage.color as sc_
import skimage.io as io_


def NumpySignal(
    signal_path: path_h, vmap_path: path_h = None, mkpt_dim: int = None
) -> sl_.signal_details_t:
    """
    The argument mkpt_dim appears to be optional. It is so only because:
        - vmap_path has been put right after signal_path to gather together path-related arguments,
        - then mkpt_dim has been put after vmap_path,
        - but vmap_path is optional,
        - therefore mkpt_dim must be declared as optional.
    But mkpt_dim turly is mandatory.
    """
    if mkpt_dim is None:
        raise ValueError('Argument "mkpt_dim" is mandatory')

    sl_.CheckPathExtension(signal_path, ("npy", "npz"))
    signal = nmpy.load(signal_path)

    if vmap_path is None:
        validity_map = None
    else:
        validity_map = nmpy.load(vmap_path)
        if not isinstance(validity_map, array_t):
            keys = tuple(validity_map.keys())
            validity_map = validity_map[keys[0]]

        sl_.CheckValidityMap(validity_map, mkpt_dim)

    return signal, validity_map


def RawImage(
    image_path: path_h, vmap_path: path_h = None, mkpt_dim: int = None
) -> sl_.signal_details_t:
    """
    The argument mkpt_dim appears to be optional. It is so only because:
        - vmap_path has been put right after signal_path to gather together path-related arguments,
        - then mkpt_dim has been put after vmap_path,
        - but vmap_path is optional,
        - therefore mkpt_dim must be declared as optional.
    But mkpt_dim truly is mandatory.
    """
    if mkpt_dim is None:
        raise ValueError('Argument "mkpt_dim" is mandatory')

    image = _RawImage(image_path)
    sl_.CheckRawSignal(image, mkpt_dim)

    if vmap_path is None:
        validity_map = None
    else:
        validity_map = _RawImage(vmap_path)
        sl_.CheckValidityMap(validity_map, mkpt_dim)
        sl_.CheckRawSignalAndVMapCoherence(image, validity_map, mkpt_dim)

    return image, validity_map


def SingleChannelOfImage(
    image_path: path_h,
    vmap_path: path_h = None,
    mkpt_dim: int = None,
    channel: str = "gray",
) -> sl_.signal_details_t:
    """
    The argument mkpt_dim appears to be optional. It is so only because:
        - vmap_path has been put right after signal_path to gather together path-related arguments,
        - then mkpt_dim has been put after vmap_path,
        - but vmap_path is optional,
        - therefore mkpt_dim must be declared as optional.
    But mkpt_dim turly is mandatory.

    channel (case insensitive): gray, 0, 1, 2, R, G, B, H, S, V
    """
    image, validity_map = RawImage(image_path, vmap_path=vmap_path, mkpt_dim=mkpt_dim)

    if mkpt_dim != 2:
        raise ValueError(
            f"{mkpt_dim}{mg_.SEP}Invalid marked point dimension; "
            f"Must be 2 in this context"
        )

    if image.ndim == mkpt_dim + 1:
        if (nmpy.diff(image[:, :, :3], axis=2) == 0).all():
            image = image[:, :, 0]
            return image, validity_map

        channel_couple_lst = [(0, 1), (0, 2), (1, 2)]
        for idx, channel_couple in enumerate(channel_couple_lst):
            simultaneously_zero = (image[:, :, channel_couple[0]] == 0).all() and (
                image[:, :, channel_couple[1]] == 0
            ).all()
            if simultaneously_zero:
                image = image[:, :, {0, 1, 2}.difference(channel_couple)]
                return image, validity_map

        # Normally, channel is already a string, but 0, 1, 2 also works
        channel = channel.__str__().lower()

        if channel == "gray":  # ITU-R 601-2 luma transform
            image = (
                (
                    0.299 * image[:, :, 0]
                    + 0.587 * image[:, :, 1]
                    + 0.114 * image[:, :, 2]
                )
                .round()
                .astype(image.dtype)
            )
        elif channel in "012":
            image = image[:, :, int(channel)]
        elif channel in "rgb":
            image = image[:, :, int("rgb".find(channel))]
        elif channel in "hsv":
            normalized_image = image.astype(nmpy.float64)
            # noinspection PyArgumentList
            image_max = normalized_image.max()
            if image_max > 1.0:
                normalized_image /= image_max  # Normally never zero
            else:
                normalized_image = image
            hsv_image = sc_.rgb2hsv(normalized_image)
            image = hsv_image[:, :, int("hsv".find(channel))]
        else:
            raise ValueError(f"{channel}{mg_.SEP}Invalid channel specification")

    return image, validity_map


def _RawImage(image_path: path_h) -> array_t:
    #
    return io_.imread(PathAsStr(image_path))
