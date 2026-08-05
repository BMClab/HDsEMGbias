# `analysis_v2.py` Provenance PDF Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add testable runtime provenance to `analysis_v2.py`, establish a reviewed output baseline under the upgraded environment, and commit a searchable, visually verified PDF of the latest successful run without publishing raw results.

**Architecture:** A single hidden-code marimo cell owns function-local provenance collection plus a flat Markdown formatter whose HTML table output is tested. The PDF workflow uses two executions: an intentional environment-migration refresh followed by a clean deterministic export whose provenance and generated outputs are verified before the PDF enters the repository; marimo's derived session snapshot remains local and ignored.

**Tech Stack:** Python 3.12, marimo 0.23.16, `importlib.metadata`, Git, uv dependency groups, Playwright/Chromium WebPDF, unittest, pandas, NumPy, Pillow, Poppler tools.

## Global Constraints

- Run every notebook and export command from the repository root: `/home/marcos/github/bmclab/HDsEMGbias`.
- Keep `diabetes/results/` local and git-ignored; never stage, copy, embed, or upload raw results.
- Ignore `diabetes/run_model.py`; do not run or modify it.
- Use `diabetes/analysis_v2.py` as the only current diabetes analysis notebook.
- The final PDF must omit code inputs, include executed outputs, use WebPDF explicitly, and preserve provenance as searchable text.
- `diabetes/__marimo__/session/analysis_v2.py.json` may contain derived outputs and must remain ignored and untracked.
- The initial 0.23.16 run is an intentional generated-output migration; only the second run must be byte-identical to its committed baseline.
- Any material change to reported estimates stops the workflow until the notebook, manuscript, and reviewer response are reconciled.
- Each full export is expected to take 4–8 minutes, has a 15-minute hard timeout, and must be polled at least once per minute so a long computation is not mistaken for a hang.
- Commit task-scoped files only; do not push unless the user asks.

---

### Task 1: Lock the PDF export environment

**Files:**
- Modify: `pyproject.toml:1-25`
- Modify: `uv.lock`
- Modify: `.gitignore:120-130`

**Interfaces:**
- Consumes: the user's existing marimo 0.23.16 lockfile update.
- Produces: `marimo>=0.23.16` in project dependencies, a `dev` dependency group containing `playwright>=1.62.0`, an environment capable of invoking WebPDF, and a narrow ignore rule for the analysis-v2 session snapshot.

- [ ] **Step 1: Raise the marimo floor and add the development dependency**

Run:

```bash
uv add "marimo>=0.23.16"
uv add --dev "playwright>=1.62.0"
```

Expected: `[project].dependencies` contains `"marimo>=0.23.16"`, and uv creates:

```toml
[dependency-groups]
dev = [
    "playwright>=1.62.0",
]
```

- [ ] **Step 2: Synchronize and verify the locked tools**

Run:

```bash
uv sync --locked
uv run marimo --version
uv run python -c "import nbconvert, nbformat, playwright; print(nbconvert.__version__, nbformat.__version__, playwright.__file__)"
```

Expected: marimo reports `0.23.16`; all three Python imports succeed.

- [ ] **Step 3: Install Playwright's matching Chromium runtime**

Run:

```bash
uv run playwright install chromium
```

Expected: Chromium installation succeeds. No file under `diabetes/results/` is read or written by this command.

- [ ] **Step 4: Ignore only the derived analysis-v2 session snapshot**

Insert this rule immediately after the existing `diabetes/results/` line so both analysis data boundaries remain together:

```gitignore
# marimo's analysis-v2 session snapshot embeds derived executed outputs.
diabetes/__marimo__/session/analysis_v2.py.json
```

Run:

```bash
git check-ignore -v diabetes/__marimo__/session/analysis_v2.py.json
git ls-files diabetes/__marimo__/session/analysis_v2.py.json
```

Expected: the first command identifies the new rule and the second prints nothing. The existing tracked `analysis_2conds.py.json` remains untouched.

- [ ] **Step 5: Inspect and commit only the environment and data-boundary update**

Run:

```bash
git diff --check
git diff -- pyproject.toml uv.lock .gitignore
git add pyproject.toml uv.lock .gitignore
git diff --cached --check
git commit -m "build: update notebook PDF export environment"
```

