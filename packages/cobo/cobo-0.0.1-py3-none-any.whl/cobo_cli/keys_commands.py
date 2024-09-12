import logging

import click
from click import BadParameter

from cobo_cli.managers.keys_manager import KeysManager

logger = logging.getLogger(__name__)


@click.group("keys")
@click.pass_context
def keys(ctx):
    ...


@keys.command("generate")
@click.option("--key-type", default="API", help="Specify the key used for API or APP.")
@click.option("--alg", default="ed25519", help="Specify the key generation algorithm.")
@click.option("--force", is_flag=True, help="Force to replace existing keys.")
@click.pass_context
def generate(ctx, key_type: str, alg: str, force: bool):
    logger.debug(
        f"Generating keys using the following options, key_type: {key_type}, "
        f"algorithm: {alg}, force: {force}"
    )

    key_type = key_type.upper()
    if key_type not in ["API", "APP"]:
        raise BadParameter(
            "--key-type parameter must be either 'API' or 'APP'", ctx=ctx
        )

    alg = alg.lower()
    if alg not in ["ed25519"]:
        raise BadParameter("--alg parameter must be 'ed25519'", ctx=ctx)

    if ctx.obj.env_manager.get_config(f"{key_type}_KEY"):
        # 已经存在存储的 KEY ，则必须使用强制参数才可以生成新的。
        if not force:
            raise BadParameter(
                f"--force must be used when {key_type} key exists.", ctx=ctx
            )

    secret, pubkey = KeysManager.generate(alg)
    ctx.obj.env_manager.set_config(f"{key_type}_KEY", pubkey)
    ctx.obj.env_manager.set_config(f"{key_type}_SECRET", secret)
    click.echo(
        f"{key_type} key generation successful. Public key: {pubkey} and Secret are saved."
    )
