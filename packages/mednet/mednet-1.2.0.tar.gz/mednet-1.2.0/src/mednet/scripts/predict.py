# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pathlib

import clapper.click
import click
from clapper.logging import setup

from .click import ConfigCommand, PathOrURL

logger = setup(__name__.split(".")[0], format="%(levelname)s: %(message)s")


@click.command(
    entry_point_group="mednet.config",
    cls=ConfigCommand,
    epilog="""Examples:

1. Run prediction on an existing DataModule configuration:

   .. code:: sh

      mednet predict -vv lwnet drive --weight=path/to/model.ckpt --output-folder=path/to/predictions

2. Enable multi-processing data loading with 6 processes:

   .. code:: sh

      mednet predict -vv lwnet drive --parallel=6 --weight=path/to/model.ckpt --output-folder=path/to/predictions

""",
)
@click.option(
    "--output-folder",
    "-o",
    help="Directory in which to save predictions (created if does not exist)",
    required=True,
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        writable=True,
        path_type=pathlib.Path,
    ),
    default="results",
    show_default=True,
    cls=clapper.click.ResourceOption,
)
@click.option(
    "--model",
    "-m",
    help="""A lightning module instance implementing the network architecture
    (not the weights, necessarily) to be used for prediction.""",
    required=True,
    cls=clapper.click.ResourceOption,
)
@click.option(
    "--datamodule",
    "-d",
    help="""A lightning DataModule that will be asked for prediction data
    loaders. Typically, this includes all configured splits in a DataModule,
    however this is not a requirement.  A DataModule that returns a single
    dataloader for prediction (wrapped in a dictionary) is acceptable.""",
    required=True,
    cls=clapper.click.ResourceOption,
)
@click.option(
    "--batch-size",
    "-b",
    help="""Number of samples in every batch (this parameter affects memory
    requirements for the network).""",
    required=True,
    show_default=True,
    default=1,
    type=click.IntRange(min=1),
    cls=clapper.click.ResourceOption,
)
@click.option(
    "--device",
    "-d",
    help='A string indicating the device to use (e.g. "cpu" or "cuda:0")',
    show_default=True,
    required=True,
    default="cpu",
    cls=clapper.click.ResourceOption,
)
@click.option(
    "--weight",
    "-w",
    help="""Path or URL to pretrained model file (`.ckpt` extension),
    corresponding to the architecture set with `--model`.  Optionally, you may
    also pass a directory containing the result of a training session, in which
    case either the best (lowest validation) or latest model will be loaded.""",
    required=True,
    cls=clapper.click.ResourceOption,
    type=PathOrURL(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
@click.option(
    "--parallel",
    "-P",
    help="""Use multiprocessing for data loading: if set to -1 (default),
    disables multiprocessing data loading.  Set to 0 to enable as many data
    loading instances as processing cores available in the system.  Set to
    >= 1 to enable that many multiprocessing instances for data loading.""",
    type=click.IntRange(min=-1),
    show_default=True,
    required=True,
    default=-1,
    cls=clapper.click.ResourceOption,
)
@clapper.click.verbosity_option(
    logger=logger, cls=clapper.click.ResourceOption, expose_value=False
)
def predict(
    output_folder,
    model,
    datamodule,
    batch_size,
    device,
    weight,
    parallel,
    **_,
) -> None:  # numpydoc ignore=PR01
    """Run inference on input samples, using a pre-trained model."""

    from ..engine.device import DeviceManager
    from ..engine.trainer import validate_model_datamodule
    from ..scripts.utils import JSONable, save_json_metadata, save_json_with_backup
    from ..utils.checkpointer import get_checkpoint_to_run_inference

    validate_model_datamodule(model, datamodule)

    # sets-up the data module
    datamodule.batch_size = batch_size
    datamodule.parallel = parallel
    datamodule.model_transforms = list(model.model_transforms)

    datamodule.prepare_data()
    datamodule.setup(stage="predict")

    if isinstance(weight, pathlib.Path) and weight.is_dir():
        weight = get_checkpoint_to_run_inference(weight)

    logger.info(f"Loading checkpoint from `{weight}`...")
    model = type(model).load_from_checkpoint(weight, strict=False)

    device_manager = DeviceManager(device)

    save_json_metadata(
        output_file=output_folder / "predictions.meta.json",
        output_folder=output_folder,
        model=model,
        datamodule=datamodule,
        batch_size=batch_size,
        device=device,
        weight=weight,
        parallel=parallel,
    )

    predictions: JSONable = None
    match datamodule.task:
        case "classification":
            from ..engine.classify.predictor import run as run_classify

            logger.info(f"Running prediction for `{datamodule.task}` task...")
            predictions = run_classify(model, datamodule, device_manager)

        case "segmentation":
            from ..engine.segment.predictor import run as run_segment

            logger.info(f"Running prediction for `{datamodule.task}` task...")
            predictions = run_segment(model, datamodule, device_manager, output_folder)

        case _:
            raise click.BadParameter(
                f"Do not know how to handle `{datamodule.task}` task from "
                f"`{type(datamodule).__module__}.{type(datamodule).__name__}`"
            )

    predictions_file = output_folder / "predictions.json"
    save_json_with_backup(predictions_file, predictions)
    logger.info(f"Predictions saved to `{str(predictions_file)}`")