Expected: the commit contains the user's marimo lock refresh, the raised marimo floor, the new Playwright development group, and the narrow session-snapshot ignore rule; no generated analysis output is staged.

---

### Task 2: Add tested runtime provenance to the notebook

**Files:**
- Modify: `diabetes/tests/test_analysis_v2_figure_display.py:1-45`
- Modify: `diabetes/analysis_v2.py:1-45`

**Interfaces:**
- Consumes: `load_notebook_function(name)` from the existing AST-based test harness and public `mo.md(...).text` HTML rendering.
- Produces: `collect_provenance(notebook_path, *, now=None, package_version=None, run_git=None) -> dict[str, str]`, `format_provenance_markdown(provenance) -> str`, and a visible HTML table.

- [ ] **Step 1: Write failing provenance tests**

Add these imports to the test module:

```python
import hashlib
from datetime import datetime, timezone
from tempfile import TemporaryDirectory

import marimo as mo
```

Add this test class:

```python
class ProvenanceTest(unittest.TestCase):
    def setUp(self):
        self.collect_provenance = load_notebook_function("collect_provenance")
        self.format_provenance_markdown = load_notebook_function(
            "format_provenance_markdown"
        )
        self.executed_at = datetime(2026, 8, 4, 22, 42, 41, tzinfo=timezone.utc)

    def test_collects_versions_clean_git_state_and_source_digest(self):
        versions = {
            "marimo": "0.23.16",
            "numpy": "1.26.0",
            "pandas": "3.0.5",
            "matplotlib": "3.11.1",
            "scipy": "1.16.3",
        }

        def package_version(name):
            return versions[name]

        with TemporaryDirectory() as directory:
            source = Path(directory) / "diabetes" / "analysis_v2.py"
            source.parent.mkdir()
            source.write_text("print('analysis')\n")

            def run_git(_repo_root, *arguments):
                if arguments == ("rev-parse", "--show-toplevel"):
                    self.assertEqual(Path(_repo_root).resolve(), source.parent.resolve())
                    return directory
                if arguments == ("rev-parse", "HEAD"):
                    return "0123456789abcdef"
                if arguments == ("status", "--porcelain"):
                    return ""
                raise AssertionError(arguments)

            result = self.collect_provenance(
                source,
                now=self.executed_at,
                package_version=package_version,
                run_git=run_git,
            )

        self.assertEqual(result["Executed at"], "2026-08-04T22:42:41+00:00")
        self.assertEqual(result["marimo"], "0.23.16")
        self.assertEqual(result["NumPy"], "1.26.0")
        self.assertEqual(result["pandas"], "3.0.5")
        self.assertEqual(result["Matplotlib"], "3.11.1")
        self.assertEqual(result["SciPy"], "1.16.3")
        self.assertEqual(result["Git commit"], "0123456789abcdef")
        self.assertEqual(result["Git state"], "clean")
        self.assertEqual(
            result["Notebook SHA-256"],
            hashlib.sha256(b"print('analysis')\n").hexdigest(),
        )

    def test_marks_a_dirty_worktree(self):
        def run_git(_repo_root, *arguments):
            if arguments == ("rev-parse", "--show-toplevel"):
                return str(NOTEBOOK.parents[1])
            if arguments == ("rev-parse", "HEAD"):
                return "0123456789abcdef"
            if arguments == ("status", "--porcelain"):
                return " M uv.lock"
            raise AssertionError(arguments)

        result = self.collect_provenance(
            NOTEBOOK,
            now=self.executed_at,
            package_version=lambda _name: "test-version",
            run_git=run_git,
        )

        self.assertEqual(result["Git state"], "dirty")

    def test_formats_a_real_unindented_markdown_table(self):
        markdown = self.format_provenance_markdown(
            {"Executed at": "2026-08-04T22:42:41+00:00", "Git state": "clean"}
        )
        rendered = mo.md(markdown)

        self.assertTrue(
            all(not line.startswith("    ") for line in markdown.splitlines())
        )
        self.assertIn("<table>", rendered.text)
        self.assertIn("<td><code>clean</code></td>", rendered.text)
        self.assertEqual(rendered.text.count("<tr>"), 3)

    def test_degrades_when_package_git_and_source_metadata_are_unavailable(self):
        def unavailable_version(_name):
            raise RuntimeError("metadata unavailable")

        def unavailable_git(_repo_root, *_arguments):
            raise OSError("git unavailable")

        result = self.collect_provenance(
            NOTEBOOK.with_name("missing.py"),
            now=self.executed_at,
            package_version=unavailable_version,
            run_git=unavailable_git,
        )

        for label in ("marimo", "NumPy", "pandas", "Matplotlib", "SciPy"):
            self.assertEqual(result[label], "unavailable")
        self.assertEqual(result["Git commit"], "unavailable")
        self.assertEqual(result["Git state"], "unavailable")
        self.assertEqual(result["Notebook SHA-256"], "unavailable")
```

