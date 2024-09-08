# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Define specialized data typing for classification tasks."""

import typing

import torch

from ..typing import RawDataLoader as BaseDataLoader


class RawDataLoader(BaseDataLoader):
    """A loader object can load samples and labels from storage for classification tasks."""

    def target(self, sample: typing.Any) -> torch.Tensor:
        """Load only sample target from its raw representation.

        Parameters
        ----------
        sample
            Information about the sample to load. Implementation dependent.

        Returns
        -------
            The label corresponding to the specified sample, encapsulated as a
            1D torch float tensor.
        """

        raise NotImplementedError("You must implement the `target()` method")
