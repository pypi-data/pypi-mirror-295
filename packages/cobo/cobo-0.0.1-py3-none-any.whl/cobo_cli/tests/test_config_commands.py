import logging
import os
import unittest

import click
from click.testing import CliRunner

from cobo_cli.commands import cli

logger = logging.getLogger(__name__)


class TestConfigCommands(unittest.TestCase):
    def setUp(self):
        logging.getLogger().setLevel(logging.DEBUG)

    def test_config_commands(self):
        runner = CliRunner()

        assert isinstance(cli, click.Group)
        with runner.isolated_filesystem():
            cwd = os.getcwd()
            env_file = f"{cwd}/.cobo_cli.env"
            result = runner.invoke(
                cli,
                [
                    "--enable-debug",
                    "--env-file",
                    env_file,
                    "config",
                    "set",
                    "num",
                    "100",
                ],
            )
            logger.info(f"command result: {result.output}")
            self.assertEqual(result.exit_code, 0)
            self.assertTrue("set num to 100 in the configuration file" in result.output)

            result = runner.invoke(
                cli, ["--enable-debug", "--env-file", env_file, "config", "get", "num"]
            )
            logger.info(f"command result: {result.output}")
            self.assertEqual(result.exit_code, 0)
            self.assertTrue("num=100" in result.output)

            result = runner.invoke(
                cli,
                ["--enable-debug", "--env-file", env_file, "config", "get", "number"],
            )
            logger.info(f"command result: {result.output}")
            self.assertEqual(result.exit_code, 0)
            self.assertTrue("number=None" in result.output)

            result = runner.invoke(
                cli,
                ["--enable-debug", "--env-file", env_file, "config", "unset", "num"],
            )
            logger.info(f"command result: {result.output}")
            self.assertEqual(result.exit_code, 0)
            self.assertTrue("num removed." in result.output)

            result = runner.invoke(
                cli, ["--enable-debug", "--env-file", env_file, "config", "get", "num"]
            )
            logger.info(f"command result: {result.output}")
            self.assertEqual(result.exit_code, 0)
            self.assertTrue("num=None" in result.output)