- [ ] **Step 2: Run the tests and verify the expected failure**

Run:

```bash
uv run python -m unittest diabetes.tests.test_analysis_v2_figure_display.ProvenanceTest -v
```

Expected: FAIL with `missing notebook function: collect_provenance`.

- [ ] **Step 3: Implement the function and visible cell**

Change the notebook header to:

```python
__generated_with = "0.23.16"
```

Insert this single cell immediately after the existing dependency-import cell:

```python
@app.cell(hide_code=True)
def _(mo):
    def collect_provenance(
        notebook_path,
        *,
        now=None,
        package_version=None,
        run_git=None,
    ):
        from datetime import datetime
        import hashlib
        from importlib import metadata
        from pathlib import Path
        import platform
        import subprocess

        if now is None:
            now = datetime.now().astimezone()
        if package_version is None:
            package_version = metadata.version

        if run_git is None:
            def run_git(repo_root, *arguments):
                completed = subprocess.run(
                    ["git", *arguments],
                    cwd=repo_root,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                return completed.stdout.strip()

        source_path = Path(notebook_path).resolve()

        try:
            repo_root = Path(
                run_git(source_path.parent, "rev-parse", "--show-toplevel")
            ).resolve()
        except (OSError, subprocess.CalledProcessError):
            repo_root = None

        provenance = {
            "Executed at": now.isoformat(timespec="seconds"),
            "Python": platform.python_version(),
        }
        packages = {
            "marimo": "marimo",
            "NumPy": "numpy",
            "pandas": "pandas",
            "Matplotlib": "matplotlib",
            "SciPy": "scipy",
        }
        for label, distribution in packages.items():
            try:
                provenance[label] = package_version(distribution)
            except Exception:
                provenance[label] = "unavailable"

        try:
            if repo_root is None:
                raise OSError("repository root unavailable")
            provenance["Git commit"] = run_git(repo_root, "rev-parse", "HEAD")
            status = run_git(repo_root, "status", "--porcelain")
            provenance["Git state"] = "dirty" if status else "clean"
        except (OSError, subprocess.CalledProcessError):
            provenance["Git commit"] = "unavailable"
            provenance["Git state"] = "unavailable"

        try:
            provenance["Notebook SHA-256"] = hashlib.sha256(
                source_path.read_bytes()
            ).hexdigest()
        except OSError:
            provenance["Notebook SHA-256"] = "unavailable"

        return provenance

    def format_provenance_markdown(provenance):
        rows = "\n".join(
            f"| {label} | `{value}` |" for label, value in provenance.items()
        )
        return (
            "### Execution provenance\n\n"
            "| Item | Value |\n"
            "|---|---|\n"
            f"{rows}"
        )

    _provenance = collect_provenance(__file__)
    mo.md(format_provenance_markdown(_provenance))
    return
```

- [ ] **Step 4: Run focused and existing notebook tests**

Run:

```bash
uv run python -m unittest diabetes.tests.test_analysis_v2_figure_display.ProvenanceTest -v
uv run python -m unittest diabetes.tests.test_analysis_v2_figure_display -v
```

Expected: all tests PASS.

- [ ] **Step 5: Run marimo's structural check**

Run:

```bash
uv run marimo check --strict diabetes/analysis_v2.py
```

Expected: zero issues.

- [ ] **Step 6: Commit the tested provenance cell**

Run:

```bash
git diff --check
git add diabetes/analysis_v2.py diabetes/tests/test_analysis_v2_figure_display.py
git diff --cached --check
git commit -m "feat: record notebook execution provenance"
```

