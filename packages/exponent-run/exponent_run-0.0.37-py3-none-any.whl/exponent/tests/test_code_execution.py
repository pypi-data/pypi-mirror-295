import os

from exponent.core.remote_execution.command_execution import execute_command
from exponent.core.remote_execution.file_write import (
    execute_search_replace_edit,
    execute_udiff_edit,
)
from exponent.core.remote_execution.languages.shell import execute_shell
from exponent.core.remote_execution.types import CommandRequest, CommandResponse
from exponent.core.types.generated.command_request_data import (
    FileReadCommandRequestData,
)


async def test_execute_shell(default_temporary_directory: str) -> None:
    output = await execute_shell(
        code="ls -1v",
        working_directory=default_temporary_directory,
        timeout=5,
    )

    output_lines = output.strip().split("\n")
    expected_lines = 6

    assert len(output_lines) == expected_lines

    assert output_lines == [
        "exponent.txt",
        "symlink.txt",
        "test1.py",
        "test2.py",
        "",
        "EXIT CODE: 0",
    ]

    output = await execute_shell(
        code="true && echo 'hi' || echo \"boo\"",
        working_directory=default_temporary_directory,
        timeout=5,
    )

    assert output.strip() == "hi\n\nEXIT CODE: 0"


async def test_execute_udiff(temporary_directory_with_bigger_file: str) -> None:
    diff = (
        "@@ ... @@\n"
        " def subtract(a: int, b: int) -> int:\n"
        "-    return a ++ b\n"
        "+    return a - b\n"
        " \n"
        " def add(a: int, b: int) -> int:\n"
    )
    execute_udiff_edit(
        file_path="test1.py",
        content=diff,
        working_directory=temporary_directory_with_bigger_file,
    )

    contents = None
    with open(os.path.join(temporary_directory_with_bigger_file, "test1.py")) as f:
        contents = f.read()

    assert (
        contents
        == """
def subtract(a: int, b: int) -> int:
    return a - b

def add(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b
"""
    )


async def test_execute_udiff_fuzzy(temporary_directory_with_bigger_file: str) -> None:
    diff = (
        "@@ ... @@\n"
        " def subtract(a: int, b: int) -> int:\n"
        "-    return a ++ b\n"
        "+    return a - b\n"
        " def add(a: int, b: int) -> int:\n"
    )
    execute_udiff_edit(
        file_path="test1.py",
        content=diff,
        working_directory=temporary_directory_with_bigger_file,
    )

    contents = None
    with open(os.path.join(temporary_directory_with_bigger_file, "test1.py")) as f:
        contents = f.read()

    assert (
        contents
        == """
def subtract(a: int, b: int) -> int:
    return a - b

def add(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b
"""
    )


async def test_execute_search_replace(
    temporary_directory_with_bigger_file: str,
) -> None:
    diff = (
        "<<<<< SEARCH\n"
        "def subtract(a: int, b: int) -> int:\n"
        "    return a ++ b\n"
        "======\n"
        "def subtract(a: int, b: int) -> int:\n"
        "    return a - b\n"
        ">>>>>> REPLACE\n"
    )
    execute_search_replace_edit(
        file_path="test1.py",
        content=diff,
        working_directory=temporary_directory_with_bigger_file,
    )

    contents = None
    with open(os.path.join(temporary_directory_with_bigger_file, "test1.py")) as f:
        contents = f.read()

    assert (
        contents
        == """
def subtract(a: int, b: int) -> int:
    return a - b

def add(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b
"""
    )


async def test_execute_search_replace_fuzzy(
    temporary_directory_with_bigger_file: str,
) -> None:
    diff = (
        "<<<<SEARCH\n"
        "def subtract(a: int, b: int) -> int:\n"
        "    return a ++ b\n"
        "======\n"
        "def subtract(a: int, b: int) -> int:\n"
        "    return a - b\n"
        ">>>>>>>>>> REPLACE\n"
    )
    execute_search_replace_edit(
        file_path="test1.py",
        content=diff,
        working_directory=temporary_directory_with_bigger_file,
    )

    contents = None
    with open(os.path.join(temporary_directory_with_bigger_file, "test1.py")) as f:
        contents = f.read()

    assert (
        contents
        == """
def subtract(a: int, b: int) -> int:
    return a - b

def add(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b
"""
    )


async def test_execute_command(default_temporary_directory: str) -> None:
    request = CommandRequest(
        correlation_id="123456",
        data=FileReadCommandRequestData(file_path="test1.py", language="python"),
    )

    response = await execute_command(
        request, working_directory=default_temporary_directory
    )

    assert response == CommandResponse(
        content="print('Hello, world!')",
        correlation_id="123456",
    )
