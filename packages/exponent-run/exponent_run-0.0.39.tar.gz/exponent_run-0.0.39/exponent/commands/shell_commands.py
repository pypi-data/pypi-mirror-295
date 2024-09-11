import asyncio
import shutil
import sys
from collections.abc import Callable, Coroutine, Iterable
from concurrent.futures import Future
from typing import Any

import click
from exponent.commands.common import (
    create_chat,
    inside_ssh_session,
    redirect_to_login,
    start_client,
)
from exponent.commands.settings import use_settings
from exponent.commands.types import (
    StrategyChoice,
    StrategyOption,
    exponent_cli_group,
)
from exponent.commands.utils import (
    ConnectionTracker,
    Spinner,
    start_background_event_loop,
)
from exponent.core.config import Settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.mutations import HALT_CHAT_STREAM_MUTATION
from exponent.core.graphql.subscriptions import CHAT_EVENTS_SUBSCRIPTION
from exponent.core.remote_execution.exceptions import ExponentError
from exponent.core.types.generated.strategy_info import (
    ENABLED_STRATEGY_INFO_LIST,
)
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.syntax import Syntax

SLASH_COMMANDS = {
    "/help": "Show available commands",
    "/autorun": "Toggle autorun mode",
    "/web": "Move chat to a web browser",
}


@exponent_cli_group()
def shell_cli() -> None:
    pass


@shell_cli.command()
@click.option(
    "--model",
    help="LLM model",
    required=True,
    default="CLAUDE_3_POINT_5_SONNET",
)
@click.option(
    "--strategy",
    prompt=True,
    prompt_required=False,
    type=StrategyChoice(ENABLED_STRATEGY_INFO_LIST),
    cls=StrategyOption,
)
@click.option(
    "--autorun",
    is_flag=True,
    help="Enable autorun mode",
)
@click.option(
    "--prompt",
    help="Initial prompt",
)
@use_settings
def shell(
    settings: Settings,
    model: str,
    strategy: str,
    autorun: bool = False,
    prompt: str | None = None,
) -> None:
    """Start an Exponent session in your current shell."""

    if not settings.api_key:
        redirect_to_login(settings)
        return

    api_key = settings.api_key
    base_api_url = settings.base_api_url
    gql_client = GraphQLClient(api_key, base_api_url)
    loop = start_background_event_loop()

    chat_uuid = asyncio.run_coroutine_threadsafe(
        create_chat(api_key, base_api_url), loop
    ).result()

    if chat_uuid is None:
        sys.exit(1)

    connection_tracker = ConnectionTracker()

    client_fut = asyncio.run_coroutine_threadsafe(
        start_client(
            api_key, base_api_url, chat_uuid, connection_tracker=connection_tracker
        ),
        loop,
    )

    input_handler = InputHandler()
    chat = Chat(chat_uuid, settings.base_url, gql_client, model, strategy, autorun)
    shell = Shell(prompt, loop, input_handler, chat, connection_tracker)
    shell.run()
    client_fut.cancel()
    print("\rBye!")


