# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""`DenseNet-121 network architecture <densenet-pytorch_>`_, from [DENSENET-2017]_."""

import logging
import typing

import torch
import torch.nn
import torch.optim.optimizer
import torch.utils.data
import torchvision.models as models

from ...data.typing import TransformSequence
from ..typing import Checkpoint
from .model import Model

logger = logging.getLogger(__name__)


class Densenet(Model):
    """`DenseNet-121 network architecture <densenet-pytorch_>`_, from [DENSENET-2017]_.

    Parameters
    ----------
    loss_type
        The loss to be used for training and evaluation.

        .. warning::

           The loss should be set to always return batch averages (as opposed
           to the batch sum), as our logging system expects it so.
    loss_arguments
        Arguments to the loss.
    optimizer_type
        The type of optimizer to use for training.
    optimizer_arguments
        Arguments to the optimizer after ``params``.
    scheduler_type
        The type of scheduler to use for training.
    scheduler_arguments
        Arguments to the scheduler after ``params``.
    model_transforms
        An optional sequence of torch modules containing transforms to be
        applied on the input **before** it is fed into the network.
    augmentation_transforms
        An optional sequence of torch modules containing transforms to be
        applied on the input **before** it is fed into the network.
    pretrained
        If set to True, loads pretrained model weights during initialization,
        else trains a new model.
    dropout
        Dropout rate after each dense layer.
    num_classes
        Number of outputs (classes) for this model.
    """

    def __init__(
        self,
        loss_type: type[torch.nn.Module] = torch.nn.BCEWithLogitsLoss,
        loss_arguments: dict[str, typing.Any] = {},
        optimizer_type: type[torch.optim.Optimizer] = torch.optim.Adam,
        optimizer_arguments: dict[str, typing.Any] = {},
        scheduler_type: type[torch.optim.lr_scheduler.LRScheduler] | None = None,
        scheduler_arguments: dict[str, typing.Any] = {},
        model_transforms: TransformSequence = [],
        augmentation_transforms: TransformSequence = [],
        pretrained: bool = False,
        dropout: float = 0.1,
        num_classes: int = 1,
    ):
        super().__init__(
            name="densenet",
            loss_type=loss_type,
            loss_arguments=loss_arguments,
            optimizer_type=optimizer_type,
            optimizer_arguments=optimizer_arguments,
            scheduler_type=scheduler_type,
            scheduler_arguments=scheduler_arguments,
            model_transforms=model_transforms,
            augmentation_transforms=augmentation_transforms,
            num_classes=num_classes,
        )

        self.pretrained = pretrained
        self.dropout = dropout

        # Load pretrained model
        if not self.pretrained:
            weights = None
        else:
            logger.info(f"Loading pretrained `{self.name}` model weights")
            weights = models.DenseNet121_Weights.DEFAULT

        self.model_ft = models.densenet121(weights=weights, drop_rate=self.dropout)

        # Adapts output features
        self.num_classes = num_classes

    @Model.num_classes.setter  # type: ignore[attr-defined]
    def num_classes(self, v: int) -> None:
        if self.model_ft.classifier.out_features != v:
            if self.pretrained:
                logger.info(
                    f"Resetting `{self.name}` pretrained classifier layer weights due "
                    f"to change in output size "
                    f"({self.model_ft.classifier.out_features} -> {v})"
                )
            self.model_ft.classifier = torch.nn.Linear(
                self.model_ft.classifier.in_features, v
            )
        self._num_classes = v

    def on_load_checkpoint(self, checkpoint: Checkpoint) -> None:
        num_classes = checkpoint["state_dict"]["model_ft.classifier.bias"].shape[0]

        if num_classes != self.num_classes:
            logger.debug(
                f"Resetting number-of-output-classes at `{self.name}` model from "
                f"{self.num_classes} to {num_classes} while loading checkpoint."
            )
        self.num_classes = num_classes

        super().on_load_checkpoint(checkpoint)

    def forward(self, x):
        x = self.normalizer(x)
        return self.model_ft(x)

    def set_normalizer(self, dataloader: torch.utils.data.DataLoader) -> None:
        """Initialize the normalizer for the current model.

        This function is NOOP if ``pretrained = True`` (normalizer set to
        imagenet weights, during contruction).

        Parameters
        ----------
        dataloader
            A torch Dataloader from which to compute the mean and std.
            Will not be used if the model is pretrained.
        """

        if self.pretrained:
            from ..normalizer import make_imagenet_normalizer

            logger.info(
                f"ImageNet pre-trained {self.name} model - NOT "
                f"computing z-norm factors from train dataloader. "
                f"Using preset factors from torchvision.",
            )
            self.normalizer = make_imagenet_normalizer()
        else:
            super().set_normalizer(dataloader)
