import asyncio
import sys

import click
from exponent.commands.common import (
    create_chat,
    inside_ssh_session,
    redirect_to_login,
    start_client,
)
from exponent.commands.settings import use_settings
from exponent.commands.types import exponent_cli_group
from exponent.commands.utils import (
    ConnectionTracker,
    Spinner,
    launch_exponent_browser,
    print_exponent_message,
)
from exponent.core.config import Settings


@exponent_cli_group()
def run_cli() -> None:
    """Run AI-powered chat sessions."""
    pass


@run_cli.command()
@click.option(
    "--chat-id",
    help="ID of an existing chat session to reconnect",
    required=False,
)
@click.option(
    "--prompt",
    help="Start a chat with a given prompt.",
)
@click.option(
    "--benchmark",
    is_flag=True,
    help="Enable benchmarking mode",
)
@use_settings
def run(
    settings: Settings,
    chat_id: str | None = None,
    prompt: str | None = None,
    benchmark: bool = False,
) -> None:
    """Start or reconnect to an Exponent session."""
    if not settings.api_key:
        redirect_to_login(settings)
        return

    api_key = settings.api_key
    base_url = settings.base_url
    base_api_url = settings.base_api_url
    loop = asyncio.get_event_loop()
    chat_uuid = chat_id or loop.run_until_complete(create_chat(api_key, base_api_url))

    if chat_uuid is None:
        sys.exit(1)

    if (
        (not benchmark)
        and (not prompt)
        and (not inside_ssh_session())
        # If the user specified a chat ID, they probably don't want to re-launch the chat
        and (not chat_id)
    ):
        # Open the chat in the browser
        launch_exponent_browser(settings.environment, base_url, chat_uuid)

    print_exponent_message(base_url, chat_uuid)
    print()

    connection_tracker = ConnectionTracker()

    client_fut = loop.create_task(
        start_client(
            api_key,
            base_api_url,
            chat_uuid,
            prompt,
            benchmark,
            connection_tracker,
        )
    )

    conn_fut = loop.create_task(handle_connection_changes(connection_tracker))

    _, pending = loop.run_until_complete(
        asyncio.wait({client_fut, conn_fut}, return_when=asyncio.FIRST_COMPLETED)
    )

    print("Disconnected upon user request, shutting down...")

    for task in pending:
        task.cancel()


async def handle_connection_changes(connection_tracker: ConnectionTracker) -> None:
    try:
        async with asyncio.timeout(5):
            assert await connection_tracker.next_change()
    except TimeoutError:
        spinner = Spinner("Connecting...")
        spinner.show()
        assert await connection_tracker.next_change()
        spinner.hide()

    while True:
        assert not await connection_tracker.next_change()

        print("Disconnected...", end="")
        await asyncio.sleep(1)
        spinner = Spinner("Reconnecting...")
        spinner.show()
        assert await connection_tracker.next_change()
        spinner.hide()
        print("\x1b[1;32m✓ Reconnected", end="")
        sys.stdout.flush()
        await asyncio.sleep(1)
        print("\r\x1b[0m\x1b[2K", end="")
        sys.stdout.flush()
