# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Definition of types related to models used in classification tasks."""

import typing

Prediction: typing.TypeAlias = tuple[str, typing.Sequence[int], typing.Sequence[float]]
"""The sample name, the target, and the predicted value."""

PredictionSplit: typing.TypeAlias = typing.Mapping[str, typing.Sequence[Prediction]]
"""A series of predictions for different database splits."""

SaliencyMapAlgorithm: typing.TypeAlias = typing.Literal[
    "ablationcam",
    "eigencam",
    "eigengradcam",
    "fullgrad",
    "gradcam",
    "gradcamelementwise",
    "gradcam++",
    "gradcamplusplus",
    "hirescam",
    "layercam",
    "randomcam",
    "scorecam",
    "xgradcam",
]
"""Supported saliency map algorithms."""
