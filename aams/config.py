from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SPECS_DIR = REPO_ROOT / "specs" / "current"
HISTORY_DIR = REPO_ROOT / "specs" / "history"
LOGS_DIR = REPO_ROOT / "logs"
DOCS_DIR = REPO_ROOT / "docs"

CURRENT_SPEC_PATH = SPECS_DIR / "arch_spec.json"
EXPERIMENT_LOG_PATH = LOGS_DIR / "experiments.jsonl"
METRICS_PATH = DOCS_DIR / "metrics.json"

RULES_PATH = REPO_ROOT / "safety" / "rules.json"

ALLOWED_ATTENTION = ["mhsa", "gqa", "mqa", "linear"]
ALLOWED_FFN = ["gelu", "swiglu"]
ALLOWED_RESIDUAL = ["pre_norm", "post_norm"]
ALLOWED_POS_ENCODING = ["rotary", "absolute"]
