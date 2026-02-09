"""Built-in filesystem tools for Akatsuki agents.

Provides read_file, write_file, list_directory, and run_command
so agents can interact with the local codebase.
"""

from __future__ import annotations

import os
import subprocess

from agents import function_tool


@function_tool
def read_file(file_path: str) -> str:
    """Read and return the contents of a file."""
    path = os.path.abspath(file_path)
    with open(path) as f:
        return f.read()


@function_tool
def write_file(file_path: str, content: str) -> str:
    """Write content to a file. Creates parent directories if needed."""
    path = os.path.abspath(file_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} chars to {path}"


@function_tool
def list_directory(directory: str = ".") -> str:
    """List files and directories at the given path."""
    path = os.path.abspath(directory)
    entries = sorted(os.listdir(path))
    result = []
    for entry in entries:
        full = os.path.join(path, entry)
        prefix = "d " if os.path.isdir(full) else "f "
        result.append(prefix + entry)
    return "\n".join(result)


@function_tool
def run_command(command: str) -> str:
    """Run a shell command and return stdout + stderr. Use for git, tests, linting, etc."""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=120,
        cwd=os.getcwd(),
    )
    output = ""
    if result.stdout:
        output += result.stdout
    if result.stderr:
        output += "\n" + result.stderr
    if result.returncode != 0:
        output += f"\n[exit code: {result.returncode}]"
    return output.strip()


# Grouped tool sets for different permission levels
READ_TOOLS = [read_file, list_directory]
WRITE_TOOLS = [read_file, write_file, list_directory, run_command]
