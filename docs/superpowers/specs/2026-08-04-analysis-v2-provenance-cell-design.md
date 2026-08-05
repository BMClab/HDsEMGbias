# `analysis_v2.py` provenance cell design

Date: 2026-08-04

Status: Revised after review; pending approval

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

The cell will define a named `collect_provenance()` function and then render its result. Keeping the collection logic named and independent of marimo presentation makes success and failure behavior directly testable through the repository's existing AST-based notebook test pattern. The cell will not inspect, summarize, embed, or upload any file under `diabetes/results/`.

## Data flow and failure handling

The cell reads installed package metadata, the notebook source bytes, and the local Git revision, then renders a Markdown table through marimo. It records both `git rev-parse HEAD` and whether `git status --porcelain` reports changes, so a commit is never presented as a complete description of a dirty run. A missing package version or unavailable Git command will be represented as `unavailable`; provenance collection must not abort the statistical analysis. Failure to read the notebook source is handled the same way.

## PDF prerequisites and export policy

The machine does not have pandoc or XeLaTeX, so PDF generation intentionally uses marimo's WebPDF path. Add Playwright as a project development dependency so its Python version is locked, and install its matching Chromium runtime once with `playwright install chromium`. Playwright and the browser are prerequisites, not analysis inputs; neither receives data from `diabetes/results/`.

The export will be run from the repository root with outputs enabled, code inputs omitted, and marimo output rasterization disabled. `--no-rasterize-outputs` preserves the provenance table as searchable PDF text; static Matplotlib image outputs remain available to WebPDF.

The notebook writes 36 tracked files under `diabetes/figures/` and `diabetes/csv_results/` during execution. Their expected outcome is byte-identical regeneration. Before export, record their SHA-256 manifest and start from a clean tracked state. After export, compare the manifest and Git status; any changed tracked output or unexpected untracked output is a red flag that stops publication for review. The PDF is first written outside the repository and copied to its stable repository path only after all checks pass.

## Validation

1. Add unit tests for `collect_provenance()` covering normal collection, the source digest, the clean/dirty indicator, and graceful degradation when package, Git, or source metadata is unavailable.
2. Run the focused provenance tests and the existing `analysis_v2` tests.
3. Run marimo's strict notebook check.
4. Record hashes for all tracked generated CSV and PNG outputs, and confirm the tracked worktree is clean before execution.
5. From the repository root, export with `uv run marimo export pdf --no-include-inputs --no-rasterize-outputs diabetes/analysis_v2.py -o /tmp/analysis_v2_last_run.pdf -f`.
6. Confirm the export finishes successfully against the local ignored results.
7. Compare generated-output hashes and full Git status with the pre-export state; stop if any tracked output differs or any unexpected file appears.
8. Extract and inspect PDF text to verify the timestamp, versions, commit, dirty indicator, and source digest are present and searchable.
9. Render and visually inspect all PDF pages, including the analysis figures.
10. Confirm `diabetes/results/` remains ignored and no raw result files enter Git status, then copy the validated PDF to `diabetes/analysis_v2_last_run.pdf`.

## Repository presentation

Store the artifact as `diabetes/analysis_v2_last_run.pdf`; its internal provenance table identifies the run, so timestamped filenames do not accumulate in the working tree. Because each timestamp changes the binary, every committed re-export still adds a new PDF blob to Git history. Regenerate the committed snapshot only for meaningful changes to the notebook, data, or execution environment.

Update the README to:

- replace the stale `diabetes/analysis.py` reference with `diabetes/analysis_v2.py`;
- link the latest executed PDF snapshot;
- state that raw results remain local and ignored;
- document the Playwright/Chromium prerequisite;
- document the exact export command and required repository-root working directory.
