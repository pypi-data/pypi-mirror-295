import logging
import os
from pathlib import Path

import click
from click import BadParameter

from cobo_cli.apps_commands import apps
from cobo_cli.config_commands import config
from cobo_cli.data.enums import EnvironmentType
from cobo_cli.data.objects import CommandContext
from cobo_cli.keys_commands import keys
from cobo_cli.login_commands import login
from cobo_cli.managers.env_manager import EnvManager

formatter = logging.Formatter("%(levelname)s\t%(asctime)s\t[%(name)s] %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[console_handler])


logger = logging.getLogger(__name__)


def _enumerate_env():
    """
    Return a path for the env file.
    """
    path = os.environ.get("COBO_ENV", f"{Path.home()}/.cobo/.env")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--enable-debug", is_flag=True, help="Enable debug mode.")
@click.option("--env", "-e", default="dev", help="Specify the environment used.")
@click.option(
    "--env-file", default=_enumerate_env(), help="Specify the dotenv file location."
)
@click.pass_context
def cli(ctx, enable_debug, env, env_file):
    env = env.lower()
    if env not in EnvironmentType.values():
        raise BadParameter(
            f"--env parameter must be in {EnvironmentType.values()}", ctx=ctx
        )
    logger.debug(f"MainCommand called with following parameters: {env}, {env_file}")
    ctx.ensure_object(CommandContext)
    ctx.obj.env_manager = EnvManager(env_file)
    ctx.obj.env = EnvironmentType(env)
    logger.debug(f"Command context obj: {ctx.obj}")

    logging.getLogger().setLevel(logging.DEBUG if enable_debug else logging.INFO)
    logger.debug(f"Debug mode enabled: {enable_debug}")


# 添加子命令
assert isinstance(config, click.Group)
cli.add_command(config)

assert isinstance(login, click.Group)
cli.add_command(login)

assert isinstance(keys, click.Group)
cli.add_command(keys)

assert isinstance(apps, click.Group)
cli.add_command(apps)

if __name__ == "__main__":
    cli()
