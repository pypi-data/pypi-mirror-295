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


@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_config_describe_montgomery():
    from mednet.scripts.config import describe

    runner = CliRunner()
    result = runner.invoke(describe, ["montgomery"])
    _assert_exit_0(result)
    assert (
        ":py:mod:`Montgomery database <mednet.data.classify.montgomery>` (default split)."
        in result.output
    )


@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_database_check():
    from mednet.scripts.database import check

    runner = CliRunner()
    result = runner.invoke(check, ["--verbose", "--limit=1", "montgomery"])
    _assert_exit_0(result)


def test_main_help():
    from mednet.scripts.classify.cli import classify

    _check_help(classify)


def _str_counter(substr, s):
    return sum(1 for _ in re.finditer(substr, s, re.MULTILINE))


def test_evaluate_help():
    from mednet.scripts.classify.evaluate import evaluate

    _check_help(evaluate)


def test_saliency_generate_help():
    from mednet.scripts.classify.saliency.generate import generate

    _check_help(generate)


def test_saliency_completeness_help():
    from mednet.scripts.classify.saliency.completeness import (
        completeness,
    )

    _check_help(completeness)


def test_saliency_view_help():
    from mednet.scripts.classify.saliency.view import view

    _check_help(view)


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_train_pasa_montgomery(session_tmp_path):
    from mednet.scripts.train import train
    from mednet.utils.checkpointer import (
        CHECKPOINT_EXTENSION,
        _get_checkpoint_from_alias,
    )

    runner = CliRunner()

    with stdout_logging() as buf:
        output_folder = session_tmp_path / "classification-standalone"
        result = runner.invoke(
            train,
            [
                "pasa",
                "montgomery",
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
            r"^Loading dataset:`validation` without caching. Trade-off: CPU RAM usage: less | Disk I/O: more.$": 1,
            r"^Applying train/valid loss balancing...$": 1,
            r"^Training for at most 1 epochs.$": 1,
            r"^Uninitialised pasa model - computing z-norm factors from train dataloader.$": 1,
            r"^Dataset `train` is already setup. Not re-instantiating it.$": 1,
            r"^Dataset `validation` is already setup. Not re-instantiating it.$": 1,
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
@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_predict_pasa_montgomery(session_tmp_path):
    from mednet.scripts.predict import predict
    from mednet.utils.checkpointer import (
        CHECKPOINT_EXTENSION,
        _get_checkpoint_from_alias,
    )

    runner = CliRunner()

    with stdout_logging() as buf:
        output_folder = session_tmp_path / "classification-standalone"
        last = _get_checkpoint_from_alias(output_folder, "periodic")
        assert last.name.endswith("epoch=0" + CHECKPOINT_EXTENSION)
        result = runner.invoke(
            predict,
            [
                "pasa",
                "montgomery",
                "-vv",
                "--batch-size=1",
                f"--weight={str(last)}",
                f"--output-folder={str(output_folder)}",
            ],
        )
        _assert_exit_0(result)

        assert (output_folder / "predictions.meta.json").exists()
        assert (output_folder / "predictions.json").exists()

        keywords = {
            r"^Writing run metadata at .*$": 1,
            r"^Loading dataset: * without caching. Trade-off: CPU RAM usage: less | Disk I/O: more$": 3,
            r"^Loading checkpoint from .*$": 1,
            r"^Restoring normalizer from checkpoint.$": 1,
            r"^Running prediction on `train` split...$": 1,
            r"^Running prediction on `validation` split...$": 1,
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
@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_evaluate_pasa_montgomery(session_tmp_path):
    from mednet.scripts.classify.evaluate import evaluate

    runner = CliRunner()

    with stdout_logging() as buf:
        output_folder = session_tmp_path / "classification-standalone"
        result = runner.invoke(
            evaluate,
            [
                "-vv",
                f"--predictions={str(output_folder / 'predictions.json')}",
                f"--output-folder={str(output_folder)}",
                "--threshold=test",
                "--credible-regions",
            ],
        )
        _assert_exit_0(result)

        assert (output_folder / "evaluation.json").exists()
        assert (output_folder / "evaluation.meta.json").exists()
        assert (output_folder / "evaluation.rst").exists()
        assert (output_folder / "evaluation.pdf").exists()

        keywords = {
            r"^Writing run metadata at .*$": 1,
            r"^Setting --threshold=.*$": 1,
            r"^Computing performance on split .*...$": 3,
            r"^Computing credible regions for metrics on split .*": 3,
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
@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_saliency_generation_pasa_montgomery(session_tmp_path):
    from mednet.scripts.classify.saliency.generate import generate
    from mednet.utils.checkpointer import (
        CHECKPOINT_EXTENSION,
        _get_checkpoint_from_alias,
    )

    runner = CliRunner()

    with stdout_logging() as buf:
        saliency_algo = "gradcam"
        input_folder = session_tmp_path / "classification-standalone"
        last = _get_checkpoint_from_alias(input_folder, "periodic")
        output_folder = input_folder / saliency_algo
        assert last.name.endswith("epoch=0" + CHECKPOINT_EXTENSION)
        result = runner.invoke(
            generate,
            [
                "-vv",
                "pasa",
                "montgomery",
                f"--saliency-map-algorithm={saliency_algo}",
                f"--weight={str(last)}",
                f"--output-folder={str(output_folder)}",
            ],
        )
        _assert_exit_0(result)

        assert (output_folder / "generation.meta.json").exists()

        keywords = {
            r"^Writing run metadata at .*$": 1,
            r"^Loading dataset:.*$": 3,
            r"^Generating saliency maps for dataset .*$": 3,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )

        assert len(list(output_folder.rglob("**/*.npy"))) == 138


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_saliency_view_pasa_montgomery(session_tmp_path):
    from mednet.scripts.classify.saliency.view import view

    runner = CliRunner()

    with stdout_logging() as buf:
        input_folder = session_tmp_path / "classification-standalone" / "gradcam"
        output_folder = input_folder / "view"
        result = runner.invoke(
            view,
            [
                "-vv",
                "pasa",
                "montgomery",
                f"--input-folder={str(input_folder)}",
                f"--output-folder={str(output_folder)}",
            ],
        )
        _assert_exit_0(result)

        assert (output_folder / "view.meta.json").exists()

        keywords = {
            r"^Writing run metadata at .*$": 1,
            r"^Loading dataset:.*$": 3,
            r"^Generating visualizations for samples \(target = 1\) at dataset .*$": 3,
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
        assert len(list(output_folder.rglob("**/*.png"))) == 58


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_train_pasa_montgomery_from_checkpoint(tmp_path):
    from mednet.scripts.train import train
    from mednet.utils.checkpointer import (
        CHECKPOINT_EXTENSION,
        _get_checkpoint_from_alias,
    )

    runner = CliRunner()

    result0 = runner.invoke(
        train,
        [
            "pasa",
            "montgomery",
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
                "pasa",
                "montgomery",
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
            r"^Loading dataset:`train` without caching. Trade-off: CPU RAM usage: less | Disk I/O: more.$": 1,
            r"^Loading dataset:`validation` without caching. Trade-off: CPU RAM usage: less | Disk I/O: more.$": 1,
            r"^Applying train/valid loss balancing...$": 1,
            r"^Training for at most 2 epochs.$": 1,
            r"^Resuming from epoch 0 \(checkpoint file: .*$": 1,
            r"^Writing run metadata at.*$": 1,
            r"^Dataset `train` is already setup. Not re-instantiating it.$": 1,
            r"^Dataset `validation` is already setup. Not re-instantiating it.$": 1,
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
@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_experiment(tmp_path):
    from mednet.scripts.experiment import experiment

    runner = CliRunner()

    num_epochs = 2
    result = runner.invoke(
        experiment,
        [
            "-vv",
            "pasa",
            "montgomery",
            f"--epochs={num_epochs}",
            f"--output-folder={str(tmp_path)}",
        ],
    )
    _assert_exit_0(result)

    assert (tmp_path / "train.meta.json").exists()
    assert (tmp_path / f"model-at-epoch={num_epochs-1}.ckpt").exists()
    assert (tmp_path / "predictions.json").exists()
    assert (tmp_path / "predictions.meta.json").exists()

    # Need to glob because we cannot be sure of the checkpoint with lowest validation loss
    assert (
        len(list((tmp_path).glob("model-at-lowest-validation-loss-epoch=*.ckpt"))) == 1
    )
    assert (tmp_path / "trainlog.pdf").exists()
    assert len(list((tmp_path / "logs").glob("events.out.tfevents.*"))) == 1
    assert (tmp_path / "evaluation.json").exists()
    assert (tmp_path / "evaluation.meta.json").exists()
    assert (tmp_path / "evaluation.rst").exists()
    assert (tmp_path / "evaluation.pdf").exists()


@pytest.mark.skip_if_rc_var_not_set("datadir.montgomery")
def test_preprocess_montgomery(tmp_path):
    from mednet.scripts.preprocess import preprocess

    runner = CliRunner()

    with stdout_logging() as buf:
        result = runner.invoke(
            preprocess,
            [
                "-vv",
                "pasa",
                "montgomery",
                "--limit=3",
                f"--output-folder={str(tmp_path)}",
            ],
        )
        _assert_exit_0(result)

        keywords = {
            r"^Loading dataset:.*$": 3,
            r"^CXR_png/MCUCXR_.*\.png: \[1, 512, 512\]@torch\.float32$": 9,
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
        assert len(list(tmp_path.rglob("**/*.png"))) == 9


@pytest.mark.slow
@pytest.mark.skip_if_rc_var_not_set("datadir.cxr8")
def test_multilabel_experiment(tmp_path):
    from mednet.scripts.experiment import experiment

    runner = CliRunner()

    num_epochs = 2
    result = runner.invoke(
        experiment,
        [
            "-vv",
            "pasa",
            "nih-cxr14-100",
            f"--epochs={num_epochs}",
            f"--output-folder={str(tmp_path)}",
            "--no-balance-classes",
        ],
    )
    _assert_exit_0(result)

    assert (tmp_path / "train.meta.json").exists()
    assert (tmp_path / f"model-at-epoch={num_epochs-1}.ckpt").exists()
    assert (tmp_path / "predictions.json").exists()
    assert (tmp_path / "predictions.meta.json").exists()

    # Need to glob because we cannot be sure of the checkpoint with lowest validation loss
    assert (
        len(list((tmp_path).glob("model-at-lowest-validation-loss-epoch=*.ckpt"))) == 1
    )
    assert (tmp_path / "trainlog.pdf").exists()
    assert len(list((tmp_path / "logs").glob("events.out.tfevents.*"))) == 1
    assert (tmp_path / "evaluation.json").exists()
    assert (tmp_path / "evaluation.meta.json").exists()
    assert (tmp_path / "evaluation.rst").exists()
    assert (tmp_path / "evaluation.pdf").exists()
