import json
from os import path
from clangd_client import ClangdClient

TEMPLATE_C_FILE = """#include "windows.h"
int main() {
    __REPLACE_ME__(
    return 0;
}
"""


def function_parameters(requested_function):
    client = ClangdClient()
    client.initialize()

    # Setup the compiler
    dummy_dir = "/tmp"
    dummy_file = path.join(dummy_dir, "dummy.c")
    compiler_commands = [
        {
            "directory": dummy_dir,
            "command": f'clang -target x86_64-w64-mingw32 "{dummy_file}"',
            "file": dummy_file,
        }
    ]

    compiler_commands_file = path.join(dummy_dir, "compile_commands.json")
    json.dump(compiler_commands, open(compiler_commands_file, "w"))
    file_contents = TEMPLATE_C_FILE.replace("__REPLACE_ME__", requested_function)

    # Send the open message
    client.open_file(dummy_file, file_contents)

    # Find the line,position for the function
    line, position = [
        (i, v.index(requested_function) + len(requested_function) + 1)
        for i, v in enumerate(file_contents.split("\n"))
        if requested_function in v
    ][0]

    response = client.request_signature(dummy_file, line, position)
    client.shutdown()

    signatures = response.get("result", {}).get("signatures")
    return signatures
