# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for our CLI applications."""

import contextlib
import re

import pytest
from click.testing import CliRunner


@contextlib.contextmanager
def stdout_logging():
    # copy logging messages to std out

    import io
    import logging

    buf = io.StringIO()
    ch = logging.StreamHandler(buf)
    ch.setFormatter(logging.Formatter("%(message)s"))
    ch.setLevel(logging.INFO)
    logger = logging.getLogger("mednet")
    logger.addHandler(ch)
    yield buf
    logger.removeHandler(ch)


def _assert_exit_0(result):
    assert (
        result.exit_code == 0
    ), f"Exit code {result.exit_code} != 0 -- Output:\n{result.output}"


def _check_help(entry_point):
    runner = CliRunner()
    result = runner.invoke(entry_point, ["--help"])
    _assert_exit_0(result)
    assert result.output.startswith("Usage:")


@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_config_describe_drive():
    from mednet.scripts.config import describe

    runner = CliRunner()
    result = runner.invoke(describe, ["drive"])
    _assert_exit_0(result)
    assert (
        ":py:mod:`DRIVE database <mednet.data.segment.drive>` (default split)."
        in result.output
    )


@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_database_check():
    from mednet.scripts.database import check

    runner = CliRunner()
    result = runner.invoke(check, ["--verbose", "--limit=1", "drive"])
    _assert_exit_0(result)


def test_main_help():
    from mednet.scripts.segment.cli import segment

    _check_help(segment)


def _str_counter(substr, s):
    return sum(1 for _ in re.finditer(substr, s, re.MULTILINE))


def test_evaluate_help():
    from mednet.scripts.segment.evaluate import evaluate

    _check_help(evaluate)


def test_dump_annotations_help():
    from mednet.scripts.segment.dump_annotations import dump_annotations

    _check_help(dump_annotations)


