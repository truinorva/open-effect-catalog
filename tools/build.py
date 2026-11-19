"""Validate every entry and bundle the release.

    python tools/build.py --check                  # validate only (CI on every pull request)
    python tools/build.py                          # validate and write dist/
    python tools/build.py --version 2026.12.0      # what the release workflow runs

dist/ receives:
    effects.json     all entries in one file, with licence and attribution in "meta"
    vocabulary.json  actions, objects, operations and parameters
    NOTICE.md, LICENSE

effects.json and vocabulary.json keep the structure of the TRIZ Effects Database
(effects.json / functions.json), so a release can be dropped into its web viewer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yamlio  # noqa: E402

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    raise SystemExit("jsonschema is missing: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
ENTRY_ORDER = [
    "id", "kind", "home", "functions", "parameters", "uses",
    "domain", "maturity", "sources", "authors", "origin", "text",
]


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def load_vocabulary(rep: Report) -> tuple[dict[str, Any], dict[str, set[str]]]:
    path = ROOT / "vocabulary" / "vocabulary.yaml"
    vocab = yamlio.load(path)
    ids = {
        "actions": [a["id"] for d in vocab["domains"] for a in d["actions"]],
        "objects": [o["id"] for o in vocab["objects"]],
        "operations": [o["id"] for o in vocab["operations"]],
        "parameters": [p["id"] for g in vocab["parameterGroups"] for p in g["parameters"]],
        "kinds": [k["id"] for k in vocab["kinds"]],
    }
    for name, values in ids.items():
        dupes = sorted({v for v in values if values.count(v) > 1})
        if dupes:
            rep.error("vocabulary", f"duplicate {name} ids {dupes}")
    clash = set(ids["objects"]) & set(ids["parameters"])
    if clash:
        rep.error("vocabulary", f"object and parameter ids must never overlap: {sorted(clash)}")
    kinds = set(ids["kinds"])
    for d in vocab["domains"]:
        for a in d["actions"]:
            if a.get("kind") not in kinds:
                rep.error("vocabulary", f"action {a['id']!r} has unknown kind {a.get('kind')!r}")
    return vocab, {k: set(v) for k, v in ids.items()}


def check_entry(entry: dict[str, Any], path: Path, ids: dict[str, set[str]],
                origins: dict[str, Any], rep: Report) -> None:
    where = f"effects/{path.name}"
    if entry.get("id") != path.stem:
        rep.error(where, f"id {entry.get('id')!r} must equal the file name {path.stem!r}")
    for cell in entry.get("functions", []):
        action, _, obj = cell.partition("|")
        if action not in ids["actions"]:
            rep.error(where, f"function cell {cell!r}: unknown action {action!r}")
        if obj not in ids["objects"]:
            rep.error(where, f"function cell {cell!r}: unknown object {obj!r}")
    for cell in entry.get("parameters", []):
        op, _, par = cell.partition("|")
        if op not in ids["operations"]:
            rep.error(where, f"parameter cell {cell!r}: unknown operation {op!r}")
        if par not in ids["parameters"]:
            rep.error(where, f"parameter cell {cell!r}: unknown parameter {par!r}")
    home = entry.get("home")
    if home and home not in entry.get("functions", []):
        rep.error(where, f"home {home!r} must be one of the function cells")
    if not entry.get("functions") and not entry.get("parameters"):
        rep.warn(where, "no function or parameter cell - the entry cannot be found in the grid")
    if entry.get("kind") == "application" and not entry.get("uses"):
        rep.warn(where, "application without 'uses'")
    origin = entry.get("origin")
    if origin is not None and origin not in origins:
        rep.error(where, f"origin {origin!r} is not defined in dataset.yaml")
    for lang, text in entry.get("text", {}).items():
        for field, value in text.items():
            if "TODO" in value:
                rep.error(where, f"text.{lang}.{field} still contains TODO")
        if text.get("kind") == "maschinell" and not text.get("model"):
            rep.warn(where, f"text.{lang}: machine translation without 'model'")


def load_entries(schema: dict[str, Any], ids: dict[str, set[str]], origins: dict[str, Any],
                 notice: str, rep: Report) -> list[dict[str, Any]]:
    validator = Draft202012Validator(schema)
    entries: list[dict[str, Any]] = []
    seen: dict[str, str] = {}
    for path in sorted((ROOT / "effects").glob("*")):
        if path.suffix != ".yaml":
            rep.error(f"effects/{path.name}", "only .yaml files belong in effects/")
            continue
        try:
            entry = yamlio.load(path)
        except Exception as exc:  # noqa: BLE001 - report YAML errors with the file name
            rep.error(f"effects/{path.name}", f"YAML error: {exc}")
            continue
        if not isinstance(entry, dict):
            rep.error(f"effects/{path.name}", "file is empty or not a mapping")
            continue
        schema_errors = sorted(validator.iter_errors(entry), key=lambda e: list(e.path))
        for err in schema_errors:
            loc = "/".join(str(p) for p in err.path) or "(top)"
            rep.error(f"effects/{path.name}", f"{loc}: {err.message}")
        if schema_errors:
            continue
        key = entry["id"].lower()
        if key in seen:
            rep.error(f"effects/{path.name}", f"id already used by {seen[key]}")
        seen[key] = path.name
        check_entry(entry, path, ids, origins, rep)
        entries.append(entry)

    known = {e["id"] for e in entries}
    for entry in entries:
        for used in entry["uses"]:
            if used not in known:
                rep.error(f"effects/{seen[entry['id'].lower()]}", f"uses unknown entry {used!r}")
    names = sorted({a for e in entries for a in e["authors"]}
                   | {t["author"] for e in entries for t in e["text"].values() if t.get("author")})
    for name in names:
        if name not in notice:
            rep.error("NOTICE.md", f"author {name!r} is missing from the contributor list")
    return entries


def ordered(entry: dict[str, Any]) -> dict[str, Any]:
    return {k: entry[k] for k in ENTRY_ORDER if k in entry}


def build_meta(dataset: dict[str, Any], entries: list[dict[str, Any]], vocab: dict[str, Any],
               version: str) -> dict[str, Any]:
    payload = json.dumps([entries, vocab], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    licenses = [dataset["license"]]
    origins = []
    for key, info in dataset.get("origins", {}).items():
        count = sum(1 for e in entries if e.get("origin") == key)
        if not count:
            continue
        origins.append({"key": key, **info, "entries": count})
        if info["license"] not in licenses:
            licenses.append(info["license"])
    attribution = dataset["copyright"]
    if origins:
        attribution += "; contains " + "; ".join(
            f"{o['title']} by {o['attribution']} ({o['license']})" for o in origins)
    return {
        "title": dataset["title"],
        "description": dataset["description"],
        "version": version,
        "fingerprint": hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16],
        "license": " AND ".join(licenses),
        "licenseUrl": dataset["licenseUrl"],
        "attribution": attribution,
        "notice": dataset["notice"],
        "source": dataset["source"],
        "effects": sum(1 for e in entries if e["kind"] == "effect"),
        "applications": sum(1 for e in entries if e["kind"] == "application"),
        "cells": len({c for e in entries for c in e["functions"]}),
        "parameterCells": len({c for e in entries for c in e["parameters"]}),
        "languages": sorted({lang for e in entries for lang in e["text"]}),
        "origins": origins,
    }


def write_json(data: Any, path: Path) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate only, write nothing")
    parser.add_argument("--version", default="dev", help="release version, e.g. 2026.12.0")
    parser.add_argument("--out", default="dist", help="output directory (default: dist)")
    args = parser.parse_args()

    rep = Report()
    dataset = yamlio.load(ROOT / "dataset.yaml")
    schema = json.loads((ROOT / "schema" / "effect.schema.json").read_text(encoding="utf-8"))
    notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
    vocab, ids = load_vocabulary(rep)
    entries = load_entries(schema, ids, dataset.get("origins", {}), notice, rep)

    for w in rep.warnings:
        print(f"warning: {w}")
    for e in rep.errors:
        print(f"error:   {e}")
    if rep.errors:
        print(f"\n{len(rep.errors)} error(s) in {len(entries)} valid entries - nothing written.")
        return 1

    entries = sorted((ordered(e) for e in entries), key=lambda e: e["id"])
    meta = build_meta(dataset, entries, vocab, args.version)
    print(f"OK: {meta['effects']} effects, {meta['applications']} applications, "
          f"{meta['cells']} function cells, {meta['parameterCells']} parameter cells, "
          f"licence {meta['license']}, fingerprint {meta['fingerprint']}.")
    if args.check:
        return 0

    out = (ROOT / args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    write_json({"meta": meta, "effects": entries}, out / "effects.json")
    write_json(vocab, out / "vocabulary.json")
    shutil.copyfile(ROOT / "NOTICE.md", out / "NOTICE.md")
    shutil.copyfile(ROOT / "LICENSE", out / "LICENSE")
    print(f"Wrote {out / 'effects.json'} (version {args.version}) and vocabulary.json, NOTICE.md, LICENSE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
