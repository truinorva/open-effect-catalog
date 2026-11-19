# NOTICE — Open Effect Catalog

Open Effect Catalog
Copyright (c) 2026 Truinorva GmbH and the contributors named below.

This file is the **single place of attribution** for the whole data set.
Nobody who uses or passes on the data has to credit entries one by one.

## Licences at a glance

| Part | Licence |
| --- | --- |
| Tooling, schema, workflows, documentation, and every entry written for this project (entries without an `origin` field) | MIT — see [`LICENSE`](LICENSE) |
| Entries with `origin: triz-consulting`, and the vocabulary in `vocabulary/` | CC BY 4.0 — see [Third-party data](#third-party-data) |

The release file `effects.json` states the combined licence in `meta.license`
(currently `MIT AND CC-BY-4.0`) and lists every upstream collection with its
entry count in `meta.origins`.

## How to attribute

Include this NOTICE file (or a link to it) together with `LICENSE` when you
pass on the data or a product built on it. In an imprint, an "Open-source
licences" page or an About box, one line is enough:

> Open Effect Catalog — © 2026 Truinorva GmbH and contributors, MIT License.
> Contains the TRIZ Effects Database by Robert Adunka, TRIZ Consulting Group,
> licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), modified.

German version:

> Open Effect Catalog unter MIT-Lizenz, Copyright 2026 Truinorva GmbH und
> Mitwirkende. Enthält die TRIZ Effects Database von Robert Adunka, TRIZ
> Consulting Group, unter CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), verändert.

CC BY 4.0 lets attribution be given "in any reasonable manner based on the
medium, means, and context" (section 3(a)(2)), for example through a link to a
page that carries it. That is what this central notice is for. The `authors`
field stays in every entry as data; you need not display it.

## Third-party data

### TRIZ Effects Database

- **Attribution:** Robert Adunka, TRIZ Consulting Group
- **Source:** https://www.triz-consulting.de/EffectsDatabase/ (data version 2026-11-11, vocabulary version 2.1.1)
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0),
  https://creativecommons.org/licenses/by/4.0/
- **Covers:** every file in `effects/` with `origin: triz-consulting`, and `vocabulary/vocabulary.yaml`
- **Changes:** converted from `effects.json` and `functions.json` into one YAML
  file per entry and one vocabulary file; wording and cell allocations were not
  changed at import. All later changes are recorded in the git history of this
  repository.
- **Disclaimer:** the licensor offers the material as-is and as-available and
  makes no representations or warranties of any kind (CC BY 4.0, section 5).

## Contributors

Authors of entries, in alphabetical order. `tools/build.py` fails if an
author named in an entry is missing here — add yourself with your first entry.

- Adrian Fischer
- Eric Dirk Pryputsch
- Finn-Ole Jensen
- Obaidullah Sharifi
- Philipp Mahncke
- Robert Adunka
- Tabitha Adunka
- Till Wersig
- Tim Jacobsen
- Tim Kunkelmann
- Walid Sayd

Maintained by Truinorva GmbH.
