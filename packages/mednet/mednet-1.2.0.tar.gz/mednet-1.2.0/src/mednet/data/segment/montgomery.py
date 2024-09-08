# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Montgomery database for lung segmentation.

The standard digital image database for Tuberculosis was created by the National
Library of Medicine, Maryland, USA in collaboration with Shenzhen No.3 People’s
Hospital, Guangdong Medical College, Shenzhen, China. The Chest X-rays are from

* Database reference: [MONTGOMERY-SHENZHEN-2014]_, [GAAL-2020]_
* Original resolution (height x width or width x height): 4020x4892 px or
  4892x4020 px

Data specifications:

* Raw data input (on disk):

  * PNG images 8 bit grayscale issued from digital radiography machines
  * Original resolution (height x width or width x height): 4020x4892 px or
    4892x4020 px
  * Samples: 138 images and associated labels

* Output image:

  * Transforms:

    * Load raw PNG with :py:mod:`PIL`
    * Convert to torch tensor

  * Final specifications

    * image: Grayscale, encoded as a single plane tensor, 32-bit floats,
      original size.
    * target: A binary mask containing ones where lungs are in the original
      image, otherwise, zeroes.
    * mask: Binary, with all ones (no specific mask)

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


class RawDataLoader(BaseDataLoader):
    """A specialized raw-data-loader for the Montgomery dataset."""

    datadir: pathlib.Path
    """This variable contains the base directory where the database raw data is
    stored."""

    def __init__(self):
        self.datadir = pathlib.Path(
            load_rc().get(CONFIGURATION_KEY_DATADIR, os.path.realpath(os.curdir))
        )

    def sample(self, sample: typing.Any) -> Sample:
        """Load a single image sample from the disk.

        Parameters
        ----------
        sample
            A tuple containing the path suffix, within the dataset root folder,
            where to find the image to be loaded, and an integer, representing the
            sample label.

        Returns
        -------
            The sample representation.
        """

        image = PIL.Image.open(self.datadir / sample[0]).convert(mode="RGB")
        image = to_dtype(to_image(image), torch.float32, scale=True)

        # Combines left and right lung masks into a single tensor
        left = PIL.Image.open(self.datadir / sample[1]).convert(mode="1", dither=None)
        right = PIL.Image.open(self.datadir / sample[2]).convert(mode="1", dither=None)
        target = np.ma.mask_or(np.asarray(left), np.asarray(right))
        target = to_dtype(to_image(target), torch.float32, scale=True)

        mask = torch.ones_like(target)

        image = tv_tensors.Image(image)
        target = tv_tensors.Mask(target)
        mask = tv_tensors.Mask(mask)

        return dict(image=image, target=target, mask=mask, name=sample[0])


class DataModule(CachingDataModule):
    """Montgomery database for lung segmentation.

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
