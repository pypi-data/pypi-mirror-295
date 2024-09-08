# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""ChestX-ray8: Hospital-scale Chest X-ray Database.

The database contains a total of 112'120 images. Image size for each X-ray is
1024 x 1024. One set of automatically generated mask annotations is available
for all images.

* Database references:

  * Original data: [CXR8-2017]_
  * Split reference: [GAAL-2020]_

.. important:: **Raw data organization**

    The CXR8_ base datadir, which you should configure following the
    :ref:`mednet.setup` instructions, must contain at least the following
    directories:

    - ``images/`` (directory containing the CXR images, in PNG format)
    - ``segmentations/`` (must contain masks downloaded from `CXR8-Annotations`_)

    The flag ``idiap_folder_structure`` makes the loader search for files
    named, e.g. ``images/00030621_006.png``, as
    ``images/00030/00030621_006.png`` (this is valid for both images and
    segmentation masks).

* Raw data input (on disk):

  * PNG RGB 8-bit depth images
  * Resolution: 1024 x 1024 pixels
  * Total samples available: 112'120

* Output image:

  * Transforms:

    * Load raw PNG with :py:mod:`PIL`, with auto-conversion to RGB, convert to
      tensor
    * Labels for each of the lungs are read from the provided GIF files and
      merged into a single output image.

The ``default`` split contains 78'484 images for training, 11'212 images for
validation, and 22'424 images for testing.

This module contains the base declaration of common data modules and raw-data
loaders for this database. All configured splits inherit from this definition.
"""

import importlib.resources.abc
import os
import pathlib
import typing

import numpy as np
import PIL.Image
import torch
from torchvision import tv_tensors
from torchvision.transforms.v2.functional import to_dtype, to_image

from ...utils.rc import load_rc
from ..datamodule import CachingDataModule
from ..split import JSONDatabaseSplit
from ..typing import RawDataLoader as BaseDataLoader
from ..typing import Sample

DATABASE_SLUG = __name__.rsplit(".", 1)[-1]
"""Pythonic name to refer to this database."""

CONFIGURATION_KEY_DATADIR = "datadir." + DATABASE_SLUG
"""Key to search for in the configuration file for the root directory of this
database."""

CONFIGURATION_KEY_IDIAP_FILESTRUCTURE = DATABASE_SLUG + ".idiap_folder_structure"
"""Key to search for in the configuration file indicating if the loader should
use standard or idiap-based file organisation structure.

It causes the internal loader to search for files in a slightly different
folder structure, that was adapted to Idiap's requirements (number of files per
folder to be less than 10k).
"""


class RawDataLoader(BaseDataLoader):
    """A specialized raw-data-loader for the cxr8 dataset."""

    datadir: pathlib.Path
    """This variable contains the base directory where the database raw data is
    stored."""

    def __init__(self):
        self.datadir = pathlib.Path(
            load_rc().get(CONFIGURATION_KEY_DATADIR, os.path.realpath(os.curdir))
        )
        self.idiap_file_organisation = load_rc().get(
            CONFIGURATION_KEY_IDIAP_FILESTRUCTURE,
            False,
        )

    def sample(self, sample: typing.Any) -> Sample:
        """Load a single image sample from the disk.

        Parameters
        ----------
        sample
            A tuple containing path suffixes to the sample image, target, and mask
            to be loaded, within the dataset root folder.

        Returns
        -------
            The sample representation.
        """

        file_path = pathlib.Path(sample[0])
        label_path = pathlib.Path(sample[1])

        if self.idiap_file_organisation:
            sample_parts = sample[0].split("/", 1)
            file_path = pathlib.Path(
                sample_parts[0] + "/" + sample_parts[1][:5] + "/" + sample_parts[1]
            )

            label_parts = sample[1].split("/", 1)
            label_path = pathlib.Path(
                pathlib.Path(
                    label_parts[0] + "/" + label_parts[1][:5] + "/" + label_parts[1]
                )
            )

        image = PIL.Image.open(self.datadir / file_path).convert(mode="RGB")
        image = to_dtype(to_image(image), torch.float32, scale=True)

        target = np.array(PIL.Image.open(self.datadir / label_path))
        target = np.where(target == 255, 0, target)
        target = PIL.Image.fromarray(np.array(target > 0))
        target = to_dtype(to_image(target), torch.float32, scale=True)

        image = tv_tensors.Image(image)
        target = tv_tensors.Mask(target)
        mask = tv_tensors.Mask(torch.ones_like(target))

        return dict(image=image, target=target, mask=mask, name=sample[0])


class DataModule(CachingDataModule):
    """ChestX-ray8: Hospital-scale Chest X-ray Database.

    Parameters
    ----------
    split_path
        Path or traversable (resource) with the JSON split description to load.
    """

    def __init__(self, split_path: pathlib.Path | importlib.resources.abc.Traversable):
        super().__init__(
            database_split=JSONDatabaseSplit(split_path),
            raw_data_loader=RawDataLoader(),
            database_name=DATABASE_SLUG,
            split_name=split_path.name.rsplit(".", 2)[0],
            task="segmentation",
        )
