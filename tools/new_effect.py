"""Create a new, empty entry file to fill in by hand.

    python tools/new_effect.py magnetostriction --name-en "Magnetostriction" \
        --name-de "Magnetostriktion" --author "Erika Musterfrau" \
        --source https://en.wikipedia.org/wiki/Magnetostriction

The file lands in effects/<id>.yaml with all fields present and empty. Write
the description in your own words, choose the cells from
vocabulary/vocabulary.yaml, then run `python tools/build.py --check`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yamlio  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def text_block(name: str, author: str, kind: str) -> dict[str, str]:
    return {
        "name": name,
        "description": "TODO: describe the effect in your own words.",
        "example": "",
        "conditions": "",
        "limits": "",
        "sideEffects": "",
        "kind": kind,
        "author": author,
        "model": "",
        "updated": dt.date.today().isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("id", help="lower-case, hyphenated, English, e.g. acoustic-levitation")
    parser.add_argument("--name-en", required=True)
    parser.add_argument("--name-de", required=True)
    parser.add_argument("--author", required=True, help="your name as it should appear in NOTICE.md")
    parser.add_argument("--kind", choices=["effect", "application"], default="effect")
    parser.add_argument("--source", action="append", default=[], help="URL or literature reference (repeatable)")
    parser.add_argument("--lang", choices=["de", "en"], default="de", help="language you write the original in")
    args = parser.parse_args()

    if not ID_PATTERN.match(args.id):
        parser.error("id must be lower-case words joined by hyphens")
    path = ROOT / "effects" / f"{args.id}.yaml"
    if path.exists():
        parser.error(f"{path.relative_to(ROOT)} exists already")

    names = {"de": args.name_de, "en": args.name_en}
    entry = {
        "id": args.id,
        "kind": args.kind,
        "home": "",
        "functions": [],
        "parameters": [],
        "uses": [],
        "domain": {"id": "", "de": "", "en": ""},
        "maturity": "",
        "sources": args.source,
        "authors": [args.author],
        # A second person reviews the entry before it goes into a release.
        "review": {"status": "ungeprueft", "by": [], "date": ""},
        # Only the language you write in. The translation is added later, marked
        # kind: maschinell (with model) until a person has read it.
        "text": {args.lang: text_block(names[args.lang], args.author, "original")},
    }
    yamlio.dump_entry(entry, path)
    print(f"Created {path.relative_to(ROOT)} - fill in the TODOs, then run: python tools/build.py --check")
    notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
    if args.author not in notice:
        print(f"Add '- {args.author}' to the contributor list in NOTICE.md (the build checks this).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
