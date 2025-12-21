from __future__ import annotations

import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("LocalNotes")

NOTES_FILE = Path(__file__).with_name("notes.txt")


@mcp.tool()
def get_notes_file_path(create_if_missing: bool = False) -> str:
    """
    Returns the absolute path to the notes file used by this server.

    Args:
        create_if_missing: If True, creates the file if it does not exist.
    """
    try:
        if create_if_missing:
            NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
            NOTES_FILE.touch(exist_ok=True)

        return str(NOTES_FILE.resolve())
    except Exception as e:
        print(f"[server] Error getting notes file path: {e}", file=sys.stderr)
        return f"Error getting notes file path: {e}"


@mcp.tool()
def add_note_to_file(content: str) -> str:
    """
    Appends the given content to the user's local notes.
    Args:
        content: The text content to append.
    """
    try:
        NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with NOTES_FILE.open("a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"Content appended to {NOTES_FILE.name}."
    except Exception as e:
        print(f"[server] Error appending to file: {e}", file=sys.stderr)
        return f"Error appending to file {NOTES_FILE.name}: {e}"


@mcp.tool()
def read_notes() -> str:
    """
    Reads and returns the contents of the user's local notes.
    """
    try:
        notes = NOTES_FILE.read_text(encoding="utf-8")
        return notes if notes.strip() else "No notes found."
    except FileNotFoundError:
        return "No notes file found."
    except Exception as e:
        print(f"[server] Error reading file: {e}", file=sys.stderr)
        return f"Error reading file {NOTES_FILE.name}: {e}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
