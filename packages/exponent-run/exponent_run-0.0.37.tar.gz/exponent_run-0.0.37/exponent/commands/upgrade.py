import click
from exponent.commands.types import exponent_cli_group
from exponent.commands.utils import (
    check_exponent_version,
    get_exponent_version_for_update,
)
from exponent.version import get_version


@exponent_cli_group()
def upgrade_cli() -> None:
    """Manage Exponent version upgrades."""
    pass


@upgrade_cli.command()
@click.option(
    "--force", is_flag=True, help="Force upgrade even if no new version is available."
)
def upgrade(force: bool = False) -> None:
    """Upgrade Exponent to the latest version."""
    current_version = get_version()
    new_version = get_exponent_version_for_update()

    if new_version or force:
        click.echo(f"Current version: {current_version}")
        if new_version:
            click.echo(f"New version available: {new_version}")
        check_exponent_version()
    else:
        click.echo("Exponent is already up to date.")