Expected: only the notebook and its focused tests are committed.

---

### Task 3: Document and link the reproducible PDF workflow

**Files:**
- Modify: `README.md:60-85`

**Interfaces:**
- Consumes: the locked Playwright dev dependency and provenance-enabled notebook.
- Produces: a repository-root regeneration entrypoint and a stable link to `diabetes/analysis_v2_last_run.pdf`.

- [ ] **Step 1: Replace the stale diabetes notebook section**

Replace the current `diabetes/analysis.py` instructions with:

````markdown
## Diabetes neuropathy analysis

Keep the raw simulation data in `diabetes/results/`. This directory is intentionally git-ignored and is not included in the repository or the PDF snapshot. Marimo's derived `diabetes/__marimo__/session/analysis_v2.py.json` execution snapshot is also intentionally ignored because it can embed large executed outputs; the reviewed PDF is the publication artifact.

Run these commands from the repository root. The current analysis notebook is:

```bash
uv run marimo edit diabetes/analysis_v2.py
```

The [latest executed PDF snapshot](diabetes/analysis_v2_last_run.pdf) records its execution timestamp, software versions, Git state, commit, and notebook SHA-256.

Install the PDF browser runtime once after synchronizing the development environment:

```bash
uv sync --locked
uv run playwright install chromium
```

Generate a candidate PDF outside the repository so failed or unreviewed runs cannot replace the published snapshot. A complete run normally takes 4–8 minutes; this command allows 15 minutes before terminating:

```bash
timeout --signal=TERM 15m uv run marimo export pdf --include-outputs --webpdf --no-include-inputs --no-rasterize-outputs diabetes/analysis_v2.py -o /tmp/analysis_v2_last_run.pdf -f
```

Export executes the notebook and refreshes tracked files under `diabetes/figures/` and `diabetes/csv_results/`. Review those changes and the PDF before copying the validated artifact into place:

```bash
cp /tmp/analysis_v2_last_run.pdf diabetes/analysis_v2_last_run.pdf
```
````

Retain the existing simulation command section, but do not add or reference `run_model.py`.

- [ ] **Step 2: Check the README rendering and links**

Run:

```bash
rg -n "analysis\.py|analysis_v2|analysis_v2_last_run|__marimo__|playwright|timeout|include-outputs|webpdf" README.md
git diff --check
```

Expected: no `diabetes/analysis.py` reference remains; the notebook path, PDF path, ignored session policy, runtime expectation, prerequisites, timeout, and exact export flags are present.

- [ ] **Step 3: Commit the documentation change**

Run:

```bash
git add README.md
git diff --cached --check
git commit -m "docs: document executed notebook snapshot"
```

Expected: README only.

---

### Task 4: Establish the upgraded generated-output baseline

**Files:**
- Modify after review: tracked files under `diabetes/csv_results/`
- Modify after review: tracked files under `diabetes/figures/`
- Ignored local side effect: `diabetes/__marimo__/session/analysis_v2.py.json`
- Temporary only: `/tmp/analysis_v2_baseline_refresh.pdf`
- Temporary only: `/tmp/analysis_v2_pre_refresh_20260804/`
- Temporary only: `/tmp/compare_analysis_v2_outputs.py`

**Interfaces:**
- Consumes: a clean worktree containing Tasks 1-3 and local `diabetes/results/`.
- Produces: a reviewed generated-output baseline under marimo 0.23.16, Matplotlib 3.11.1, and pandas 3.0.5.

- [ ] **Step 1: Confirm clean state and preserve the previous outputs**

Run:

```bash
git status --short --branch
mkdir -p /tmp/analysis_v2_pre_refresh_20260804
git archive HEAD diabetes/figures diabetes/csv_results | tar -x -C /tmp/analysis_v2_pre_refresh_20260804
```

Expected: the tracked worktree is clean before execution and the committed pre-migration outputs are preserved for semantic comparison.

- [ ] **Step 2: Run the intentional baseline refresh**

Run:

```bash
timeout --signal=TERM 15m uv run marimo export pdf --include-outputs --webpdf --no-include-inputs --no-rasterize-outputs diabetes/analysis_v2.py -o /tmp/analysis_v2_baseline_refresh.pdf -f
```

