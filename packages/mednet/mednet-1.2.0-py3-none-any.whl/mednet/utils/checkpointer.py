# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import pathlib
import re
import typing

logger = logging.getLogger(__name__)


CHECKPOINT_ALIASES = {
    "best": "model-at-lowest-validation-loss-{epoch}",
    "periodic": "model-at-{epoch}",
}
"""Standard paths where checkpoints may be (if produced with this
framework)."""

CHECKPOINT_EXTENSION = ".ckpt"


def _get_checkpoint_from_alias(
    path: pathlib.Path,
    alias: typing.Literal["best", "periodic"],
) -> pathlib.Path:
    """Get an existing checkpoint file path.

    This function can search for names matching the checkpoint alias "stem"
    (ie. the prefix), and then assumes a dash "-" and a number follows that
    prefix before the expected file extension.  The number is parsed and
    considred to be an epoch number.  The latest file (the file containing the
    highest epoch number) is returned.

    If only one file is present matching the alias characteristics, then it is
    returned.

    Parameters
    ----------
    path
        Folder in which may contain checkpoint.
    alias
        Can be one of "best" or "periodic".

    Returns
    -------
        Path to the requested checkpoint, or ``None``, if no checkpoint file
        matching specifications is found on the provided path.

    Raises
    ------
    FileNotFoundError
        In case it cannot find any file on the provided path matching the given
        specifications.
    """

    template = path / (CHECKPOINT_ALIASES[alias] + CHECKPOINT_EXTENSION)

    if template.exists():
        return template

    # otherwise, we see if we are looking for a template instead, in which case
    # we must pick the latest.
    assert "{epoch}" in str(
        template,
    ), f"Template `{str(template)}` does not contain the keyword `{{epoch}}`"

    pattern = re.compile(
        template.name.replace("{epoch}", r"epoch(?P<separator>=|-|_)(?P<epoch>\d+)"),
    )
    highest = -1
    separator = "="
    for f in template.parent.iterdir():
        match = pattern.match(f.name)
        if match is not None:
            value = int(match.group("epoch"))
            if value > highest:
                highest = value
                separator = match.group("separator")

    if highest != -1:
        return template.with_name(
            template.name.replace("{epoch}", f"epoch{separator}{highest}"),
        )

    raise FileNotFoundError(
        f"A file matching `{str(template)}` specifications was not found",
    )


def get_checkpoint_to_resume_training(
    path: pathlib.Path,
) -> pathlib.Path:
    """Return the best checkpoint file path to resume training from.

    Parameters
    ----------
    path
        The base directory containing either the "periodic" checkpoint to start
        the training session from.

    Returns
    -------
    pathlib.Path
        Path to a checkpoint file that exists on disk.

    Raises
    ------
    FileNotFoundError
        If none of the checkpoints can be found on the provided directory.
    """

    return _get_checkpoint_from_alias(path, "periodic")


def get_checkpoint_to_run_inference(
    path: pathlib.Path,
) -> pathlib.Path:
    """Return the best checkpoint file path to run inference with.

    Parameters
    ----------
    path
        The base directory containing either the "best", "last" or "periodic"
        checkpoint to start the training session from.

    Returns
    -------
    pathlib.Path
        Path to a checkpoint file that exists on disk.

    Raises
    ------
    FileNotFoundError
        If none of the checkpoints can be found on the provided directory.
    """

    try:
        return _get_checkpoint_from_alias(path, "best")
    except FileNotFoundError:
        logger.error(
            "Did not find lowest-validation-loss model to run inference "
            "from.  Trying to search for the last periodically saved model...",
        )

    return _get_checkpoint_from_alias(path, "periodic")
