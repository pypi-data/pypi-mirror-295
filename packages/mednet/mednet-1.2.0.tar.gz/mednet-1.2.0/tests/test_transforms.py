# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for transforms."""

import numpy
import PIL.Image
import torch
import torchvision.transforms.v2.functional as F  # noqa: N812

from mednet.data.augmentations import ElasticDeformation
from mednet.models.transforms import crop_image_to_mask


def test_crop_mask():
    original_tensor_size = (3, 50, 100)
    original_mask_size = (1, 50, 100)
    slice_ = (slice(None), slice(10, 30), slice(50, 70))

    tensor = torch.rand(original_tensor_size)
    mask = torch.zeros(original_mask_size)
    mask[slice_] = 1

    cropped_tensor = crop_image_to_mask(tensor, mask)

    assert cropped_tensor.shape == (3, 20, 20)
    assert torch.all(cropped_tensor.eq(tensor[slice_]))


def test_elastic_deformation(datadir):
    # Get a raw sample without deformation
    raw_without_deformation = PIL.Image.open(
        datadir / "raw_without_elastic_deformation.png"
    )
    raw_without_deformation = F.to_dtype(
        F.to_image(raw_without_deformation), torch.float32, scale=True
    )

    # Elastic deforms the raw
    numpy.random.seed(seed=100)
    ed = ElasticDeformation()
    raw_deformed = ed(raw_without_deformation)
    raw_deformed = F.to_pil_image(raw_deformed)
    # uncomment to save a new reference if required
    # raw_deformed.save(datadir / "raw_with_elastic_deformation.png")

    # Get the same sample already deformed (with seed=100)
    raw_2 = PIL.Image.open(datadir / "raw_with_elastic_deformation.png")
    raw_2 = F.to_pil_image(F.to_dtype(F.to_image(raw_2), torch.float32, scale=True))

    numpy.testing.assert_array_equal(numpy.asarray(raw_deformed), numpy.asarray(raw_2))