Expected: 4–8 minutes, exit code 0, and a nonempty temporary PDF. Poll the running process at least once per minute. Exit code 124 means the 15-minute timeout fired: stop, inspect Git status and partial outputs, and diagnose before retrying. Differences in tracked PNG and CSV files are expected on this first upgraded run.

- [ ] **Step 3: Create and run a semantic comparison report**

Create `/tmp/compare_analysis_v2_outputs.py` with:

```python
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from pandas.testing import assert_frame_equal


ROOT = Path("/home/marcos/github/bmclab/HDsEMGbias")
OLD = Path("/tmp/analysis_v2_pre_refresh_20260804")

csv_failures = []
png_changes = []

for current in sorted((ROOT / "diabetes/csv_results").glob("*.csv")):
    relative = current.relative_to(ROOT)
    previous = OLD / relative
    if not previous.exists():
        continue
    old_frame = pd.read_csv(previous)
    new_frame = pd.read_csv(current)
    try:
        assert_frame_equal(
            old_frame,
            new_frame,
            check_dtype=False,
            check_exact=False,
            rtol=1e-12,
            atol=1e-12,
        )
    except AssertionError as error:
        csv_failures.append((str(relative), str(error)))

for current in sorted((ROOT / "diabetes/figures").glob("*.png")):
    relative = current.relative_to(ROOT)
    previous = OLD / relative
    if not previous.exists():
        continue
    old_pixels = np.asarray(Image.open(previous).convert("RGBA"))
    new_pixels = np.asarray(Image.open(current).convert("RGBA"))
    if old_pixels.shape != new_pixels.shape:
        png_changes.append((str(relative), old_pixels.shape, new_pixels.shape, None, None))
        continue
    changed = np.any(old_pixels != new_pixels, axis=2)
    png_changes.append(
        (
            str(relative),
            old_pixels.shape,
            new_pixels.shape,
            float(changed.mean()),
            int(np.abs(old_pixels.astype(int) - new_pixels.astype(int)).max()),
        )
    )

print("CSV semantic failures:")
for path, error in csv_failures:
    print(path, error)
print("PNG pixel comparison:")
for result in png_changes:
    print(result)

if csv_failures:
    raise SystemExit(2)
```

Run:

```bash
uv run python /tmp/compare_analysis_v2_outputs.py
git status --short
git diff --numstat -- diabetes/csv_results diabetes/figures
git check-ignore -v diabetes/__marimo__/session/analysis_v2.py.json
git ls-files diabetes/__marimo__/session/analysis_v2.py.json
```

Expected: CSV comparison reports no semantic failures. PNG differences are quantified separately from metadata changes. The marimo session snapshot is ignored and untracked, so it does not pollute the baseline commit or clean-state checks.

- [ ] **Step 4: Visually review every changed PNG and inspect textual CSV diffs**

Run:

```bash
git diff -- diabetes/csv_results
git diff --name-only -- diabetes/figures
```

Open every changed PNG through the image viewer and compare it with its preserved predecessor. Expected: no missing panel, clipped annotation, altered axis semantics, or scientifically meaningful change. If any reported CSV value changes beyond the comparison tolerance, stop and reconcile the manuscript and reviewer response.

- [ ] **Step 5: Commit the accepted migration baseline**

Run:

```bash
git add diabetes/csv_results diabetes/figures
git diff --cached --check
git commit -m "chore: refresh analysis outputs for current environment"
git status --short --branch
```

Expected: only reviewed tracked outputs are committed and the worktree returns to clean.

---

### Task 5: Produce and validate the final clean PDF

**Files:**
- Create: `diabetes/analysis_v2_last_run.pdf`
- Ignored local side effect: `diabetes/__marimo__/session/analysis_v2.py.json`
- Temporary only: `/tmp/analysis_v2_last_run.pdf`
- Temporary only: `/tmp/analysis_v2_final_baseline.sha256`
- Temporary only: `/tmp/analysis_v2_expected_commit.txt`
- Temporary only: `/tmp/analysis_v2_expected_notebook_sha.txt`
- Temporary only: `/tmp/analysis_v2_expected_versions.txt`
- Temporary only: `/tmp/analysis_v2_last_run.txt`
- Temporary only: `/tmp/analysis_v2_last_run_flat.txt`
- Temporary only: `/tmp/analysis_v2_pdf_pages/`

