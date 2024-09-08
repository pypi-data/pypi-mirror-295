# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

import mednet.config.classify.models.pasa as pasa_config
from mednet.utils.summary import summary


class Tester(unittest.TestCase):
    """Unit test for model architectures."""

    def test_summary_driu(self):
        model = pasa_config.model
        s, param = summary(model)
        self.assertIsInstance(s, str)
        self.assertIsInstance(param, int)
