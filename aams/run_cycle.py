from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from aams.config import EXPERIMENT_LOG_PATH, METRICS_PATH
from aams.evaluate import compute_fitness
from aams.mutate import mutate_spec
from aams.specs import archive_spec, load_current_spec, save_current_spec
from aams.train import train_micro_model


def _log_experiment(entry: Dict[str, Any]) -> None:
    EXPERIMENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with EXPERIMENT_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def _write_metrics_snapshot(entry: Dict[str, Any]) -> None:
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": entry["timestamp"],
        "latest": entry,
    }
    with METRICS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def run_cycle(seed: int | None = None) -> Dict[str, Any]:
    current_spec = load_current_spec()
    current_metrics = train_micro_model(current_spec)
    current_fitness = compute_fitness(current_metrics)

    mutated_spec, mutation = mutate_spec(current_spec, seed=seed)
    mutated_metrics = train_micro_model(mutated_spec)
    mutated_fitness = compute_fitness(mutated_metrics)

    accepted = mutated_fitness < current_fitness

    if accepted:
        archive_spec(current_spec, "replaced")
        save_current_spec(mutated_spec)
        chosen_spec = mutated_spec
        chosen_metrics = mutated_metrics
        chosen_fitness = mutated_fitness
    else:
        chosen_spec = current_spec
        chosen_metrics = current_metrics
        chosen_fitness = current_fitness

    timestamp = datetime.now(timezone.utc).isoformat()
    entry = {
        "timestamp": timestamp,
        "mutation": mutation,
        "accepted": accepted,
        "fitness": chosen_fitness,
        "metrics": chosen_metrics,
        "spec": chosen_spec,
    }

    _log_experiment(entry)
    _write_metrics_snapshot(entry)

    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a single AAMS evolution cycle.")
    parser.add_argument("--seed", type=int, default=None, help="Optional seed for mutation.")
    args = parser.parse_args()

    result = run_cycle(seed=args.seed)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