**Interfaces:**
- Consumes: the clean generated-output baseline from Task 4.
- Produces: a stable PDF containing searchable provenance and all rendered analysis outputs.

- [ ] **Step 1: Record the clean baseline manifest**

Run:

```bash
set -euo pipefail
git status --short --branch
test -z "$(git status --porcelain --untracked-files=all)"
git ls-files -z diabetes/figures diabetes/csv_results | xargs -0 sha256sum > /tmp/analysis_v2_final_baseline.sha256
git rev-parse HEAD > /tmp/analysis_v2_expected_commit.txt
sha256sum diabetes/analysis_v2.py | cut -d " " -f 1 > /tmp/analysis_v2_expected_notebook_sha.txt
uv run python -c "import platform; from importlib.metadata import version; print('Python' + platform.python_version()); [print(label + version(name)) for label, name in (('marimo', 'marimo'), ('NumPy', 'numpy'), ('pandas', 'pandas'), ('Matplotlib', 'matplotlib'), ('SciPy', 'scipy'))]" > /tmp/analysis_v2_expected_versions.txt
test "$(wc -l < /tmp/analysis_v2_expected_versions.txt)" -eq 6
```

Expected: clean tracked worktree, 36 generated-output hashes, and exact expected provenance values captured before execution.

- [ ] **Step 2: Execute the final native PDF export**

Run:

```bash
timeout --signal=TERM 15m uv run marimo export pdf --include-outputs --webpdf --no-include-inputs --no-rasterize-outputs diabetes/analysis_v2.py -o /tmp/analysis_v2_last_run.pdf -f
```

Expected: 4–8 minutes, exit code 0, and a nonempty PDF. Poll the process at least once per minute. Exit code 124 is a failed export; stop and inspect partial generated outputs before retrying.

- [ ] **Step 3: Prove deterministic output regeneration**

Run:

```bash
set -euo pipefail
sha256sum -c /tmp/analysis_v2_final_baseline.sha256
test -z "$(git status --porcelain --untracked-files=all)"
git check-ignore -v diabetes/__marimo__/session/analysis_v2.py.json
test -z "$(git ls-files diabetes/__marimo__/session/analysis_v2.py.json)"
```

Expected: every hash reports `OK`; Git status is empty because the generated session snapshot is ignored; the session path is not tracked. Stop if any condition fails.

- [ ] **Step 4: Verify searchable provenance and PDF structure**

Run:

```bash
set -euo pipefail
pdfinfo /tmp/analysis_v2_last_run.pdf
pdftotext /tmp/analysis_v2_last_run.pdf /tmp/analysis_v2_last_run.txt
tr -d '[:space:]' < /tmp/analysis_v2_last_run.txt > /tmp/analysis_v2_last_run_flat.txt
for label in "Executionprovenance" "Executedat" "Python" "marimo" "NumPy" "pandas" "Matplotlib" "SciPy" "Gitcommit" "Gitstate" "NotebookSHA-256"; do rg -F "$label" /tmp/analysis_v2_last_run_flat.txt > /dev/null || exit 1; done
rg -F -f /tmp/analysis_v2_expected_commit.txt /tmp/analysis_v2_last_run_flat.txt > /dev/null
rg -F -f /tmp/analysis_v2_expected_notebook_sha.txt /tmp/analysis_v2_last_run_flat.txt > /dev/null
while IFS= read -r expected_version; do rg -F "$expected_version" /tmp/analysis_v2_last_run_flat.txt > /dev/null || exit 1; done < /tmp/analysis_v2_expected_versions.txt
rg -n "20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}" /tmp/analysis_v2_last_run_flat.txt > /dev/null
rg -F "Gitstateclean" /tmp/analysis_v2_last_run_flat.txt > /dev/null
if rg -n "unavailable|dirty" /tmp/analysis_v2_last_run_flat.txt > /dev/null; then exit 1; fi
pdfimages -list /tmp/analysis_v2_last_run.pdf
stat -c "%n %s bytes" /tmp/analysis_v2_last_run.pdf
test "$(stat -c %s /tmp/analysis_v2_last_run.pdf)" -lt 100000000
```

