# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests for our CLI applications."""

import contextlib

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


def test_info_help():
    from mednet.scripts.info import info

    _check_help(info)


def test_info():
    from mednet.scripts.info import info

    runner = CliRunner()
    result = runner.invoke(info)
    _assert_exit_0(result)
    assert "platform:" in result.output
    assert "accelerators:" in result.output
    assert "version:" in result.output
    assert "databases:" in result.output
    assert "dependencies:" in result.output
    assert "python:" in result.output


def test_config_help():
    from mednet.scripts.config import config

    _check_help(config)


def test_config_list_help():
    from mednet.scripts.config import list_

    _check_help(list_)


def test_config_list():
    from mednet.scripts.config import list_

    runner = CliRunner()
    result = runner.invoke(list_)
    _assert_exit_0(result)
    assert "module: mednet.config.classify.data" in result.output
    assert "module: mednet.config.classify.models" in result.output
    assert "module: mednet.config.segment.data" in result.output
    assert "module: mednet.config.segment.models" in result.output


def test_config_list_v():
    from mednet.scripts.config import list_

    result = CliRunner().invoke(list_, ["--verbose"])
    _assert_exit_0(result)
    assert "module: mednet.config.classify.data" in result.output
    assert "module: mednet.config.classify.models" in result.output
    assert "module: mednet.config.segment.data" in result.output
    assert "module: mednet.config.segment.models" in result.output


def test_config_describe_help():
    from mednet.scripts.config import describe

    _check_help(describe)


def test_database_help():
    from mednet.scripts.database import database

    _check_help(database)


def test_database_list_help():
    from mednet.scripts.database import list_

    _check_help(list_)


def test_database_list():
    from mednet.scripts.database import list_

    runner = CliRunner()
    result = runner.invoke(list_)
    _assert_exit_0(result)
    assert result.output.startswith("  - ")


def test_database_check_help():
    from mednet.scripts.database import check

    _check_help(check)


def test_database_preprocess_help():
    from mednet.scripts.preprocess import preprocess

    _check_help(preprocess)


def test_train_help():
    from mednet.scripts.train import train

    _check_help(train)


def test_predict_help():
    from mednet.scripts.predict import predict

    _check_help(predict)


def test_experiment_help():
    from mednet.scripts.experiment import experiment

    _check_help(experiment)


def test_upload_help():
    from mednet.scripts.upload import upload

    _check_help(upload)
