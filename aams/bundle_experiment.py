from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from aams.config import BUNDLE_DIR, PENDING_METADATA_PATH, PENDING_SPEC_PATH
from aams.mutate import mutate_spec
from aams.specs import load_current_spec


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def bundle_experiment(seed: int | None = None) -> Dict[str, Any]:
    current_spec = load_current_spec()
    mutated_spec, mutation = mutate_spec(current_spec, seed=seed)
    run_id = f"aams_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    if BUNDLE_DIR.exists():
        shutil.rmtree(BUNDLE_DIR)
    BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

    _write_json(PENDING_SPEC_PATH, mutated_spec)
    metadata = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mutation": mutation,
        "pending_spec_path": str(PENDING_SPEC_PATH),
    }
    _write_json(PENDING_METADATA_PATH, metadata)

    _write_json(BUNDLE_DIR / "arch_spec.json", mutated_spec)
    _write_json(
        BUNDLE_DIR / "train_config.json",
        {
            "epochs": 1,
            "batch_size": 32,
            "max_steps": 250,
            "optimizer": "adamw",
        },
    )
    (BUNDLE_DIR / "run_id.txt").write_text(run_id, encoding="utf-8")
    (BUNDLE_DIR / "model.py").write_text(
        "# Placeholder model generated from arch_spec.json\n"
        "# Replace with compiler output when available.\n",
        encoding="utf-8",
    )

    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Bundle an experiment for Kaggle.")
    parser.add_argument("--seed", type=int, default=None, help="Optional seed for mutation.")
    args = parser.parse_args()
    metadata = bundle_experiment(seed=args.seed)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
