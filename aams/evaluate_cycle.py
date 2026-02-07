from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from aams.config import (
    EXPERIMENT_LOG_PATH,
    METRICS_PATH,
    PENDING_METADATA_PATH,
    PENDING_SPEC_PATH,
    RESULTS_PATH,
)
from aams.evaluate import compute_fitness
from aams.specs import archive_spec, load_current_spec, save_current_spec
from aams.train import train_micro_model


def _write_metrics_snapshot(entry: Dict[str, Any]) -> None:
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"updated_at": entry["timestamp"], "latest": entry}
    with METRICS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def _log_experiment(entry: Dict[str, Any]) -> None:
    EXPERIMENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with EXPERIMENT_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_cycle() -> Dict[str, Any]:
    pending_meta = _load_json(PENDING_METADATA_PATH)
    pending_spec = _load_json(PENDING_SPEC_PATH)
    results = _load_json(RESULTS_PATH)

    current_spec = load_current_spec()
    baseline_metrics = train_micro_model(current_spec)
    baseline_fitness = compute_fitness(baseline_metrics)

    candidate_fitness = compute_fitness(results)
    accepted = candidate_fitness < baseline_fitness

    if accepted:
        archive_spec(current_spec, "replaced")
        save_current_spec(pending_spec)

    timestamp = datetime.now(timezone.utc).isoformat()
    entry = {
        "timestamp": timestamp,
        "mutation": pending_meta.get("mutation", "unknown"),
        "accepted": accepted,
        "fitness": candidate_fitness,
        "metrics": results,
        "spec": pending_spec,
        "run_id": pending_meta.get("run_id"),
    }

    _log_experiment(entry)
    _write_metrics_snapshot(entry)
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Kaggle results.")
    parser.parse_args()
    entry = evaluate_cycle()
    print(json.dumps(entry, indent=2))


if __name__ == "__main__":
    main()
