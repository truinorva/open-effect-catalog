# Changelog

Versions follow `YYYY.MM.N`. Each release lists the entries that were added,
changed or removed.

## Unreleased

- Repository set up: one YAML file per entry, JSON Schema, vocabulary,
  validation and build (`tools/build.py`), release workflow.
- Imported 51 effects and 3 applications from the TRIZ Effects Database by
  Robert Adunka, TRIZ Consulting Group (data version 2026-11-11, CC BY 4.0),
  together with its vocabulary (version 2.1.1).
- Review flag: every entry carries `review.status` (`geprueft` | `ungeprueft`).
  Only reviewed entries go into a release. Entries from the TRIZ Effects
  Database count as reviewed (TRIZ Consulting Group releases each entry
  through a reviewer).
- AI may draft entries; machine text is marked `kind: maschinell` with the
  model, and a pure draft names no author. A person reviews before release.
- Duplicate check: no two entries may share a name in any language.
- 895 AI drafts (489 effects, 406 applications), not reviewed and therefore
  not released. Names and Wikipedia links come from Truinorva's candidate
  list; descriptions, examples, limits and cell allocations are newly
  written. Candidates that duplicate a TRIZ Effects Database entry were left
  out (the curated entry takes precedence), and duplicates among the drafts
  were merged.
