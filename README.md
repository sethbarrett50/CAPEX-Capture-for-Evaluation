# CAPEX: Capture for Evaluation

This directory contains all scripts, datasets, and supporting files for the generation and processing of network traffic datasets used in both the FIRE intrusion detection framework and in concept drift analysis for conformal evaluation.

---

## Directory Overview

### `AttackCaps_OLD/`

Contains legacy PCAP and log files used in the original **FIRE** paper experiments. Each pair of files (`.pcap`, `.txt`) corresponds to a device under attack and the metadata of the attack timing.

### `CEFlows/`

Stores new datasets generated for evaluating the **Conformal Evaluator** system. Includes:

* `.pcap` files with captured network traffic.
* `.csv` files output by CICFlowMeter.
* `.txt` logs of attack events.

### `oldCapScripts/`

Archive of older capture and attack orchestration scripts, used during development of the FIRE dataset.

---

## Key Files

### `conceptDriftCap.py`

Main orchestration script for concept drift experiments. Automates:

* PCAP data capture
* Launching multiple attacks (e.g., DoS, HULK)
* Logging of timing metadata for ground truth

### `hulk.py`

Standalone script for executing an HTTP flood (HULK) attack against a specified IoT device or service.

Usage:

```bash
python3 hulk.py <duration_seconds> <target_url>
# e.g. python3 hulk.py 60 http://192.168.1.172
```

### `merge_ce_flows.py`

Utility to merge multiple CSV flow outputs into a single unified file ordered by timestamp.

### `run_CIC_batch.sh`

Batch processor to run CICFlowMeter on all PCAP files inside `CEFlows/`. It outputs `.csv` flow files suitable for ML processing.

---

## Setup (Using `uv`)

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management and virtual environment setup.

### 1. Clone the repository and change directory:

```bash
cd ~/Desktop/NetworkDatasetCreation
```

### 2. Set up the virtual environment and install dependencies:

```bash
uv sync
```

This will:

* Create a `.venv/` directory
* Install all required packages from `pyproject.toml` and `uv.lock`

### 3. Run scripts with uv:

```bash
uv run conceptDriftCap.py
uv run merge_ce_flows.py
```

---

## Cleanup

If `MultiAttackCaps.tar.gz` is not needed, it can be safely removed:

```bash
rm MultiAttackCaps.tar.gz
```

---

## Notes

* All PCAPs are captured using `tcpdump`
* Network flows are extracted using [CICFlowMeter](https://www.unb.ca/cic/research/applications.html)
* Attack scripts should be run with `sudo` due to raw socket requirements

---

For questions, contact: **Seth Barrett**
