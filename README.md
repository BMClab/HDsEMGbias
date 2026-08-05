# HD-sEMG decomposition bias Analysis

[![Python](https://img.shields.io/badge/Python->=_3.10-blue.svg)](https://www.python.org/)
[![NEURON](https://img.shields.io/badge/NEURON->=_8.2.0-orange.svg)](https://neuron.yale.edu/neuron/)

## 👥 Contributors

- **Renato Watanabe**
- **Rebeka Batichotti**
- **Marcos Duarte**

## 📋 Overview

*A computational model for motoneuron simulation.*

## ⚙️ Setup Environment

### 1. Install uv (Dependency Manager)

Get the latest version of uv from [the official documentation](https://docs.astral.sh/uv/getting-started/installation/).

<details open><summary>💻<b>Windows Installation</b></summary>

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

</details>

<details>

<summary>🐧 <b>Linux/MacOS Installation</b></summary>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

</details>

### 2. Install Dependencies

```bash
uv sync
```

#### 2.1 Windows NEURON Installation

> [!IMPORTANT]
> On Windows, NEURON must be installed separately as it cannot be installed via pip.  
>
> - Download from [NEURON Documentation](https://nrn.readthedocs.io/en/8.2.6/install/install_instructions.html)
> - Install to the default directory: `C:\nrn`

Configure the `PYTHONPATH` environment variable for your IDE:

| IDE    | Configuration                                               |
|--------|-------------------------------------------------------------|
| VSCode | PYTHONPATH environment variable preset automatically        |
| Others | Set PYTHONPATH to: `C:\nrn\lib\python`                      |

## 📝 Run Marimo Notebooks

```bash
uv run marimo edit NOTEBOOK_NAME.py
```

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

Simulations can be run with the following command:

```bash
./run_trials.sh
```
