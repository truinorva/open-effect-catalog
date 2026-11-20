"""Import (or re-sync) entries from the TRIZ Effects Database by TRIZ Consulting Group.

    python tools/import_tcg.py                 # fetch from triz-consulting.de
    python tools/import_tcg.py --from DIR      # use a local copy (effects.json, functions.json)
    python tools/import_tcg.py --dry-run       # only report what would change

Writes one file per entry to effects/<id>.yaml (marked origin: triz-consulting).
Entries written for this project (no origin, or another origin) are never
touched. A re-sync overwrites local edits to imported entries; review the
result with `git diff`.

The vocabulary is NOT imported. It was taken over once (version 2.1.1) and has
been maintained in this repository since 2026-11-20 (vocabulary/vocabulary.yaml).
The script only reports how the upstream vocabulary differs, and warns when an
imported entry uses a cell that the repository's vocabulary does not know.

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
REVIEWER = "TRIZ Consulting Group"
ENTRY_KEYS = [
    "id", "kind", "home", "functions", "parameters", "uses",
    "domain", "maturity", "sources", "authors",
]


def fetch(source: str | None, name: str) -> Any:
    if source:
        return json.loads((Path(source) / name).read_text(encoding="utf-8"))
    req = urllib.request.Request(BASE_URL + name, headers={"User-Agent": "open-effects-catalog-import"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (fixed https URL)
        return json.loads(resp.read().decode("utf-8"))


def vocab_ids(vocab: dict[str, Any]) -> dict[str, set[str]]:
    return {
        "actions": {a["id"] for d in vocab.get("domains", []) for a in d.get("actions", [])},
        "objects": {o["id"] for o in vocab.get("objects", [])},
        "operations": {o["id"] for o in vocab.get("operations", [])},
        "parameters": {p["id"] for g in vocab.get("parameterGroups", []) for p in g.get("parameters", [])},
    }


def unknown_cells(entry: dict[str, Any], ids: dict[str, set[str]]) -> list[str]:
    bad = [c for c in entry["functions"]
           if c.partition("|")[0] not in ids["actions"] or c.partition("|")[2] not in ids["objects"]]
    bad += [c for c in entry["parameters"]
            if c.partition("|")[0] not in ids["operations"] or c.partition("|")[2] not in ids["parameters"]]
    return bad


def to_entry(raw: dict[str, Any], version: str) -> dict[str, Any]:
    unknown = set(raw) - set(ENTRY_KEYS) - {"text"}
    if unknown:
        raise SystemExit(f"{raw.get('id')}: unknown upstream fields {sorted(unknown)} - extend the schema first")
    entry = {key: raw[key] for key in ENTRY_KEYS}
    entry["origin"] = ORIGIN
    # Entries are written by practitioners and released by a reviewer at TRIZ
    # Consulting Group before they are published there, so they count as reviewed.
    entry["review"] = {"status": "geprueft", "by": [REVIEWER], "date": version}
    entry["text"] = raw["text"]
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="source", help="directory with effects.json and functions.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    effects = fetch(args.source, "effects.json")
    upstream_vocab = fetch(args.source, "functions.json")
    local_ids = vocab_ids(yamlio.load(ROOT / "vocabulary" / "vocabulary.yaml"))
    meta = effects.get("meta", {})
    print(f"Upstream: {meta.get('title')} {meta.get('version')} ({meta.get('license')}), "
          f"{len(effects['effects'])} entries")

    out_dir = ROOT / "effects"
    out_dir.mkdir(exist_ok=True)
    created = updated = unchanged = skipped = 0
    for raw in effects["effects"]:
        entry = to_entry(raw, meta.get("version", ""))
        path = out_dir / f"{entry['id']}.yaml"
        for cell in unknown_cells(entry, local_ids):
            print(f"  warn   {path.name}: cell {cell!r} is not in vocabulary/vocabulary.yaml - add it there or adjust the entry")
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

    # The vocabulary is maintained here; upstream changes are only reported.
    upstream_ids = vocab_ids(upstream_vocab)
    vocab_diff = []
    for kind in local_ids:
        added = sorted(upstream_ids[kind] - local_ids[kind])
        dropped = sorted(local_ids[kind] - upstream_ids[kind])
        if added:
            vocab_diff.append(f"upstream has {kind} not in the repository: {', '.join(added)}")
        if dropped:
            vocab_diff.append(f"repository has {kind} not upstream: {', '.join(dropped)}")
    for line in vocab_diff:
        print(f"  vocab  {line}")

    upstream_entry_ids = {raw["id"] for raw in effects["effects"]}
    gone = [p.name for p in out_dir.glob("*.yaml")
            if p.stem not in upstream_entry_ids and (yamlio.load(p) or {}).get("origin") == ORIGIN]
    for name in gone:
        print(f"  note   {name}: imported earlier but no longer upstream - decide by hand")

    print(f"Done{' (dry run)' if args.dry_run else ''}: {created} new, {updated} updated, "
          f"{unchanged} unchanged, {skipped} skipped; vocabulary not imported "
          f"({'differs from upstream, see above' if vocab_diff else 'same ids as upstream'}).")
    print(f"Remember: set origins.{ORIGIN}.version in dataset.yaml to {meta.get('version')!r} and update NOTICE.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
