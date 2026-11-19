"""Reading and writing entry files in one consistent YAML style.

Every tool that writes YAML goes through dump_entry(), so files written by a
script look like files written by hand and diffs stay small.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

SCHEMA_HEADER = "# yaml-language-server: $schema=../schema/effect.schema.json\n"
FOLD_AT = 72  # longer strings are written as folded blocks (>-)
WIDTH = 88


class _Dumper(yaml.SafeDumper):
    """SafeDumper that indents block sequences under their key."""

    def increase_indent(self, flow: bool = False, indentless: bool = False):
        return super().increase_indent(flow, False)


def _str(dumper: yaml.SafeDumper, value: str):
    style = None
    if len(value) > FOLD_AT and "\n" not in value and value == value.strip() and "  " not in value:
        style = ">"
    elif "\n" in value:
        style = "|"
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_Dumper.add_representer(str, _str)


def dumps(data: Any) -> str:
    text = yaml.dump(
        data,
        Dumper=_Dumper,
        allow_unicode=True,
        sort_keys=False,
        width=WIDTH,
        default_flow_style=False,
    )
    # A folded block must read back as exactly the same string; if PyYAML's
    # line folding ever changes a value, fall back to the plain style.
    if yaml.safe_load(text) != data:
        text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=WIDTH)
        if yaml.safe_load(text) != data:
            raise ValueError("YAML round trip changed the data")
    return text


def dump_entry(entry: dict[str, Any], path: Path) -> None:
    path.write_text(SCHEMA_HEADER + dumps(entry), encoding="utf-8", newline="\n")


def dump_plain(data: Any, path: Path, header: str = "") -> None:
    path.write_text(header + dumps(data), encoding="utf-8", newline="\n")


def load(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)
