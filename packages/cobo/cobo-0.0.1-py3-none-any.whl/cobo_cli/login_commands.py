import json
import logging
import time

import click
from click import BadParameter

from cobo_cli.data.constants import constants
from cobo_cli.managers.OrgTokenManager import OrgTokenManager
from cobo_cli.managers.UserTokenManager import UserTokenManager
from cobo_cli.utils.common import is_response_success

logger = logging.getLogger(__name__)


@click.group("login", invoke_without_command=True)
@click.option(
    "--user",
    "-u",
    "login_type",
    help="login action associated with user dimension. default login_type.",
    flag_value="user",
    default=True,
)
@click.option(
    "--org",
    "-o",
    "login_type",
    help="login action associated with org dimension.",
    flag_value="org",
)
@click.option(
    "--org-uuid", help="Specify the org id used for retrieve token.", required=False
)
@click.option("--refresh-token", is_flag=True, help="Refresh token.")
@click.pass_context
def login(ctx, login_type, org_uuid, refresh_token):
    logger.debug(
        f"login command called. login_type selected: {login_type}, org_uuid: {org_uuid}"
    )
    if ctx.invoked_subcommand is None:
        # 需要有 App 信息才可以获取 user 或者 org 的授权
        client_id = ctx.obj.env_manager.get_config("CLIENT_ID")
        app_key = ctx.obj.env_manager.get_config("APP_KEY")
        app_secret = ctx.obj.env_manager.get_config("APP_SECRET")

        api_host = constants.get(f"API_HOST_{ctx.obj.env.value.upper()}")
        if login_type == "user":
            # 发起 user 授权请求
            body = UserTokenManager.init_auth(api_host)
            if not is_response_success(body, stdout=True):
                return
            result = body.get("result", {})
            browser_url = result.get("browser_url")
            token_url = result.get("token_url")
            code = result.get("code")

            click.echo(f"browser_url: {browser_url}")
            click.echo(f"token_url: {token_url}")
            click.echo(f"code: {code}")
            user_response = click.confirm(
                "Do you want to open the browser to continue the authorization process?"
            )
            if user_response:
                click.launch(f"{browser_url}")
                click.echo("Opening the browser...")

            # 轮询获取 user token
            click.echo("Polling the token URL for the granted token...")
            access_token = None
            for i in range(180):
                body = UserTokenManager.get_user_token(token_url)
                access_token = body.get("access_token")
                if access_token:
                    ctx.obj.env_manager.set_config("USER_ACCESS_TOKEN", access_token)
                    click.echo(
                        f"Got token for user token: {access_token} on cobo cli, "
                        f"saved to env file by using key: USER_ACCESS_TOKEN"
                    )
                    break
                time.sleep(1)
            if not access_token:
                click.echo("Login failed, please retry.")

        if login_type == "org":
            if not org_uuid:
                raise BadParameter(
                    "--org-uuid must be provided for retrieve org token", ctx=ctx
                )

            try:
                if refresh_token:
                    env_token_str = ctx.obj.env_manager.get_config(
                        f"ORG_TOKEN_{org_uuid}"
                    )
                    if not env_token_str:
                        raise BadParameter("No refresh token found.", ctx=ctx)
                    env_token_dict = json.loads(env_token_str)
                    token_obj = OrgTokenManager.refresh_token(
                        api_host,
                        client_id,
                        app_key,
                        app_secret,
                        org_uuid,
                        env_token_dict["refresh_token"],
                    )
                else:
                    token_obj = OrgTokenManager.get_token(
                        api_host, client_id, app_key, app_secret, org_uuid
                    )
                if not token_obj:
                    raise Exception("no token fetched, please check.")
                if token_obj.get("error"):
                    raise Exception(
                        token_obj["error"] + ", " + token_obj.get("error_description")
                    )
                ctx.obj.env_manager.set_config(
                    f"ORG_TOKEN_{org_uuid}", json.dumps(token_obj)
                )
                click.echo(
                    f"Got token for org {org_uuid}, saved to env file by using key: ORG_TOKEN_{org_uuid}"
                )
            except Exception as e:
                click.echo(f"{e}", err=True)