def test_view_help():
    from mednet.scripts.segment.view import view

    _check_help(view)


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_train_lwnet_drive(session_tmp_path):
    from mednet.scripts.train import train
    from mednet.utils.checkpointer import (
        CHECKPOINT_EXTENSION,
        _get_checkpoint_from_alias,
    )

    runner = CliRunner()

    with stdout_logging() as buf:
        output_folder = session_tmp_path / "segmentation-standalone"
        result = runner.invoke(
            train,
            [
                "lwnet",
                "drive",
                "-vv",
                "--epochs=1",
                "--batch-size=1",
                f"--output-folder={str(output_folder)}",
            ],
        )
        _assert_exit_0(result)

        # asserts checkpoints are there, or raises FileNotFoundError
        last = _get_checkpoint_from_alias(output_folder, "periodic")
        assert last.name.endswith("epoch=0" + CHECKPOINT_EXTENSION)
        best = _get_checkpoint_from_alias(output_folder, "best")
        assert best.name.endswith("epoch=0" + CHECKPOINT_EXTENSION)

        assert len(list((output_folder / "logs").glob("events.out.tfevents.*"))) == 1
        assert (output_folder / "train.meta.json").exists()

        keywords = {
            r"^Writing run metadata at .*$": 1,
            r"^Loading dataset:`train` without caching. Trade-off: CPU RAM usage: less | Disk I/O: more.$": 1,
            r"^Training for at most 1 epochs.$": 1,
            r"^Uninitialised lwnet model - computing z-norm factors from train dataloader.$": 1,
            r"^Dataset `train` is already setup. Not re-instantiating it.$": 3,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_predict_lwnet_drive(session_tmp_path):
    from mednet.scripts.predict import predict
    from mednet.utils.checkpointer import (
        CHECKPOINT_EXTENSION,
        _get_checkpoint_from_alias,
    )

    runner = CliRunner()

    with stdout_logging() as buf:
        output_folder = session_tmp_path / "segmentation-standalone"
        last_ckpt = _get_checkpoint_from_alias(output_folder, "periodic")
        assert last_ckpt.name.endswith("epoch=0" + CHECKPOINT_EXTENSION)
        result = runner.invoke(
            predict,
            [
                "lwnet",
                "drive",
                "-vv",
                "--batch-size=1",
                f"--weight={str(last_ckpt)}",
                f"--output-folder={str(output_folder)}",
            ],
        )
        _assert_exit_0(result)

        assert (output_folder / "predictions.meta.json").exists()
        assert (output_folder / "predictions.json").exists()

        keywords = {
            r"^Writing run metadata at .*$": 1,
            r"^Loading dataset: * without caching. Trade-off: CPU RAM usage: less | Disk I/O: more$": 2,
            r"^Loading checkpoint from .*$": 1,
            r"^Restoring normalizer from checkpoint.$": 1,
            r"^Running prediction on `train` split...$": 1,
            r"^Running prediction on `test` split...$": 1,
            r"^Predictions saved to .*$": 1,
        }

        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_dump_annotations_lwnet_drive(session_tmp_path):
    from mednet.scripts.segment.dump_annotations import dump_annotations

    runner = CliRunner()

    with stdout_logging() as buf:
        output_folder = (
            session_tmp_path / "segmentation-standalone" / "second-annotator"
        )
        result = runner.invoke(
            dump_annotations,
            [
                "lwnet",
                "drive-2nd",
                "-vv",
                f"--output-folder={str(output_folder)}",
            ],
        )
        _assert_exit_0(result)

        assert (output_folder / "annotations.meta.json").exists()
        assert (output_folder / "annotations.json").exists()

        keywords = {
            r"^Writing run metadata at .*$": 1,
            r"^Loading dataset:.*$": 1,
            r"^Dumping annotations from split.*$": 1,
        }

        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_evaluate_lwnet_drive(session_tmp_path):
    from mednet.scripts.segment.evaluate import evaluate

    runner = CliRunner()

    with stdout_logging() as buf:
        output_folder = session_tmp_path / "segmentation-standalone"
        result = runner.invoke(
            evaluate,
            [
                "-vv",
                f"--predictions={str(output_folder / 'predictions.json')}",
                f"--output-folder={str(output_folder)}",
                "--threshold=test",
                f"--compare-annotator={str(output_folder / 'second-annotator' / 'annotations.json')}",
            ],
        )
        _assert_exit_0(result)

        assert (output_folder / "evaluation.json").exists()
        assert (output_folder / "evaluation.meta.json").exists()
        assert (output_folder / "evaluation.rst").exists()
        assert (output_folder / "evaluation.pdf").exists()

        keywords = {
            r"^Writing run metadata at .*$": 1,
            r"^Counting true/false positive/negatives at split.*$": 2,
            r"^Evaluating threshold on split .*$": 1,
            r"^Computing metrics on split .*$": 2,
            r"^Comparing 2nd. annotator using .*$": 1,
            r"^Saving evaluation results at .*$": 1,
            r"^Saving tabulated performance summary at .*$": 1,
            r"^Saving evaluation figures at .*$": 1,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_view_lwnet_drive(session_tmp_path):
    from mednet.scripts.segment.view import view

    runner = CliRunner()

    with stdout_logging() as buf:
        output_folder = session_tmp_path / "segmentation-standalone"
        result = runner.invoke(
            view,
            [
                "-vv",
                f"--predictions={str(output_folder / 'predictions.json')}",
                f"--output-folder={str(output_folder)}",
            ],
        )
        _assert_exit_0(result)

        assert len(list((output_folder / "training" / "images").glob("*.png"))) == 20
        assert len(list((output_folder / "test" / "images").glob("*.png"))) == 20

        keywords = {
            r"^Creating 20 visualisations for split.*$": 2,
            r"^Set --threshold.*$": 1,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_train_lwnet_drive_from_checkpoint(tmp_path):
    from mednet.scripts.train import train
    from mednet.utils.checkpointer import (
        CHECKPOINT_EXTENSION,
        _get_checkpoint_from_alias,
    )

    runner = CliRunner()

    result0 = runner.invoke(
        train,
        [
            "lwnet",
            "drive",
            "-vv",
            "--epochs=1",
            "--batch-size=1",
            f"--output-folder={str(tmp_path)}",
        ],
    )
    _assert_exit_0(result0)

    # asserts checkpoints are there, or raises FileNotFoundError
    last = _get_checkpoint_from_alias(tmp_path, "periodic")
    assert last.name.endswith("epoch=0" + CHECKPOINT_EXTENSION)
    best = _get_checkpoint_from_alias(tmp_path, "best")
    assert best.name.endswith("epoch=0" + CHECKPOINT_EXTENSION)

    assert (tmp_path / "train.meta.json").exists()
    assert len(list((tmp_path / "logs").glob("events.out.tfevents.*"))) == 1

    with stdout_logging() as buf:
        result = runner.invoke(
            train,
            [
                "lwnet",
                "drive",
                "-vv",
                "--epochs=2",
                "--batch-size=1",
                f"--output-folder={tmp_path}",
            ],
        )
        _assert_exit_0(result)

        # asserts checkpoints are there, or raises FileNotFoundError
        last = _get_checkpoint_from_alias(tmp_path, "periodic")
        assert last.name.endswith("epoch=1" + CHECKPOINT_EXTENSION)
        best = _get_checkpoint_from_alias(tmp_path, "best")

        assert (tmp_path / "train.meta.json").exists()
        assert len(list((tmp_path / "logs").glob("events.out.tfevents.*"))) == 2

        keywords = {
            r"^Writing run metadata at .*$": 1,
            r"^Loading dataset:`train` without caching. Trade-off: CPU RAM usage: less | Disk I/O: more.$": 1,
            r"^Training for at most 2 epochs.$": 1,
            r"^Resuming from epoch 0 \(checkpoint file: .*$": 1,
            r"^Dataset `train` is already setup. Not re-instantiating it.$": 3,
            r"^Restoring normalizer from checkpoint.$": 1,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_experiment(tmp_path):
    from mednet.scripts.experiment import experiment

    runner = CliRunner()

    num_epochs = 2
    result = runner.invoke(
        experiment,
        [
            "-vv",
            "lwnet",
            "drive",
            f"--epochs={num_epochs}",
            f"--output-folder={str(tmp_path)}",
        ],
    )
    _assert_exit_0(result)

    assert (tmp_path / "train.meta.json").exists()
    assert (tmp_path / f"model-at-epoch={num_epochs-1}.ckpt").exists()

    # Need to glob because we cannot be sure of the checkpoint with lowest validation loss
    assert len(list(tmp_path.glob("model-at-lowest-validation-loss-epoch=*.ckpt"))) == 1
    assert (tmp_path / "trainlog.pdf").exists()
    assert len(list((tmp_path / "logs").glob("events.out.tfevents.*"))) == 1
    assert (tmp_path / "predictions.json").exists()
    assert (tmp_path / "predictions.meta.json").exists()
    assert (tmp_path / "evaluation.json").exists()
    assert (tmp_path / "evaluation.meta.json").exists()
    assert (tmp_path / "evaluation.pdf").exists()
    assert (tmp_path / "evaluation.rst").exists()


@pytest.mark.skip_if_rc_var_not_set("datadir.drive")
def test_preprocess_drive(tmp_path):
    from mednet.scripts.preprocess import preprocess

    runner = CliRunner()

    with stdout_logging() as buf:
        result = runner.invoke(
            preprocess,
            [
                "-vv",
                "lwnet",
                "drive",
                "--limit=3",
                f"--output-folder={str(tmp_path)}",
            ],
        )
        _assert_exit_0(result)

        keywords = {
            r"^Loading dataset:.*$": 2,
            r"^training/images/.*\.tif: \[3, 512, 512\]@torch\.float32$": 3,
            r"^test/images/.*\.tif: \[3, 512, 512\]@torch\.float32$": 3,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )

        # there are only 58 samples with target = 1
        assert len(list(tmp_path.rglob("**/*.tif"))) == 6  # images
        assert len(list(tmp_path.rglob("**/*.gif"))) == 12  # targets and masks
