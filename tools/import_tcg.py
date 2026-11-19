"""Import (or re-sync) entries from the TRIZ Effects Database by TRIZ Consulting Group.

    python tools/import_tcg.py                 # fetch from triz-consulting.de
    python tools/import_tcg.py --from DIR      # use a local copy (effects.json, functions.json)
    python tools/import_tcg.py --dry-run       # only report what would change

Writes one file per entry to effects/<id>.yaml (marked origin: triz-consulting)
and the vocabulary to vocabulary/vocabulary.yaml. Entries written for this
project (no origin, or another origin) are never touched. A re-sync overwrites
local edits to imported entries; review the result with `git diff`.

Upstream publishes the data under CC BY 4.0; Robert Adunka, TRIZ Consulting Group,
permitted its use in this repository under the MIT License.
After a re-sync, update the data version in dataset.yaml and NOTICE.md.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yamlio  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://www.triz-consulting.de/EffectsDatabase/data/"
ORIGIN = "triz-consulting"
ENTRY_KEYS = [
    "id", "kind", "home", "functions", "parameters", "uses",
    "domain", "maturity", "sources", "authors",
]
VOCAB_HEADER = (
    "# Vocabulary: actions (grouped in domains), objects, operations and parameters.\n"
    "# Taken over from the TRIZ Effects Database by Robert Adunka, TRIZ Consulting Group\n"
    "# (used under MIT with his permission). Ids are stable: cells in effects/*.yaml refer\n"
    "# to them. Labels, hints and synonyms may be reworded at any time.\n"
)


def fetch(source: str | None, name: str) -> Any:
    if source:
        return json.loads((Path(source) / name).read_text(encoding="utf-8"))
    req = urllib.request.Request(BASE_URL + name, headers={"User-Agent": "open-effect-catalog-import"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (fixed https URL)
        return json.loads(resp.read().decode("utf-8"))


def to_entry(raw: dict[str, Any]) -> dict[str, Any]:
    unknown = set(raw) - set(ENTRY_KEYS) - {"text"}
    if unknown:
        raise SystemExit(f"{raw.get('id')}: unknown upstream fields {sorted(unknown)} - extend the schema first")
    entry = {key: raw[key] for key in ENTRY_KEYS}
    entry["origin"] = ORIGIN
    entry["text"] = raw["text"]
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="source", help="directory with effects.json and functions.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    effects = fetch(args.source, "effects.json")
    vocab = fetch(args.source, "functions.json")
    meta = effects.get("meta", {})
    print(f"Upstream: {meta.get('title')} {meta.get('version')} ({meta.get('license')}), "
          f"{len(effects['effects'])} entries")

    out_dir = ROOT / "effects"
    out_dir.mkdir(exist_ok=True)
    created = updated = unchanged = skipped = 0
    for raw in effects["effects"]:
        entry = to_entry(raw)
        path = out_dir / f"{entry['id']}.yaml"
        new_text = yamlio.SCHEMA_HEADER + yamlio.dumps(entry)
        if path.exists():
            current = yamlio.load(path) or {}
            if current.get("origin") != ORIGIN:
                print(f"  skip {path.name}: written for this project, not imported")
                skipped += 1
                continue
            if path.read_text(encoding="utf-8") == new_text:
                unchanged += 1
                continue
            updated += 1
            print(f"  update {path.name}")
        else:
            created += 1
            print(f"  new    {path.name}")
        if not args.dry_run:
            path.write_text(new_text, encoding="utf-8", newline="\n")

    vocab_path = ROOT / "vocabulary" / "vocabulary.yaml"
    vocab_changed = not vocab_path.exists() or yamlio.load(vocab_path) != vocab
    if vocab_changed:
        print("  vocabulary changed" if vocab_path.exists() else "  new    vocabulary.yaml")
        if not args.dry_run:
            vocab_path.parent.mkdir(exist_ok=True)
            yamlio.dump_plain(vocab, vocab_path, header=VOCAB_HEADER)

    upstream_ids = {raw["id"] for raw in effects["effects"]}
    gone = [p.name for p in out_dir.glob("*.yaml")
            if p.stem not in upstream_ids and (yamlio.load(p) or {}).get("origin") == ORIGIN]
    for name in gone:
        print(f"  note   {name}: imported earlier but no longer upstream - decide by hand")

    print(f"Done{' (dry run)' if args.dry_run else ''}: {created} new, {updated} updated, "
          f"{unchanged} unchanged, {skipped} skipped, vocabulary {'changed' if vocab_changed else 'unchanged'}.")
    print(f"Remember: set origins.{ORIGIN}.version in dataset.yaml to {meta.get('version')!r} and update NOTICE.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
