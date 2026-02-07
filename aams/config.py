from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SPECS_DIR = REPO_ROOT / "specs" / "current"
HISTORY_DIR = REPO_ROOT / "specs" / "history"
LOGS_DIR = REPO_ROOT / "logs"
DOCS_DIR = REPO_ROOT / "docs"
EXPERIMENTS_DIR = REPO_ROOT / "experiments"

CURRENT_SPEC_PATH = SPECS_DIR / "arch_spec.json"
PENDING_SPEC_PATH = REPO_ROOT / "specs" / "pending" / "arch_spec.json"
PENDING_METADATA_PATH = LOGS_DIR / "pending.json"
EXPERIMENT_LOG_PATH = LOGS_DIR / "experiments.jsonl"
METRICS_PATH = DOCS_DIR / "metrics.json"
RESULTS_PATH = EXPERIMENTS_DIR / "results" / "results.json"
BUNDLE_DIR = EXPERIMENTS_DIR / "bundle"

RULES_PATH = REPO_ROOT / "safety" / "rules.json"

ALLOWED_ATTENTION = ["mhsa", "gqa", "mqa", "linear"]
ALLOWED_FFN = ["gelu", "swiglu"]
ALLOWED_RESIDUAL = ["pre_norm", "post_norm"]
ALLOWED_POS_ENCODING = ["rotary", "absolute"]
