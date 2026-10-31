# paper/

## What to edit

`manuscript.md` is **generated** — your edits there will be overwritten.
Write these instead:

| File | Section |
|---|---|
| `sections/abstract.md` | Abstract |
| `sections/introduction.md` | Introduction |
| `sections/discussion.md` | Discussion |

Methods, Results and Limitations are built from `results/`, so no number in
this paper is typed by hand. If an analysis is re-run, the figures update
everywhere and your prose is untouched. A section file that does not exist
falls back to a clearly-marked outline, so the manuscript always builds.

## Before editing, read

- `../docs/PARAMETERS.md` — every value, cited to its figure, table or methods
  section, plus the parameters the source does **not** report.
- `../results/GATE.md` — why the project continued, and the two explanations
  the published data cannot separate.

## After editing

```
.venv\Scripts\python scripts\independence_check.py
.venv\Scripts\python scripts\retention_structure.py
.venv\Scripts\python scripts\build_manuscript.py
```

## The one thing not to let slip

The headline comparison uses **no fitted parameters** — it is two of the
source's own measurements multiplied together. That is the paper's strength
and it should survive rewriting. Resist the temptation to claim the gap proves
correlated partitioning: §3.2 shows copy number explains it equally well, and
the data cannot choose.

## Before posting as a preprint

The data-availability section currently says the repository is private and the
code is available on request. That is true while the manuscript circulates
privately, and it builds a clean PDF.

**When you post, three things change:**

1. Make `jsamonte/spudcell-twin` public on GitHub.
2. In `scripts/build_manuscript.py`, replace the "currently private" sentence
   in section 6 with the repository URL.
3. Rebuild and re-render.

This reminder lives here rather than in the manuscript because a `>>>`
instruction in the text blocks `build_pdf.py` entirely — which is correct
before posting and wrong before a private read.

Note that making the repository public exposes the full commit history,
including the author email addresses in it.

## Word versions

`paper/manuscript.docx` and `paper/breeder_guide.docx` are built from the
Markdown by `scripts/build_docx.js`, which needs the `docx` npm package:

    npm install docx
    node scripts/build_docx.js paper/manuscript.md paper/manuscript.docx --line-numbers
    node scripts/build_docx.js paper/breeder_guide.md paper/breeder_guide.docx

The build drops the repo-only notes (the "generated from results/" line and the
"reproduce every number" line) so they do not reach a reader.

**These .docx files are generated.** Edits made in Word are overwritten the next
time the script runs. When a collaborator returns an edited Word file, keep it
under a new name and fold the changes back into `paper/sections/*.md` by hand.
