import json
import re
from os import path
from clangd_client import ClangdClient

TEMPLATE_C_FILE = """#include "windows.h"
int main() {
    __REPLACE_ME__(
    return 0;
}
"""

class Resolver:
    def __init__(self):
        self._client = ClangdClient()
        self._client.initialize()
        self._dummy_dir = "/tmp"
        self._dummy_file = path.join(self._dummy_dir, "dummy.c")

        compiler_commands_file = path.join(self._dummy_dir, "compile_commands.json")
        if not path.exists(compiler_commands_file):
            # Write the compiler commands file if not already on disk
            compiler_commands = [
                {
                    "directory": self._dummy_dir,
                    "command": f'clang -target x86_64-w64-mingw32 "{self._dummy_file}"',
                    "file": self._dummy_file,
                }
            ]
            json.dump(compiler_commands, open(compiler_commands_file, "w"))

    def get_signature(self, name):
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
        if not re.match(pattern, name):
            raise RuntimeError("Not a valid function name!")

        file_contents = TEMPLATE_C_FILE.replace("__REPLACE_ME__", name)

        # Send the open message
        self._client.open_file(self._dummy_file, file_contents)

        # Find the line,position for the function
        line, position = [
            (i, v.index(name) + len(name) + 1)
            for i, v in enumerate(file_contents.split("\n"))
            if name in v
        ][0]

        response = self._client.request_signature(self._dummy_file, line, position)

        signatures = response.get("result", {}).get("signatures")
        return signatures
