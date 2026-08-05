# `analysis_v2.py` provenance cell design

Date: 2026-08-04

Status: Revised after implementation-plan review; pending approval

## Context

`diabetes/analysis_v2.py` depends on large, local simulation results that are intentionally excluded from Git. A committed PDF should therefore identify the exact notebook and software environment used for its most recent successful execution without publishing `diabetes/results/`.

## Considered approaches

1. **Runtime provenance table — selected.** Generate a concise visible table whenever the notebook executes. This cannot silently retain an old timestamp and provides enough information to identify the source and principal software environment.
2. **Hard-coded export annotation.** Edit a timestamp before each export. This is simpler internally but can become stale and does not identify the runtime environment reliably.
3. **Complete environment manifest.** Embed all installed packages. This maximizes detail but would overwhelm the notebook and distract from the analysis; the lockfile already serves that purpose.

## Design

Add one hidden-code marimo cell near the beginning of the notebook, under the existing Dependencies heading. Its visible output will be a compact Markdown table containing:

- execution timestamp in ISO 8601 format, including the local UTC offset;
- Python version;
- marimo, NumPy, pandas, Matplotlib, and SciPy versions;
- current Git commit;
- Git working-tree state (`clean` or `dirty`);
- SHA-256 digest of `diabetes/analysis_v2.py`.

The values will be obtained at execution time using Python's standard library and `importlib.metadata`; the cell will not import the analysis libraries a second time. This avoids duplicate marimo variable definitions. The notebook header will also be refreshed from marimo 0.17.8 to the installed 0.23.16 format when the file is saved.

The cell will define named `collect_provenance()` and `format_provenance_markdown()` functions, then render the formatted result. The formatter will build Markdown without an indented multiline template so interpolated rows cannot disable dedenting and turn the table into a code block. A focused test will pass the formatted string through `mo.md()` and require a real HTML `<table>`.

Keeping collection and formatting independent of marimo presentation makes both directly testable through the repository's existing AST-based notebook test pattern. Because that harness extracts and executes only the selected `ast.FunctionDef`, every standard-library import needed by `collect_provenance()` will be inside the function body rather than at cell scope. No other cell consumes either function, so the generated marimo cell will use a bare return. The cell will not inspect, summarize, embed, or upload any file under `diabetes/results/`.

## Data flow and failure handling

The cell passes its `__file__` path to the collector. The collector resolves that source path first, derives the repository root by running `git rev-parse --show-toplevel` from the source file's directory, records `git rev-parse HEAD`, and uses `git status --porcelain` for the clean/dirty state. This remains correct when the caller's current directory is not the repository root.

A missing package version, Git command, or source file will be represented as `unavailable`; provenance collection must not abort the statistical analysis. The final PDF validation must nevertheless reject any `unavailable` value and require `Git state` to be exactly `clean`.

## PDF prerequisites and export policy

The machine does not have pandoc or XeLaTeX, so PDF generation intentionally uses marimo's WebPDF path. Create a `[dependency-groups]` development group containing Playwright so its Python version is locked, and install its matching Chromium runtime once with `uv run playwright install chromium`. `nbformat` and `nbconvert` are already locked through the existing project dependencies and need no change. Playwright and the browser are prerequisites, not analysis inputs; neither receives data from `diabetes/results/`.

The export will be run from the repository root with outputs enabled, WebPDF selected explicitly, code inputs omitted, and marimo output rasterization disabled. `--no-rasterize-outputs` preserves the provenance table as searchable PDF text; static Matplotlib image outputs remain available to WebPDF.

Each complete export is expected to take 4–8 minutes. Agentic execution will poll at least once per minute and wrap the command in a 15-minute hard timeout; a timeout is a failed export requiring partial-output inspection before any retry.

Marimo export also writes `diabetes/__marimo__/session/analysis_v2.py.json`, a large derived snapshot that can embed executed outputs. This file is not part of the curated publication artifact and will be ignored explicitly in `.gitignore`; the existing tracked legacy session snapshot remains untouched. Validation will require the new snapshot to be ignored and untracked rather than treating it as an unexpected status entry.

