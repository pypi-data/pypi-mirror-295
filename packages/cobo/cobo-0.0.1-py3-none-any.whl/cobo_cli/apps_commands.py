import logging
import os
import subprocess
from typing import Optional

import click
from click import BadParameter, Path
from git import Repo

from cobo_cli.client.portal_client import ApiResponse, PortalClient
from cobo_cli.data.constants import default_manifest_file
from cobo_cli.data.enums import EnvironmentType, Manifest
from cobo_cli.constants import FrameworkEnum
from cobo_cli.data.constants import constants
from cobo_cli.utils.common import download_file, extract_file

logger = logging.getLogger(__name__)


@click.group("apps")
@click.pass_context
def apps(ctx: click.Context):
    ...


@apps.command("create")
@click.option(
    "-f",
    "--framework",
    required=True,
    type=FrameworkEnum,
    help=f"We support {', '.join([l.value for l in FrameworkEnum])} for now",
)
@click.option(
    "-d",
    "--directory",
    required=True,
    type=Path(readable=True, writable=True, file_okay=False, dir_okay=True),
    help="Directory which need to clone to",
)
@click.pass_context
def create_repo(
    ctx: click.Context,
    framework: FrameworkEnum,
    directory: Optional[str] = None,
) -> None:
    """
    Clone example repository based on the provided framework
    """
    directory = directory or os.getcwd()
    if not directory.startswith("/"):
        directory = os.getcwd() + "/" + directory
    if os.path.isdir(directory) and os.listdir(directory):
        raise BadParameter("directory need to be empty", ctx=ctx)
    click.echo(
        f"framework - {framework}, repo - {framework.repo}"
    )
    if framework.repo.endswith(".git"):
        Repo.clone_from(framework.repo, directory)
    else:
        file_path = download_file(framework.repo)
        extract_file(file_path, directory)
        os.remove(file_path)
    manifest_path = f"{directory.rstrip('/')}/{default_manifest_file}"
    if os.path.exists(manifest_path):
        user_response = click.confirm(
            "Existing manifest.json. Are you going to use current manifest.json?",
        )
        if user_response:
            click.echo(f"Create success! {directory}")
            return
    try:
        manifest = Manifest.load()
    except ValueError as e:
        raise BadParameter(
            str(e),
            ctx=ctx
        )
    manifest.framework = framework.value
    manifest.save(manifest_path)
    click.echo(f"Create success! {directory}")


@apps.command("run")
@click.option(
    "-p",
    "--port",
    required=False,
    type=int,
    default=5000,
    help="Port which we will listen on",
)
@click.pass_context
def run_app(ctx: click.Context, port: int):
    if not os.path.isfile(f"./{default_manifest_file}"):
        raise BadParameter(
            f"The file {default_manifest_file} does not exist. please create and update it first.",
            ctx=ctx,
        )
    try:
        manifest = Manifest.load()
    except ValueError as e:
        raise BadParameter(
            str(e),
            ctx=ctx
        )
    try:
        framework = FrameworkEnum(manifest.framework)
    except ValueError:
        raise BadParameter(
            "Invalid framework in manifest.json.",
            ctx=ctx,
        )
    app_uuid = manifest.dev_app_id or ctx.obj.env.default_app_id
    if not app_uuid:
        raise BadParameter(
            "Invalid dev_app_id in manifest.json.",
            ctx=ctx,
        )
    client = PortalClient(
        ctx=ctx,
    )
    app_resp = client.get_app(app_uuid)
    if not app_resp or not app_resp.success:
        raise BadParameter(
            app_resp.exception.errorMessage or "Invalid dev_app_id in manifest.json.",
            ctx=ctx,
        )

    url = constants[f"BASE_URL_{ctx.obj.env.value.upper()}".rstrip("/")] + f"/apps/myApps/allApps/{app_uuid}"
    click.echo(f"Open {url} in browser")
    click.launch(url)
    run_command: str = framework.run_command
    subprocess_args = run_command.split(' ')
    if port is not None:
        subprocess_args = [*subprocess_args, '--port', f"{port}"]
    subprocess.call(subprocess_args)