def pause_spinner(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(self: "Chat", *args: Any, **kwargs: Any) -> Any:
        self.spinner.hide()
        result = func(self, *args, **kwargs)
        self.spinner.show()
        return result

    return wrapper


def stop_spinner(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(self: "Chat", *args: Any, **kwargs: Any) -> Any:
        self.spinner.hide()
        result = func(self, *args, **kwargs)
        return result

    return wrapper


class Chat:
    def __init__(  # noqa: PLR0913
        self,
        chat_uuid: str,
        base_url: str,
        gql_client: GraphQLClient,
        model: str,
        strategy: str,
        autorun: bool,
    ) -> None:
        self.chat_uuid = chat_uuid
        self.base_url = base_url
        self.gql_client = gql_client
        self.model = model
        self.strategy = strategy
        self.autorun = autorun
        self.parent_uuid: str | None = None
        self.block_row_offset = 0
        self.console = Console()
        self.code_block_uuid = None
        self.file_write_uuid = None
        self.command_uuid = None
        self.block: Block = NullBlock()
        self.default_spinner = Spinner("Exponent is working...")
        self.exec_spinner = Spinner(
            "Exponent is waiting for the code to finish running..."
        )
        self.spinner = self.default_spinner

    async def send_prompt(self, prompt: str) -> str | None:
        self.spinner.show()

        return await self.process_chat_subscription(
            {"prompt": {"message": prompt, "attachments": []}}
        )

    async def send_confirmation(self) -> str | None:
        if self.code_block_uuid is not None:
            return await self.process_chat_subscription(
                {
                    "codeBlockConfirmation": {
                        "accepted": True,
                        "codeBlockUuid": self.code_block_uuid,
                    }
                }
            )
        elif self.file_write_uuid is not None:
            return await self.process_chat_subscription(
                {
                    "fileWriteConfirmation": {
                        "accepted": True,
                        "fileWriteUuid": self.file_write_uuid,
                    }
                }
            )
        elif self.command_uuid is not None:
            return await self.process_chat_subscription(
                {
                    "commandConfirmation": {
                        "accepted": True,
                        "commandUuid": self.command_uuid,
                    }
                }
            )

        return None

    def toggle_autorun(self) -> bool:
        self.autorun = not self.autorun
        return self.autorun

    async def halt_stream(self) -> None:
        await self.gql_client.query(
            HALT_CHAT_STREAM_MUTATION, {"chatUuid": self.chat_uuid}, "HaltChatStream"
        )

    def url(self) -> str:
        return f"{self.base_url}/chats/{self.chat_uuid}"

    async def process_chat_subscription(  # noqa: PLR0912, PLR0915
        self,
        extra_vars: dict[str, Any],
    ) -> str | None:
        result = None

        vars = {
            "chatUuid": self.chat_uuid,
            "parentUuid": self.parent_uuid,
            "model": self.model,
            "strategyNameOverride": self.strategy,
            "useToolsConfig": "read_write",
            "requireConfirmation": not self.autorun,
        }

        vars.update(extra_vars)
        self.code_block_uuid = None
        self.file_write_uuid = None
        self.command_uuid = None

        async for response in self.gql_client.subscribe(CHAT_EVENTS_SUBSCRIPTION, vars):
            event = response["authenticatedChat"]
            kind = event["__typename"]

            self.parent_uuid = event.get("eventUuid") or self.parent_uuid

            if kind == "MessageChunkEvent":
                if event["role"] == "assistant":
                    self.handle_message_chunk_event(event)
            elif kind == "MessageEvent":
                if event["role"] == "assistant":
                    self.handle_message_event(event)
            elif kind == "FileWriteChunkEvent":
                self.handle_file_write_chunk_event(event)
            elif kind == "FileWriteEvent":
                self.handle_file_write_event(event)
            elif kind == "FileWriteConfirmationEvent":
                self.handle_file_write_confirmation_event(event)
            elif kind == "FileWriteStartEvent":
                self.handle_file_write_start_event(event)
            elif kind == "FileWriteResultEvent":
                self.handle_file_write_result_event(event)
            elif kind == "CodeBlockChunkEvent":
                self.handle_code_block_chunk_event(event)
            elif kind == "CodeBlockEvent":
                self.handle_code_block_event(event)
            elif kind == "CodeBlockConfirmationEvent":
                self.handle_code_block_confirmation_event(event)
            elif kind == "CodeExecutionStartEvent":
                self.handle_code_execution_start_event(event)
            elif kind == "CodeExecutionEvent":
                self.handle_code_execution_event(event)
            elif kind == "CommandChunkEvent":
                if event["data"]["type"] not in ["FILE_READ", "FILE_OPEN"]:
                    continue
                self.handle_command_chunk_event(event)
            elif kind == "CommandEvent":
                if event["data"]["type"] not in ["FILE_READ", "FILE_OPEN"]:
                    continue
                self.handle_command_event(event)
            elif kind == "CommandConfirmationEvent":
                self.handle_command_confirmation_event(event)
            elif kind == "CommandStartEvent":
                self.handle_command_start_event(event)
            elif kind == "CommandResultEvent":
                self.handle_command_result_event(event)
            elif kind == "Error":
                raise ExponentError(event["message"])
            else:
                # TODO
                pass

        self.spinner.hide()
        return result

    @stop_spinner
    def handle_message_chunk_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs = []

        if self.block.event_uuid != event_uuid:
            self.block = MessageBlock(event_uuid)

        assert isinstance(self.block, MessageBlock)

        seqs.append(self.block.render_message(event["content"]))
        render(seqs)

    @pause_spinner
    def handle_message_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs = []

        if self.block.event_uuid != event_uuid:
            self.block = MessageBlock(event_uuid)

        assert isinstance(self.block, MessageBlock)

        seqs.append(self.block.render_message(event["content"]))
        seqs.append(["\n\n"])
        render(seqs)

    @stop_spinner
    def handle_file_write_chunk_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs = []

        if self.block.event_uuid != event_uuid:
            self.block = FileWriteBlock(event_uuid, event["language"])

            seqs.append(
                [
                    self.render_block_header(f"Editing file {event['filePath']}"),
                    self.render_block_padding(),
                ]
            )

        assert isinstance(self.block, FileWriteBlock)

        seqs.append(self.block.render_content(event["content"]))
        render(seqs)

    @pause_spinner
    def handle_file_write_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs: list[Any] = []

        if self.block.event_uuid != event_uuid:
            self.block = FileWriteBlock(event_uuid, event["language"])

            seqs.append(
                [
                    self.render_block_header(f"Editing file {event['filePath']}"),
                    self.render_block_padding(),
                ]
            )

        assert isinstance(self.block, FileWriteBlock)

        seqs.append(self.block.render_content(event["content"]))
        seqs.append(self.render_block_padding())

        if event["requireConfirmation"]:
            self.file_write_uuid = event_uuid

            seqs.append(
                [
                    self.render_block_footer(
                        "Confirm edit with <C+y>. Sending a new message will dismiss code changes."
                    ),
                    "\n",
                ]
            )

        render(seqs)

    @pause_spinner
    def handle_file_write_confirmation_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid != event["fileWriteUuid"]:
            return

        assert isinstance(self.block, FileWriteBlock)

        seqs = []

        if event["accepted"]:
            seqs.append(
                [
                    move_cursor_up_seq(2),
                    self.render_block_footer("⚙️ Applying edit..."),
                    "\n",
                ]
            )
        else:
            # user entered new prompt, cursor moved down
            # therefore we need to move it up, redraw status, and move it
            # back where it was

            seqs.append(
                [
                    move_cursor_up_seq(4),
                    self.render_block_footer("✘ Edit dismissed"),
                    move_cursor_down_seq(3),
                ]
            )

        render(seqs)

    @pause_spinner
    def handle_file_write_start_event(self, event: dict[str, Any]) -> None:
        return

    @pause_spinner
    def handle_file_write_result_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid != event["fileWriteUuid"]:
            return

        assert isinstance(self.block, FileWriteBlock)

        seqs = []
        result = event["content"]

        seqs.append(
            [
                move_cursor_up_seq(2),
                self.render_block_footer(f"✔️ {result}" if result else "✔️ Edit applied"),
                move_cursor_down_seq(1),
            ]
        )

        render(seqs)

    @stop_spinner
    def handle_command_chunk_event(self, event: dict[str, Any]) -> None:
        type_ = event["data"]["type"].lower()
        event_uuid = event["eventUuid"]
        seqs = []

        if self.block.event_uuid != event_uuid:
            self.block = CommandBlock(event_uuid, type_, event["data"]["language"])

            seqs.append(
                [
                    self.render_block_header(type_),
                    self.render_block_padding(),
                ]
            )

        assert isinstance(self.block, CommandBlock)

        seqs.append(self.block.render_data(event["data"]))
        render(seqs)

    @pause_spinner
    def handle_command_event(self, event: dict[str, Any]) -> None:
        type_ = event["data"]["type"].lower()
        event_uuid = event["eventUuid"]
        seqs: list[Any] = []

        if self.block.event_uuid != event_uuid:
            self.block = CommandBlock(event_uuid, type_, event["data"]["language"])

            seqs.append(
                [
                    self.render_block_header(type_),
                    self.render_block_padding(),
                ]
            )

        assert isinstance(self.block, CommandBlock)

        seqs.append(self.block.render_data(event["data"]))
        seqs.append(self.render_block_padding())

        if event["requireConfirmation"]:
            self.command_uuid = event_uuid

            seqs.append(
                [
                    self.render_block_footer(
                        f"Confirm {type_} command with <C+y>. "
                        "Sending a new message will cancel this command."
                    ),
                    "\n",
                ]
            )

        render(seqs)

    @pause_spinner
    def handle_command_confirmation_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid != event["commandUuid"]:
            return

        assert isinstance(self.block, CommandBlock)

        seqs = []

        if event["accepted"]:
            seqs.append(
                [
                    move_cursor_up_seq(2),
                    self.render_block_footer(
                        f"⚙️ Executing {self.block.type} command..."
                    ),
                    "\n",
                ]
            )
        else:
            # user entered new prompt, cursor moved down
            # therefore we need to move it up, redraw status, and move it
            # back where it was

            seqs.append(
                [
                    move_cursor_up_seq(4),
                    self.render_block_footer(
                        f"✘ {self.block.type} command did not execute"
                    ),
                    move_cursor_down_seq(3),
                ]
            )

        render(seqs)

    @pause_spinner
    def handle_command_start_event(self, event: dict[str, Any]) -> None:
        return

    @pause_spinner
    def handle_command_result_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid != event["commandUuid"]:
            return

        assert isinstance(self.block, CommandBlock)

        seqs = []
        result = event["content"]
        result = pad_left(result.strip(), "  ")

        seqs.append(
            [
                move_cursor_up_seq(2),
                self.render_block_header("output"),
                self.render_block_padding(),
                self.block.highlight_code(result, self.block.lang, line_numbers=False),
                self.render_block_padding(),
                self.render_block_footer(f"✔️ {self.block.type} command executed"),
                move_cursor_down_seq(1),
            ]
        )

        render(seqs)

    @stop_spinner
    def handle_code_block_chunk_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs = []

        if self.block.event_uuid != event_uuid:
            self.block = CodeBlock(event_uuid, event["language"])

            seqs.append(
                [
                    self.render_block_header(event["language"]),
                    self.render_block_padding(),
                ]
            )

        assert isinstance(self.block, CodeBlock)

        seqs.append(self.block.render_code(event["content"]))
        render(seqs)

    @pause_spinner
    def handle_code_block_event(self, event: dict[str, Any]) -> None:
        event_uuid = event["eventUuid"]
        seqs: list[Any] = []

        if self.block.event_uuid != event_uuid:
            self.block = CodeBlock(event_uuid, event["language"])

            seqs.append(
                [
                    self.render_block_header(event["language"]),
                    self.render_block_padding(),
                ]
            )

        assert isinstance(self.block, CodeBlock)

        seqs.append(self.block.render_code(event["content"]))
        seqs.append(self.render_block_padding())

        if event["requireConfirmation"]:
            self.code_block_uuid = event_uuid

            seqs.append(
                [
                    self.render_block_footer(
                        "Run this code now with <C+y>. Sending a new message will cancel this request."
                    ),
                    "\n",
                ]
            )

        render(seqs)

    @pause_spinner
    def handle_code_block_confirmation_event(self, event: dict[str, Any]) -> None:
        if self.block.event_uuid != event["codeBlockUuid"]:
            return

        assert isinstance(self.block, CodeBlock)

        seqs = []

        if event["accepted"]:
            seqs.append(
                [
                    move_cursor_up_seq(2),
                    self.render_block_footer("⚙️ Running code..."),
                    "\n",
                ]
            )
        else:
            # user entered new prompt, cursor moved down
            # therefore we need to move it up, redraw status, and move it
            # back where it was

            seqs.append(
                [
                    move_cursor_up_seq(4),
                    self.render_block_footer("✘ Code did not execute"),
                    move_cursor_down_seq(3),
                ]
            )

        render(seqs)

    @pause_spinner
    def handle_code_execution_start_event(self, event: dict[str, Any]) -> None:
        self.spinner = self.exec_spinner

    @pause_spinner
    def handle_code_execution_event(self, event: dict[str, Any]) -> None:
        self.spinner = self.default_spinner

        if self.block.event_uuid != event["codeBlockUuid"]:
            return

        assert isinstance(self.block, CodeBlock)

        seqs = []
        lines = pad_left(event["content"].strip(), "  ").split("\n")
        output = [[block_body_bg_seq(), erase_line_seq(), line, "\n"] for line in lines]

        seqs.append(
            [
                move_cursor_up_seq(2),
                self.render_block_header("output"),
                self.render_block_padding(),
                output,
                self.render_block_padding(),
                move_cursor_down_seq(1),
            ]
        )

        render(seqs)

    def render_block_header(self, text: str) -> list[str]:
        return [
            block_header_bg_seq(),
            block_header_fg_seq(),
            erase_line_seq(),
            " " + text,
            reset_attrs_seq(),
            "\n",
        ]

    def render_block_padding(self) -> list[str]:
        return [
            block_body_bg_seq(),
            erase_line_seq(),
            reset_attrs_seq(),
            "\n",
        ]

    def render_block_footer(self, text: str) -> list[str]:
        return [
            block_header_bg_seq(),
            block_header_fg_seq(),
            erase_line_seq(),
            " " + text,
            reset_attrs_seq(),
            "\n",
        ]


class InputHandler:
    def __init__(self) -> None:
        self.kb = KeyBindings()
        self.shortcut_pressed = None
        self.session: PromptSession[Any] = PromptSession(
            completer=SlashCommandCompleter(),
            complete_while_typing=False,
            key_bindings=self.kb,
        )

        @self.kb.add("c-y")
        def _(event: Any) -> None:
            self.shortcut_pressed = "<c-y>"
            event.app.exit()

        @self.kb.add("c-d")
        def _(event: Any) -> None:
            self.shortcut_pressed = "<c-d>"
            event.app.exit()

    def prompt(self) -> str:
        self.shortcut_pressed = None
        user_input = self.session.prompt(HTML("<b><ansigreen>></ansigreen></b> "))

        if self.shortcut_pressed:
            return self.shortcut_pressed
        else:
            assert isinstance(user_input, str)
            return user_input


class Shell:
    def __init__(  # noqa PLR0913
        self,
        prompt: str | None,
        loop: asyncio.AbstractEventLoop,
        input_handler: InputHandler,
        chat: Chat,
        connection_tracker: ConnectionTracker,
    ) -> None:
        self.prompt = prompt
        self.loop = loop
        self.input_handler = input_handler
        self.chat = chat
        self.stream_fut: Future[Any] | None = None
        self.connection_tracker = connection_tracker

    def run(self) -> None:
        self._print_welcome_message()
        self._send_initial_prompt()

        while True:
            try:
                self._wait_for_stream_completion()
                text = self.input_handler.prompt()

                if text.startswith("/"):
                    self._run_command(text[1:].strip())
                elif text == "<c-y>":
                    self._confirm_execution()
                elif text in {"q", "exit"}:
                    print()
                    break
                elif text == "<c-d>":
                    print()
                    do_quit = self._ask_for_quit_confirmation()
                    print()

                    if do_quit:
                        break
                elif text:
                    print()
                    self._send_prompt(text)

            except KeyboardInterrupt:
                if self.stream_fut is not None:
                    self._run_coroutine(self.chat.halt_stream()).result()
                else:
                    do_quit = self._ask_for_quit_confirmation()
                    print()

                    if do_quit:
                        break

            except ExponentError as e:
                self._print_error_message(e)
                break

    def _ensure_connected(self) -> None:
        if not self.connection_tracker.is_connected():
            self._run_coroutine(self._wait_for_reconnection()).result()

    async def _wait_for_reconnection(self) -> None:
        render([clear_line_seq(), "Disconnected..."])
        await asyncio.sleep(1)
        spinner = Spinner("Reconnecting...")
        spinner.show()
        await self.connection_tracker.wait_for_reconnection()
        spinner.hide()
        render([fg_color_seq(2), "\x1b[1m", "✓ Reconnected"])
        await asyncio.sleep(1)
        render([clear_line_seq()])

    def _print_welcome_message(self) -> None:
        print("Welcome to ✨ \x1b[1;32mExponent \x1b[4:3mSHELL\x1b[0m ✨")
        print()
        print("Type 'q', 'exit' or press <C-c> to exit")
        print("Enter '/help' to see a list of available commands")
        print()

    def _print_error_message(self, e: ExponentError) -> None:
        print(f"\n\n\x1b[1;31m{e}\x1b[0m")
        print("\x1b[3;33m")
        print("Please try again and reach out if the problem persists.")
        print("\x1b[0m")

    def _show_help(self) -> None:
        print()

        for command, description in SLASH_COMMANDS.items():
            print(f"{command} - {description}")

        print()

    def _run_command(self, command: str) -> None:
        if command == "help":
            self._show_help()
        elif command == "autorun":
            self._toggle_autorun()
        elif command == "web":
            self._switch_chat_to_web()
        else:
            print(f"\nUnknown command: {command}\n")

    def _ask_for_quit_confirmation(self) -> bool:
        while True:
            answer = input("Do you want to quit Exponent shell? [y/N] ").strip().lower()

            if answer in {"y", "yes"}:
                return True
            elif answer in {"n", "no", ""}:
                return False

    def _toggle_autorun(self) -> None:
        if self.chat.toggle_autorun():
            print("\nAutorun mode enabled\n")
        else:
            print("\nAutorun mode disabled\n")

    def _switch_chat_to_web(self) -> None:
        url = self.chat.url()
        print(f"\nThis chat has been moved to {url}\n")

        if not inside_ssh_session():
            click.launch(url)

        while True:
            input()

    def _confirm_execution(self) -> None:
        render(
            [
                "\r",
                move_cursor_up_seq(1),
                clear_line_seq(),
            ]
        )

        self._ensure_connected()
        self.stream_fut = self._run_coroutine(self.chat.send_confirmation())

    def _send_initial_prompt(self) -> None:
        if self.prompt is not None:
            self._send_prompt(self.prompt)

    def _send_prompt(self, text: str) -> None:
        self._ensure_connected()
        self.stream_fut = self._run_coroutine(self.chat.send_prompt(text))

    def _wait_for_stream_completion(self) -> None:
        if self.stream_fut is not None:
            self.stream_fut.result()
            self.stream_fut = None

    def _run_coroutine(self, coro: Coroutine[Any, Any, Any]) -> Future[Any]:
        return asyncio.run_coroutine_threadsafe(coro, self.loop)


class SlashCommandCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        text = document.text
        if text.startswith("/"):
            for command in SLASH_COMMANDS:
                if command.startswith(text):
                    yield Completion(command, start_position=-len(text))


class Block:
    def __init__(self, event_uuid: str) -> None:
        self.event_uuid = event_uuid
        self.spinner = None
        self.block_row_offset = 0
        self.console = Console()
        self.theme = "monokai"

    def highlight_code(self, code: str, lang: str, line_numbers: bool = True) -> str:
        syntax = Syntax(
            code,
            lang,
            theme=self.theme,
            line_numbers=line_numbers,
            word_wrap=True,
        )

        with self.console.capture() as capture:
            self.console.print(syntax)

        return capture.get()


class NullBlock(Block):
    def __init__(self) -> None:
        super().__init__("")


class MessageBlock(Block):
    def __init__(self, event_uuid: str) -> None:
        super().__init__(event_uuid)
        self.content_len = 0

    def render_message(self, message: str) -> list[Any]:
        message = message.strip()
        chunk = message[self.content_len :]
        self.content_len = len(message)

        return [chunk]


class CodeBlock(Block):
    def __init__(self, event_uuid: str, lang: str) -> None:
        super().__init__(event_uuid)
        self.lang = lang
        self.line_count = 0

    def render_code(
        self,
        code: str,
    ) -> list[Any]:
        seqs: list[Any] = []

        code = pad_left(code.strip(), "  ")
        code = self.highlight_code(code, self.lang, line_numbers=False)
        lines = code.split("\n")
        lines = lines[0 : len(lines) - 1]
        new_line_count = len(lines)

        if self.line_count > 0:
            seqs.append([move_cursor_up_seq(1), "\r"])
            lines = lines[self.line_count - 1 :]

        lines = [line + "\n" for line in lines]
        seqs.append(lines)
        self.line_count = new_line_count

        return seqs


class FileWriteBlock(Block):
    def __init__(self, event_uuid: str, lang: str) -> None:
        super().__init__(event_uuid)
        self.lang = lang
        self.line_count = 0

    def render_content(self, content: str) -> list[Any]:
        seqs: list[Any] = []
        code = pad_left(content.strip(), "  ")
        code = self.highlight_code(code, "rust" or self.lang, line_numbers=False)
        lines = code.split("\n")
        lines = lines[0 : len(lines) - 1]
        new_line_count = len(lines)

        if self.line_count > 0:
            seqs.append([move_cursor_up_seq(1), "\r"])
            lines = lines[self.line_count - 1 :]

        lines = [line + "\n" for line in lines]
        seqs.append(lines)
        self.line_count = new_line_count

        return seqs


class CommandBlock(Block):
    def __init__(self, event_uuid: str, type: str, lang: str) -> None:
        super().__init__(event_uuid)
        self.type = type
        self.lang = lang
        self.line_count = 0

    def render_data(self, data: dict[str, Any]) -> list[Any]:
        seqs: list[Any] = []
        paths = self.render_paths(data["filePath"])
        new_line_count = len(paths)

        if self.line_count > 0:
            seqs.append([move_cursor_up_seq(1), "\r"])
            paths = paths[self.line_count - 1 :]

        seqs.append(paths)
        self.line_count = new_line_count

        return seqs

    def render_paths(self, paths: str) -> list[Any]:
        lines = pad_left(paths.strip(), "  ").split("\n")

        return [[block_body_bg_seq(), erase_line_seq(), line, "\n"] for line in lines]


def text_line_count(text: str) -> int:
    cols = get_terminal_width()
    count = 0

    for line in text.split("\n"):
        count += len(line) // cols

        if len(line) == 0 or len(line) % cols > 0:
            count += 1

    return count


def get_terminal_width() -> int:
    cols, _ = shutil.get_terminal_size()
    return cols


def pad_left(text: str, padding: str) -> str:
    return "\n".join([padding + line for line in text.strip().split("\n")])


def fg_color_seq(c: int) -> str:
    return f"\x1b[{30 + c}m"


def block_header_bg_seq() -> str:
    return "\x1b[48;2;29;30;24m"


def block_header_fg_seq() -> str:
    return "\x1b[38;5;246m"


def block_body_bg_seq() -> str:
    return "\x1b[48;5;235m"


def erase_line_seq() -> str:
    return "\x1b[2K"


def erase_display_seq() -> str:
    return "\x1b[0J"


def reset_attrs_seq() -> str:
    return "\x1b[0m"


def clear_line_seq() -> str:
    return f"\r{reset_attrs_seq()}{erase_line_seq()}"


def move_cursor_up_seq(n: int) -> str:
    if n > 0:
        return f"\x1b[{n}A"
    else:
        return ""


def move_cursor_down_seq(n: int) -> str:
    if n > 0:
        return f"\x1b[{n}B"
    else:
        return ""


def render(seqs: str | list[Any] | None) -> int:
    text, newline_count = collect(seqs)
    print(text, end="")
    sys.stdout.flush()

    return newline_count


def collect(seqs: str | list[Any] | None) -> tuple[str, int]:
    if seqs is None:
        return ("", 0)

    if isinstance(seqs, str):
        return (seqs, seqs.count("\n"))

    if isinstance(seqs, tuple):
        return seqs

    assert isinstance(seqs, list)

    text = ""
    newline_count = 0

    for seq in seqs:
        t, c = collect(seq)
        text += t
        newline_count += c

    return (text, newline_count)