## Environment migration and generated outputs

The notebook writes 36 tracked files under `diabetes/figures/` and `diabetes/csv_results/` during execution. Those files were committed with the notebook at `8119d00`, but the current environment has moved from Matplotlib 3.10.3 to 3.11.1 and to pandas 3.0.5. A byte-identical first regeneration is therefore impossible for PNGs and cannot be assumed for CSV serialization.

Use a two-run migration:

1. Settle the marimo lockfile upgrade, add the Playwright development dependency, add the provenance implementation and tests, update the README, and commit these non-generated changes.
2. From that clean state, perform a baseline export that intentionally refreshes generated CSVs and PNGs; discard its PDF.
3. Review the refresh semantically. Compare CSV schemas, nonnumeric fields, and numeric values rather than raw serialization alone. Compare PNG dimensions and pixel content independently of metadata, then visually inspect any rendering differences. If a reported estimate changes materially, stop and reconcile the notebook, manuscript, and reviewer response before accepting the refresh.
4. Commit the accepted refreshed outputs as the new 0.23.16 baseline.
5. From the resulting clean state, perform the final export. On this second run, require byte-identical generated outputs; any difference is then a determinism failure.

Both PDFs are first written outside the repository. Only the validated final PDF is copied to its stable repository path.

## Validation

1. Resolve the marimo lockfile drift and create the Playwright development group, then sync the environment and install the locked browser runtime with `uv run playwright install chromium`.
2. Add `collect_provenance()`, `format_provenance_markdown()`, their presentation cell, the session-snapshot ignore rule, the README instructions, and unit tests covering normal collection, the source digest, the clean/dirty indicator, graceful degradation, and actual `<table>` rendering through `mo.md()`.
3. Run the focused provenance tests, the existing `analysis_v2` tests, and marimo's strict notebook check.
4. Commit the dependency, notebook, test, and README changes without refreshing generated outputs.
5. Confirm the tracked worktree is clean and preserve the committed pre-migration generated outputs for semantic comparison.
6. From the repository root, perform the baseline refresh with `timeout --signal=TERM 15m uv run marimo export pdf --include-outputs --webpdf --no-include-inputs --no-rasterize-outputs diabetes/analysis_v2.py -o /tmp/analysis_v2_baseline_refresh.pdf -f`.
7. Review CSVs semantically and PNGs by dimensions, pixels, and visual appearance; reconcile any material result change with the manuscript before proceeding.
8. Commit the accepted generated-output refresh, confirm the worktree is clean, and record its SHA-256 manifest as the new baseline.
9. From the repository root, perform the final export with `timeout --signal=TERM 15m uv run marimo export pdf --include-outputs --webpdf --no-include-inputs --no-rasterize-outputs diabetes/analysis_v2.py -o /tmp/analysis_v2_last_run.pdf -f`.
10. Confirm the final export finishes successfully against the local ignored results.
11. Require the second run's tracked CSVs and PNGs to match the new baseline byte-for-byte, and stop on any unexpected tracked or untracked output.
12. Extract and inspect PDF text to verify every timestamp/version/commit/digest value is present and searchable, no value is `unavailable`, and Git state is exactly `clean`.
13. Render and visually inspect all PDF pages, including the analysis figures.
14. Confirm `diabetes/results/` and the analysis-v2 marimo session snapshot remain ignored and untracked, then copy the validated PDF to `diabetes/analysis_v2_last_run.pdf`.

## Repository presentation

Store the artifact as `diabetes/analysis_v2_last_run.pdf`; its internal provenance table identifies the run, so timestamped filenames do not accumulate in the working tree. Because each timestamp changes the binary, every committed re-export still adds a new PDF blob to Git history. Regenerate the committed snapshot only for meaningful changes to the notebook, data, or execution environment.

Update the README to:

- replace the stale `diabetes/analysis.py` reference with `diabetes/analysis_v2.py`;
- link the latest executed PDF snapshot;
- state that raw results remain local and ignored;
- document the Playwright/Chromium prerequisite;
- document the exact export command and required repository-root working directory.