@apps.command("publish")
@click.pass_context
def app_publish(
    ctx: click.Context,
) -> None:
    """
    Publish App to portal.
    """
    if not os.path.exists(default_manifest_file):
        raise BadParameter(
            f"The file {default_manifest_file} does not exist. please create and update it first.",
            ctx=ctx,
        )

    try:
        manifest = Manifest.load()
    except ValueError as e:
        raise BadParameter(
            str(e),
            ctx=ctx
        )
    env = ctx.obj.env

    try:
        manifest.validate_required_fields(default_manifest_file, env)
    except ValueError as e:
        raise BadParameter(
            str(e),
            ctx=ctx
        )
    if env in [EnvironmentType.DEVELOPMENT, EnvironmentType.SANDBOX, EnvironmentType.LOCAL]:
        if manifest.dev_app_id:
            raise BadParameter(
                f"The field dev_app_id already exists in {default_manifest_file}",
                ctx=ctx,
            )
    elif env == EnvironmentType.PRODUCTION:
        if not manifest.dev_app_id:
            raise BadParameter(
                f"The field dev_app_id is not exists in {default_manifest_file}",
                ctx=ctx,
            )
        if manifest.app_id:
            raise BadParameter(
                f"The field app_id already exists in {default_manifest_file}",
                ctx=ctx,
            )
    else:
        raise BadParameter(f"Not supported in {env.value} environment")
    client = PortalClient(
        ctx=ctx,
    )
    response: ApiResponse = client.publish_app(manifest.to_dict())
    if not response.result:
        raise Exception(
            f"App publish failed. error_message: {response.exception.errorMessage}, error_id: {response.exception.errorId}"
        )
    app_id = response.result.get("app_id")
    client_id = response.result.get("client_id")
    if env == EnvironmentType.PRODUCTION:
        manifest.app_id = app_id
        manifest.client_id = client_id
    else:
        manifest.dev_app_id = app_id
        manifest.dev_client_id = client_id

    manifest.save()
    click.echo(f"App published successfully with app_id: {app_id}")


@apps.command("update")
@click.pass_context
def app_update(
    ctx: click.Context,
) -> None:
    """
    Update App manifest.
    """

    if not os.path.exists(default_manifest_file):
        raise BadParameter(
            f"The file {default_manifest_file} does not exist. please create and update it first.",
            ctx=ctx,
        )
    env = ctx.obj.env

    try:
        manifest = Manifest.load()
    except ValueError as e:
        raise BadParameter(
            str(e),
            ctx=ctx
        )
    try:
        manifest.validate_required_fields(default_manifest_file, env)
    except ValueError as e:
        raise BadParameter(
            str(e),
            ctx=ctx
        )
    if not manifest.dev_app_id:
        raise BadParameter(
            f"The field dev_app_id does not exists in {default_manifest_file}", ctx=ctx
        )

    app_id = manifest.dev_app_id

    if env == EnvironmentType.PRODUCTION:
        if not manifest.app_id:
            raise BadParameter(
                "The field app_id does not exists in manifest.json", ctx=ctx
            )
        app_id = manifest.app_id

    client = PortalClient(
        ctx=ctx,
    )

    response = client.update_app(app_id, manifest.to_dict())
    if not response.result:
        raise Exception(
            f"App update failed. error_message: {response.exception.errorMessage}, error_id: {response.exception.errorId}"
        )

    client_id = response.result.get("client_id")
    if env == EnvironmentType.PRODUCTION:
        manifest.client_id = client_id
    else:
        manifest.dev_client_id = client_id
    manifest.save()
    click.echo(f"App updated successfully with app_id: {app_id}")


@apps.command("status")
@click.pass_context
def app_status(
    ctx: click.Context,
) -> None:
    """
    Get App status to portal.
    """
    if not os.path.exists(default_manifest_file):
        raise BadParameter(
            f"The file {default_manifest_file} does not exist. please create and update it first.",
            ctx=ctx,
        )
    env = ctx.obj.env

    try:
        manifest = Manifest.load()
    except ValueError as e:
        raise BadParameter(
            str(e),
            ctx=ctx
        )
    if not manifest.dev_app_id:
        raise BadParameter(
            f"The field dev_app_id does not exists in {default_manifest_file}", ctx=ctx
        )

    app_uuid = manifest.dev_app_id

    if env == EnvironmentType.PRODUCTION:
        app_uuid = manifest.app_id

    if not app_uuid:
        raise BadParameter(
            f"The field app_id does not exists in {default_manifest_file}", ctx=ctx
        )

    client = PortalClient(
        ctx=ctx,
    )
    response = client.get_status(app_uuid=app_uuid)
    if not response.result:
        raise Exception(
            f"Check app status failed. error_message: {response.exception.errorMessage}, error_id: {response.exception.errorId}"
        )

    status = response.result.get("status")

    click.echo(f"app_id: {app_uuid}, status: {status}")
