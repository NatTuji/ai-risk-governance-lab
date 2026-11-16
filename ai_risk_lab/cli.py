"""Local file interface; declared inputs never become commands or network calls."""

import argparse
import json
from pathlib import Path
import sys

from .engine import assess
from .model import load_use_case
from .report import render_markdown

def main(argv=None):
    parser = argparse.ArgumentParser(description="Assess a declared AI deployment locally.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    command = subparsers.add_parser("assess", help="Generate an assessment for human review")
    command.add_argument("input", type=Path, help="UTF-8 JSON use case")
    command.add_argument("--format", choices=("markdown", "json"), default="markdown")
    command.add_argument("--output", type=Path, help="New report file; existing files are protected")
    args = parser.parse_args(argv)
    try:
        result = assess(load_use_case(args.input))
        output = (
            json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
            if args.format == "json"
            else render_markdown(result)
        )
        if args.output:
            # Exclusive creation prevents accidental overwrite, including the input.
            with args.output.open("x", encoding="utf-8", newline="\n") as target:
                target.write(output)
        else:
            sys.stdout.write(output)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0