Expected: fail-fast mode makes every assertion binding; every label and each label-plus-version token is searchable, wrapped commit/SHA text is reconstructed before matching, the timestamp includes a UTC offset, the normalized table contains `Gitstateclean`, no field is `unavailable`, PDF images are present, and the file is below GitHub's 100 MB file limit.

- [ ] **Step 5: Render and inspect every page**

Run:

```bash
mkdir -p /tmp/analysis_v2_pdf_pages
pdftoppm -png -r 110 /tmp/analysis_v2_last_run.pdf /tmp/analysis_v2_pdf_pages/page
```

Inspect every rendered page with the image viewer. Expected: the provenance block near the beginning is visibly a two-column table rather than a code block or run-on paragraph; figures, captions, statistical output, and page breaks are legible; no page is empty or clipped.

- [ ] **Step 6: Publish only the validated PDF and commit it**

Run:

```bash
cp /tmp/analysis_v2_last_run.pdf diabetes/analysis_v2_last_run.pdf
git status --short
git add diabetes/analysis_v2_last_run.pdf
git diff --cached --check
git commit -m "docs: add latest executed analysis snapshot"
```

Expected: the commit contains only `diabetes/analysis_v2_last_run.pdf`. Its embedded source commit is the clean generated-output baseline commit immediately preceding the PDF commit.

---

### Task 6: Final repository verification

**Files:**
- Verify: `diabetes/analysis_v2.py`
- Verify: `diabetes/tests/test_analysis_v2_figure_display.py`
- Verify: `README.md`
- Verify: `diabetes/analysis_v2_last_run.pdf`
- Verify untouched: `diabetes/run_model.py`

**Interfaces:**
- Consumes: all preceding commits.
- Produces: a clean, locally reproducible handoff with no raw result data tracked.

- [ ] **Step 1: Re-run code and notebook checks**

Run:

```bash
uv run python -m unittest diabetes.tests.test_analysis_v2_figure_display -v
uv run marimo check --strict diabetes/analysis_v2.py
git diff --check
```

Expected: all tests and notebook checks pass; no whitespace errors.

- [ ] **Step 2: Verify data boundaries and untouched obsolete code**

Run:

```bash
git check-ignore -v diabetes/results/
git ls-files diabetes/results
git check-ignore -v diabetes/__marimo__/session/analysis_v2.py.json
git ls-files diabetes/__marimo__/session/analysis_v2.py.json
git diff 8119d00..HEAD -- diabetes/run_model.py
```

Expected: `diabetes/results/` and the analysis-v2 session snapshot are ignored and untracked, and `run_model.py` has no diff.

- [ ] **Step 3: Verify the final artifact and repository state**

Run:

```bash
set -euo pipefail
pdfinfo diabetes/analysis_v2_last_run.pdf
pdftotext diabetes/analysis_v2_last_run.pdf /tmp/analysis_v2_committed_pdf.txt
tr -d '[:space:]' < /tmp/analysis_v2_committed_pdf.txt > /tmp/analysis_v2_committed_pdf_flat.txt
git rev-parse HEAD^ > /tmp/analysis_v2_pdf_source_commit.txt
sha256sum diabetes/analysis_v2.py | cut -d " " -f 1 > /tmp/analysis_v2_committed_notebook_sha.txt
rg -F -f /tmp/analysis_v2_pdf_source_commit.txt /tmp/analysis_v2_committed_pdf_flat.txt > /dev/null
rg -F -f /tmp/analysis_v2_committed_notebook_sha.txt /tmp/analysis_v2_committed_pdf_flat.txt > /dev/null
rg -F "Gitstateclean" /tmp/analysis_v2_committed_pdf_flat.txt > /dev/null
if rg -n "unavailable|dirty" /tmp/analysis_v2_committed_pdf_flat.txt > /dev/null; then exit 1; fi
test -z "$(git status --porcelain --untracked-files=all)"
git status --short --branch
git log -6 --oneline
```

Expected: the PDF remains readable and searchable, its embedded source commit is the commit immediately before the PDF artifact, its source digest matches the notebook, Git state is exactly clean, the worktree is clean, and all task-scoped commits are present locally. Do not push.
