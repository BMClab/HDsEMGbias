# `analysis_v2.py` provenance cell design

Date: 2026-08-04

Status: Approved for implementation

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
- SHA-256 digest of `diabetes/analysis_v2.py`.

The values will be obtained at execution time using Python's standard library and package metadata. The cell will not inspect, summarize, embed, or upload any file under `diabetes/results/`.

## Data flow and failure handling

The cell reads installed package metadata, the notebook source bytes, and the local Git revision, then renders a Markdown table through marimo. A missing package version or unavailable Git command will be represented as `unavailable`; provenance collection must not abort the statistical analysis. Failure to read the notebook source is handled the same way.

## Validation

1. Run marimo's strict notebook check.
2. Export the notebook through marimo's native PDF exporter with outputs enabled and code inputs omitted.
3. Confirm the export finishes successfully against the local ignored results.
4. Extract and inspect the PDF text to verify the timestamp, versions, commit, and source digest are present.
5. Render and visually inspect all PDF pages, including the analysis figures.
6. Confirm `diabetes/results/` remains ignored and no raw result files enter Git status.

## Repository presentation

Store the stable artifact as `diabetes/analysis_v2_last_run.pdf`; its internal provenance table identifies the run, so timestamped filenames do not accumulate. Update the README to link the current notebook and executed PDF snapshot while explaining that raw results remain local.
