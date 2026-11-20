# Open Effect Catalog

An open catalog of physical, chemical, biological and geometric **effects**,
searchable by function. Ask "how do I *move* a *liquid*?" and get every effect
that can do it, with a short explanation, an example, its limits and side
effects, in German and English. Made for function-oriented search in TRIZ,
engineering design and everyday problem solving.

- **One file per entry.** Every effect lives in `effects/<id>.yaml` and can be
  edited, reviewed and discussed on its own.
- **One file per release.** A tag bundles all entries into a single
  `effects.json` attached to the GitHub Release.
- **Reviewed before release.** Every entry carries a review flag. Drafts —
  also AI drafts — may live in the repository, but only entries a person has
  checked go into a release.
- **Attribution in one place.** Credit is given once, centrally, in
  [`NOTICE.md`](NOTICE.md), not per entry.

> **Kurz auf Deutsch:** Offener Effektkatalog: physikalische, chemische,
> biologische und geometrische Effekte, gesucht nach Funktion. Jeder Effekt ist eine
> eigene YAML-Datei unter `effects/`; ein Release packt alle Einträge in eine
> `effects.json`. Die Namensnennung steht gesammelt in `NOTICE.md`, nicht an
> jedem Effekt.

## How the data is organised

Each entry is found in two independent grids:

- **Function view:** *action × object*, e.g. `move|liquid`, `hold|particles`.
  27 actions in six groups (position and movement, shape, cohesion, matter,
  thermal, sensing) and five objects (solid, particles, liquid, gas, field).
- **Parameter view:** *operation × parameter*, e.g. `increase|speed`,
  `change|orientation`.

The vocabulary for both views lives in
[`vocabulary/vocabulary.yaml`](vocabulary/vocabulary.yaml). It was taken over
once from the TRIZ Effects Database (version 2.1.1) and is maintained in this
repository; changes go through pull requests like any entry. Its ids are
stable; labels, hints and synonyms may be reworded at any time.

```text
effects/                one YAML file per effect or application
vocabulary/             actions, objects, operations, parameters (maintained here)
templates/new-effect.yaml  commented template for a new entry
schema/                 JSON Schema for an entry (editors validate as you type)
dataset.yaml            release metadata and upstream collections
tools/build.py          validate everything and bundle dist/effects.json
tools/new_effect.py     create an empty entry to fill in
tools/import_tcg.py     re-sync entries from the TRIZ Effects Database (not the vocabulary)
NOTICE.md               licences, attribution, contributors
```

### An entry

```yaml
# yaml-language-server: $schema=../schema/effect.schema.json
id: acoustic-levitation
kind: effect                 # effect | application
home: hold|liquid            # the cell where the entry was first found
functions:                   # every action|object cell it can fulfil
  - hold|liquid
  - move|particles
parameters:                  # every operation|parameter cell
  - change|position
uses: []                     # applications: ids of the effects they rely on
domain: {id: Physik, de: Physik, en: Physics}
maturity: ''                 # lehrbuch | nische | verbreitet (applications: kindheit … niedergang)
sources:
  - https://de.wikipedia.org/wiki/Levitation_(Technik)#Akustische_Levitation
authors:
  - Robert Adunka
origin: triz-consulting      # only for entries taken over from another collection
review:                      # only geprueft entries are released
  status: geprueft           # geprueft | ungeprueft
  by: [TRIZ Consulting Group]
  date: '2026-11-11'
text:
  de:
    name: Akustische Levitation
    description: >-
      Eine Probe wie Styroporkügelchen oder Wassertropfen …
    example: Ultraschallluftlager
    kind: original           # original | geprueft | maschinell
    updated: '2026-09-16'
  en:
    name: Acoustic levitation
    …
```

The field names follow the
[TRIZ Effects Database](https://www.triz-consulting.de/EffectsDatabase/) of
TRIZ Consulting Group, so a release `effects.json` and `vocabulary.json` can be
read by its web viewer without conversion.

## Using a release

Download `effects.json` from the
[latest release](https://github.com/truinorva/open-effect-catalog/releases/latest).
It contains a `meta` block (version, fingerprint, licence, attribution,
upstream collections, counts) and the `effects` array. `vocabulary.json` holds
the labels for every cell id.

Please keep [`NOTICE.md`](NOTICE.md) and [`LICENSE`](LICENSE) with the data, or
link to them. One line on your licences page is enough; NOTICE.md has the
wording in English and German.

## Working on the data

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt        # Windows: .venv\Scripts\pip
python tools/build.py --check                     # validate every entry
python tools/build.py                             # write dist/effects.json
```

`build.py` checks every file against the schema, every cell against the
vocabulary, every `uses` link, that each id equals its file name, that no two
entries share a name (duplicates), and that every author and reviewer is
listed in NOTICE.md. The release contains only reviewed entries. CI runs the
same check on each pull request.

To add an entry, copy [`templates/new-effect.yaml`](templates/new-effect.yaml)
to `effects/<id>.yaml` and fill it in — on GitHub in the browser is fine. Or,
locally:

```bash
python tools/new_effect.py magnetostriction --name-en Magnetostriction --name-de Magnetostriktion --author "Your Name" --source https://en.wikipedia.org/wiki/Magnetostriction
```

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first — especially the rule on
**own wording**.

## Releasing

Releases use calendar versions: `vYYYY.MM.N`, e.g. `v2026.12.0`.

```bash
git tag v2026.12.0
git push origin v2026.12.0
```

The workflow validates, builds with that version and attaches `effects.json`,
`vocabulary.json`, `NOTICE.md` and `LICENSE` to the release.

## Licence

Released under the **MIT License** — see [`LICENSE`](LICENSE). Anyone may use,
change and pass on the data, also commercially and inside closed products, as
long as the licence notice stays with it.

The first entries and the vocabulary were written by **Robert Adunka (TRIZ
Consulting Group)** and his co-authors for the
[TRIZ Effects Database](https://www.triz-consulting.de/EffectsDatabase/) and
are used here under MIT with his permission. All contributors and a ready-made
attribution line: [`NOTICE.md`](NOTICE.md).

© 2026 Truinorva GmbH, TRIZ Consulting Group GmbH, Robert Adunka and contributors.
