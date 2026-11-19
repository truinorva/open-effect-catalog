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
- 10 AI drafts (not reviewed, not released): magnetostriction,
  piezoelectric-effect, seebeck-effect, peltier-effect, leidenfrost-effect,
  venturi-effect, triboelectric-effect, hall-effect, ferrofluid,
  brazil-nut-effect.
