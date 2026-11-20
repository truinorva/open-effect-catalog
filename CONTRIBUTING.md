# Contributing

Thank you for helping. Every entry is a small text of its own, so the rules
below are mostly about where the text comes from.

## The rules that matter: own wording, own allocation, human review

1. **No copied text.** Sources (Wikipedia, textbooks, papers) are for looking
   the facts up. Physical facts are free; somebody else's wording is not. Do
   not paste, and do not paraphrase sentence by sentence.
2. **Nothing from other effect databases or effect catalogs** — online or in
   print. Not their text, not their list of entries, and not their allocation
   of effects to functions. Their selection and allocation are protected
   (in the EU by the database right), even where single facts are not.
   Decide the cells for an entry yourself, from what the effect does.
3. **AI may draft, a person reviews.** An AI may find candidates, draft
   entries and translate. Machine-written text is marked `kind: maschinell`
   with the model in `model`; a pure machine draft has an empty `authors`
   list, so no person's name stands over text nobody has read. **Nothing goes
   into a release before a person has reviewed it** (see below).

Pull requests that break these rules are closed, however good the content.

## Adding an entry

Search first (on GitHub press `T` and type the name): duplicates are rejected.

**In the browser:** copy [`templates/new-effect.yaml`](templates/new-effect.yaml),
create `effects/<id>.yaml` with "Add file → Create new file", paste the
template and replace every placeholder. The comments in the template explain
each field.

**Locally:**

```bash
python tools/new_effect.py <id> --name-en "..." --name-de "..." --author "Your Name" --source <url>
```

- **id**: English, lower case, words joined by hyphens, e.g. `acoustic-levitation`.
  It equals the file name and never changes once merged.
- **functions**: every `action|object` cell the effect can fulfil. The ids are
  in `vocabulary/vocabulary.yaml`. A verb belongs to a cell only if the effect
  changes or maintains a parameter of that object.
- **home**: the cell where you came across the effect; must be one of `functions`.
- **parameters**: the independent second view, `operation|parameter`.
- **text**: at least the language you write in; `name` and `description` are
  required. `example`, `conditions`, `limits` and `sideEffects` are worth
  filling in — limits and side effects are what make an entry useful.
- **sources**: where a reader can check the facts.
- **authors**: your name. Add it to the contributor list in `NOTICE.md` too;
  the build fails otherwise.

Then run:

```bash
python tools/build.py --check
```

## Editing an entry

Edit the YAML file directly — on GitHub in the browser is fine. Set `updated`
to today's date in every language block you changed. If you substantially
rewrite an entry, add your name to `authors`.

Entries with `origin: triz-consulting` were written by Robert Adunka and his
co-authors for the TRIZ Effects Database and are used here under MIT with his
permission. They may be improved here like any other entry.

## Reviewing an entry

Every entry has a review flag. `tools/build.py` puts only entries with
`review.status: geprueft` into a release; drafts stay in the repository.

```yaml
review:
  status: geprueft          # geprueft | ungeprueft
  by:
    - Your Name             # also listed in NOTICE.md
  date: '2026-11-19'
```

Before you set `geprueft`, check:

- **Facts:** every statement holds up against the sources; add a source if
  one is missing.
- **Wording:** nothing is copied — search one distinctive sentence on the web.
  Rewrite what reads like a translation of someone else's text.
- **Cells:** each function cell is justified by what the effect does to that
  object; `home` is one of them; parameter cells fit.
- **Languages:** read every language version and set its `kind` from
  `maschinell` to `geprueft` (the build refuses a reviewed entry with unread
  machine text).

If you rewrote a draft substantially, add yourself to `authors` as well.

Entries imported from the TRIZ Effects Database count as reviewed: TRIZ
Consulting Group releases every entry through a reviewer before publishing it.

## Changing the vocabulary

`vocabulary/vocabulary.yaml` was taken over once from the TRIZ Effects
Database (version 2.1.1) and has been maintained here since 2026-11-20.
`tools/import_tcg.py` does not overwrite it; it only reports how the upstream
vocabulary differs.

- Labels, hints and synonyms may be reworded at any time.
- Ids never change: every cell in `effects/` refers to them.
- A new action, object, operation or parameter is added by pull request.
  Explain which effects need it. Object and parameter ids must never overlap;
  the build checks this.

## Branches and pull requests

Work on a branch, open a pull request against `main`. A maintainer reviews the
content (facts, own wording, cell allocation) and merges. Releases are tagged
from `main`.

## Licence of contributions

By opening a pull request you agree that your contribution is published under
the MIT License of this repository (see `LICENSE`) and that you have the right
to do so.
