# Contributing

Thank you for helping. Every entry is a small text of its own, so the rules
below are mostly about where the text comes from.

## The one rule that matters: own wording, own allocation

1. **Write every sentence yourself.** Sources (Wikipedia, textbooks, papers)
   are for looking the facts up. Physical facts are free; somebody else's
   wording is not. Do not paste, and do not paraphrase sentence by sentence.
2. **Nothing from other effect databases or effect catalogs** — online or in
   print. Not their text, not their list of entries, and not their allocation
   of effects to functions. Their selection and allocation are protected
   (in the EU by the database right), even where single facts are not.
   Decide the cells for an entry yourself, from what the effect does.
3. **AI may help, but not write.** An AI may help to find candidate effects and
   to translate. A machine translation is marked `kind: maschinell` with the
   model in `model`; once a person has read and corrected it, set
   `kind: geprueft`. Entries are written by people.

Pull requests that break these rules are closed, however good the content.

## Adding an entry

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

## Branches and reviews

Work on a branch, open a pull request against `main`. A maintainer reviews the
content (facts, own wording, cell allocation) and merges. Releases are tagged
from `main`.

## Licence of contributions

By opening a pull request you agree that your contribution is published under
the MIT License of this repository (see `LICENSE`) and that you have the right
to do so.
