# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""`Little W-Net (LWNET) network architecture <lwnet_>`_, from [GALDRAN-2020]_.

It is based on two simple U-Nets with 3 layers concatenated to each other.  The
first U-Net produces a segmentation map that is used by the second to better
guide segmentation.
"""

import logging
import typing

import torch
import torch.nn

from ...data.typing import TransformSequence
from ..losses import MultiLayerBCELogitsLossWeightedPerBatch
from .model import Model

logger = logging.getLogger(__name__)


def _conv1x1(in_planes, out_planes, stride=1):
    return torch.nn.Conv2d(
        in_planes, out_planes, kernel_size=1, stride=stride, bias=False
    )


class ConvBlock(torch.nn.Module):
    """Convolution block.

    Parameters
    ----------
    in_c
        Number of input channels.
    out_c
        Number of output channels.
    k_sz
        Kernel Size.
    shortcut
        If True, adds a Conv2d layer.
    pool
        If True, adds a MaxPool2d layer.
    """

    def __init__(self, in_c, out_c, k_sz=3, shortcut=False, pool=True):
        super().__init__()
        if shortcut is True:
            self.shortcut = torch.nn.Sequential(
                _conv1x1(in_c, out_c), torch.nn.BatchNorm2d(out_c)
            )
        else:
            self.shortcut = None
        pad = (k_sz - 1) // 2

        block = []
        if pool:
            self.pool = torch.nn.MaxPool2d(kernel_size=2)
        else:
            self.pool = None

        block.append(torch.nn.Conv2d(in_c, out_c, kernel_size=k_sz, padding=pad))
        block.append(torch.nn.ReLU())
        block.append(torch.nn.BatchNorm2d(out_c))

        block.append(torch.nn.Conv2d(out_c, out_c, kernel_size=k_sz, padding=pad))
        block.append(torch.nn.ReLU())
        block.append(torch.nn.BatchNorm2d(out_c))

        self.block = torch.nn.Sequential(*block)

    def forward(self, x: torch.Tensor):
        if self.pool is not None:
            x = self.pool(x)
        out = self.block(x)
        if self.shortcut is not None:
            return out + self.shortcut(x)
        return out


class UpsampleBlock(torch.nn.Module):
    """Upsample block implementation.

    Parameters
    ----------
    in_c
        Number of input channels.
    out_c
        Number of output channels.
    up_mode
        Upsampling mode.
    """

    def __init__(self, in_c, out_c, up_mode="transp_conv"):
        super().__init__()
        block = []
        if up_mode == "transp_conv":
            block.append(torch.nn.ConvTranspose2d(in_c, out_c, kernel_size=2, stride=2))
        elif up_mode == "up_conv":
            block.append(
                torch.nn.Upsample(mode="bilinear", scale_factor=2, align_corners=False)
            )
            block.append(torch.nn.Conv2d(in_c, out_c, kernel_size=1))
        else:
            raise Exception("Upsampling mode not supported")

        self.block = torch.nn.Sequential(*block)

    def forward(self, x):
        return self.block(x)


class ConvBridgeBlock(torch.nn.Module):
    """ConvBridgeBlock implementation.

    Parameters
    ----------
    channels
        Number of channels.
    k_sz
        Kernel Size.
    """

    def __init__(self, channels, k_sz=3):
        super().__init__()
        pad = (k_sz - 1) // 2
        block = []

        block.append(torch.nn.Conv2d(channels, channels, kernel_size=k_sz, padding=pad))
        block.append(torch.nn.ReLU())
        block.append(torch.nn.BatchNorm2d(channels))

        self.block = torch.nn.Sequential(*block)

    def forward(self, x):
        return self.block(x)


class UpConvBlock(torch.nn.Module):
    """UpConvBlock implementation.

    Parameters
    ----------
    in_c
        Number of input channels.
    out_c
        Number of output channels.
    k_sz
        Kernel Size.
    up_mode
        Upsampling mode.
    conv_bridge
        If True, adds a ConvBridgeBlock layer.
    shortcut
        If True, adds a Conv2d layer.
    """

    def __init__(
        self,
        in_c,
        out_c,
        k_sz=3,
        up_mode="up_conv",
        conv_bridge=False,
        shortcut=False,
    ):
        super().__init__()
        self.conv_bridge = conv_bridge

        self.up_layer = UpsampleBlock(in_c, out_c, up_mode=up_mode)
        self.conv_layer = ConvBlock(
            2 * out_c, out_c, k_sz=k_sz, shortcut=shortcut, pool=False
        )
        if self.conv_bridge:
            self.conv_bridge_layer = ConvBridgeBlock(out_c, k_sz=k_sz)

    def forward(self, x, skip):
        up = self.up_layer(x)
        if self.conv_bridge:
            out = torch.cat([up, self.conv_bridge_layer(skip)], dim=1)
        else:
            out = torch.cat([up, skip], dim=1)
        return self.conv_layer(out)


class LittleUNet(torch.nn.Module):
    """Base little U-Net (LUNET) network architecture, from [GALDRAN-2020]_.

    Parameters
    ----------
    in_c
        Number of input channels.
    n_classes
        Number of outputs (classes) for this model.
    layers
        Number of layers of the model.
    k_sz
        Kernel Size.
    up_mode
        Upsampling mode.
    conv_bridge
        If True, adds a ConvBridgeBlock layer.
    shortcut
        If True, adds a Conv2d layer.
    """

    def __init__(
        self,
        in_c,
        n_classes,
        layers,
        k_sz=3,
        up_mode="transp_conv",
        conv_bridge=True,
        shortcut=True,
    ):
        super().__init__()
        self.n_classes = n_classes
        self.first = ConvBlock(
            in_c=in_c, out_c=layers[0], k_sz=k_sz, shortcut=shortcut, pool=False
        )

        self.down_path = torch.nn.ModuleList()
        for i in range(len(layers) - 1):
            block = ConvBlock(
                in_c=layers[i],
                out_c=layers[i + 1],
                k_sz=k_sz,
                shortcut=shortcut,
                pool=True,
            )
            self.down_path.append(block)

        self.up_path = torch.nn.ModuleList()
        reversed_layers = list(reversed(layers))
        for i in range(len(layers) - 1):
            block = UpConvBlock(
                in_c=reversed_layers[i],
                out_c=reversed_layers[i + 1],
                k_sz=k_sz,
                up_mode=up_mode,
                conv_bridge=conv_bridge,
                shortcut=shortcut,
            )
            self.up_path.append(block)

        # init, shamelessly lifted from torchvision/models/resnet.py
        for m in self.modules():
            if isinstance(m, torch.nn.Conv2d):
                torch.nn.init.kaiming_normal_(
                    m.weight, mode="fan_out", nonlinearity="relu"
                )
            elif isinstance(m, torch.nn.BatchNorm2d | torch.nn.GroupNorm):
                torch.nn.init.constant_(m.weight, 1)
                torch.nn.init.constant_(m.bias, 0)

        self.final = torch.nn.Conv2d(layers[0], n_classes, kernel_size=1)

    def forward(self, x):
        x = self.first(x)
        down_activations = []
        for i, down in enumerate(self.down_path):
            down_activations.append(x)
            x = down(x)
        down_activations.reverse()
        for i, up in enumerate(self.up_path):
            x = up(x, down_activations[i])
        return self.final(x)


class LittleWNet(Model):
    """`Little W-Net (LWNET) network architecture <lwnet_>`_, from [GALDRAN-2020]_.

    Concatenates two :py:class:`Little U-Net <LittleUNet>` models.

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
    num_classes
        Number of outputs (classes) for this model.
    """

    def __init__(
        self,
        loss_type: type[torch.nn.Module] = MultiLayerBCELogitsLossWeightedPerBatch,
        loss_arguments: dict[str, typing.Any] = {},
        optimizer_type: type[torch.optim.Optimizer] = torch.optim.Adam,
        optimizer_arguments: dict[str, typing.Any] = {},
        scheduler_type: type[torch.optim.lr_scheduler.LRScheduler] | None = None,
        scheduler_arguments: dict[str, typing.Any] = {},
        model_transforms: TransformSequence = [],
        augmentation_transforms: TransformSequence = [],
        num_classes: int = 1,
    ):
        super().__init__(
            name="lwnet",
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

        self.unet1 = LittleUNet(
            in_c=3,
            n_classes=self.num_classes,
            layers=(8, 16, 32),
            conv_bridge=True,
            shortcut=True,
        )
        self.unet2 = LittleUNet(
            in_c=3 + self.num_classes,
            n_classes=self.num_classes,
            layers=(8, 16, 32),
            conv_bridge=True,
            shortcut=True,
        )

    def forward(self, x):
        xn = self.normalizer(x)
        x1 = self.unet1(xn)
        x2 = self.unet2(torch.cat([xn, x1], dim=1))
        return x1, x2

    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        # prediction only returns the result of the last lunet
        return torch.sigmoid(self(batch["image"])[1])
