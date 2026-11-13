"""Check extensions.json, the registry, against its format.

Run from the repository root: ``python scripts/check.py``. It uses only the
standard library and never downloads anything. It exits with 1 and prints
every problem when the registry does not follow the format in README.md.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).resolve().parent.parent / "extensions.json"
SCHEMA = 1
ID = re.compile(r"[a-z0-9-]+(\.[a-z0-9-]+)+")
MAX_ID_BYTES = 128
URL = re.compile(r"https?://\S+")
REQUIRED = ("id", "name", "author", "reference")
TEXT_FIELDS = ("name", "description")
URL_FIELDS = ("reference", "download_url", "update_url")


def main() -> int:
    """Check the registry and report what is wrong.

    Returns:
        0 when the registry is valid, 1 otherwise.
    """
    try:
        document = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"extensions.json: {error}")
        return 1
    problems = check(document)
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print(f"extensions.json: {len(document['extensions'])} extensions, valid")
    return 0


def check(document: Any) -> list[str]:
    """List the problems of a registry document.

    Args:
        document: The decoded contents of extensions.json.

    Returns:
        One line per problem; empty when there is none.
    """
    if not isinstance(document, dict):
        return ["the registry must be an object"]
    problems = []
    if document.get("schema") != SCHEMA:
        problems.append(f"`schema` must be {SCHEMA}")
    entries = document.get("extensions")
    if not isinstance(entries, list):
        return [*problems, "`extensions` must be a list"]
    ids = []
    for index, entry in enumerate(entries):
        where = f"extensions[{index}]"
        if not isinstance(entry, dict):
            problems.append(f"{where}: must be an object")
            continue
        if isinstance(entry.get("id"), str):
            where = f"{where} ({entry['id']})"
        problems.extend(f"{where}: {problem}" for problem in check_entry(entry))
        if isinstance(entry.get("id"), str):
            ids.append(entry["id"])
    duplicates = sorted({id_ for id_ in ids if ids.count(id_) > 1})
    problems.extend(f"`{id_}` is listed more than once" for id_ in duplicates)
    if ids != sorted(ids):
        problems.append("entries must be sorted by `id`")
    return problems


def check_entry(entry: dict[str, Any]) -> list[str]:
    """List the problems of one entry.

    Args:
        entry: One element of `extensions`.

    Returns:
        One line per problem; empty when there is none.
    """
    problems = [f"`{field}` is required" for field in REQUIRED if field not in entry]
    id_ = entry.get("id")
    if "id" in entry and not (
        isinstance(id_, str) and ID.fullmatch(id_) and len(id_.encode()) <= MAX_ID_BYTES
    ):
        problems.append(
            "`id` must be reverse-DNS: two or more labels of [a-z0-9-] joined by dots"
        )
    if "author" in entry and not non_empty_text(entry["author"]):
        problems.append("`author` must be non-empty text")
    for field in TEXT_FIELDS:
        if field in entry and not localized_text(entry[field]):
            problems.append(
                f"`{field}` must be non-empty text or an object of language to text"
            )
    for field in URL_FIELDS:
        value = entry.get(field)
        if field in entry and not (isinstance(value, str) and URL.fullmatch(value)):
            problems.append(f"`{field}` must be an http(s) URL")
    return problems


def non_empty_text(value: Any) -> bool:
    """Tell whether a value is a string with something in it.

    Args:
        value: Any decoded JSON value.

    Returns:
        Whether it is a non-blank string.
    """
    return isinstance(value, str) and bool(value.strip())


def localized_text(value: Any) -> bool:
    """Tell whether a value is text, or a non-empty object of language to text.

    Args:
        value: Any decoded JSON value.

    Returns:
        Whether it is text or a language map of text.
    """
    if isinstance(value, dict):
        return bool(value) and all(non_empty_text(text) for text in value.values())
    return non_empty_text(value)


if __name__ == "__main__":
    sys.exit(main())
