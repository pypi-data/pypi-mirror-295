import json

import click
from exponent.commands.common import (
    redirect_to_login,
    run_until_complete,
)
from exponent.commands.settings import use_settings
from exponent.commands.types import exponent_cli_group
from exponent.core.config import Settings, get_settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.cloud_config_queries import (
    CREATE_CLOUD_CONFIG_MUTATION,
    GET_CLOUD_CONFIGS_QUERY,
    UPDATE_CLOUD_CONFIG_MUTATION,
)
from exponent.core.graphql.get_chats_query import GET_CHATS_QUERY
from exponent.core.graphql.subscriptions import AUTHENTICATED_USER_SUBSCRIPTION


@exponent_cli_group()
def config_cli() -> None:
    """Manage Exponent configuration settings."""
    pass


@config_cli.command()
def config() -> None:
    """Display current Exponent configuration."""
    config_file_settings = get_settings().get_config_file_settings()

    click.secho(
        json.dumps(config_file_settings, indent=2),
        fg="green",
    )


@config_cli.command()
@click.option("--key", help="Your Exponent API Key")
@use_settings
def login(settings: Settings, key: str) -> None:
    """Log in to Exponent."""

    if not key:
        redirect_to_login(settings, "provided")
        return

    click.echo(f"Saving API Key to {settings.config_file_path}")

    if settings.api_key and settings.api_key != key:
        click.confirm("Detected existing API Key, continue? ", default=True, abort=True)

    settings.update_api_key(key)
    settings.write_settings_to_config_file()

    click.echo("API Key saved.")


@config_cli.command(hidden=True)
@use_settings
def get_chats(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        get_chats_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
        )
    )


@config_cli.command(hidden=True)
@use_settings
def get_authenticated_user(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        get_authenticated_user_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
        )
    )


async def get_chats_task(
    api_key: str,
    base_api_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url)
    result = await graphql_client.query(GET_CHATS_QUERY)
    click.echo(result)


async def get_authenticated_user_task(
    api_key: str,
    base_api_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url)
    async for it in graphql_client.subscribe(AUTHENTICATED_USER_SUBSCRIPTION):
        click.echo(it)


@config_cli.command(hidden=True)
@use_settings
def get_cloud_configs(
    settings: Settings,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        get_cloud_configs_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
        )
    )


async def get_cloud_configs_task(
    api_key: str,
    base_api_url: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url)
    result = await graphql_client.query(GET_CLOUD_CONFIGS_QUERY)
    click.echo(result)


@config_cli.command(hidden=True)
@click.option("--github-org-name", required=True, help="GitHub organization name")
@click.option("--github-repo-name", required=True, help="GitHub repository name")
@use_settings
def create_cloud_config(
    settings: Settings,
    github_org_name: str,
    github_repo_name: str,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        create_cloud_config_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            github_org_name=github_org_name,
            github_repo_name=github_repo_name,
        )
    )


async def create_cloud_config_task(
    api_key: str,
    base_api_url: str,
    github_org_name: str,
    github_repo_name: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url)
    variables = {
        "githubOrgName": github_org_name,
        "githubRepoName": github_repo_name,
    }
    result = await graphql_client.query(CREATE_CLOUD_CONFIG_MUTATION, variables)
    click.echo(result)


@config_cli.command(hidden=True)
@click.option("--cloud-config-uuid", required=True, help="Cloud config UUID")
@click.option("--github-org-name", required=True, help="GitHub organization name")
@click.option("--github-repo-name", required=True, help="GitHub repository name")
@use_settings
def update_cloud_config(
    settings: Settings,
    cloud_config_uuid: str,
    github_org_name: str,
    github_repo_name: str,
) -> None:
    if not settings.api_key:
        redirect_to_login(settings)
        return

    run_until_complete(
        update_cloud_config_task(
            api_key=settings.api_key,
            base_api_url=settings.base_api_url,
            cloud_config_uuid=cloud_config_uuid,
            github_org_name=github_org_name,
            github_repo_name=github_repo_name,
        )
    )


async def update_cloud_config_task(
    api_key: str,
    base_api_url: str,
    cloud_config_uuid: str,
    github_org_name: str,
    github_repo_name: str,
) -> None:
    graphql_client = GraphQLClient(api_key, base_api_url)
    variables = {
        "cloudConfigUuid": cloud_config_uuid,
        "githubOrgName": github_org_name,
        "githubRepoName": github_repo_name,
    }

    result = await graphql_client.query(UPDATE_CLOUD_CONFIG_MUTATION, variables)
    click.echo(result)
