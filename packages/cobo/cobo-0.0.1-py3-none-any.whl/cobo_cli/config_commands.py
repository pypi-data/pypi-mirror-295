import logging

import click

logger = logging.getLogger(__name__)


@click.group("config")
@click.pass_context
def config(ctx: click.Context):
    ...


@config.command("set")
@click.argument("key")
@click.argument("value")
@click.pass_context
def set_config(ctx, key, value):
    """Set a key-value pair in the configuration."""
    dotenv_path = ctx.obj.env_manager.set_config(key, value)
    click.echo(f"set {key} to {value} in the configuration file {dotenv_path}")


@config.command("get")
@click.argument("key", required=False)
@click.pass_context
def get_config(ctx, key):
    """Get a key-value pair in the configuration."""
    configurations = ctx.obj.env_manager.get_config(key, True)
    for key, value in configurations.items():
        click.echo(f"{key}={value}")


@config.command("unset")
@click.argument("key")
@click.pass_context
def unset_config(ctx, key):
    """Unset a key-value pair in the configuration."""
    removed, key_to_unset = ctx.obj.env_manager.unset_config(key)
    if removed:
        click.echo(f"{key_to_unset} removed.")
