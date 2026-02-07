from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from aams.config import RESULTS_PATH


def receive_results(source: Path) -> Dict[str, Any]:
    if not source.exists():
        raise FileNotFoundError(f"Results file not found: {source}")
    payload = json.loads(source.read_text(encoding="utf-8"))
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Store Kaggle results for evaluation.")
    parser.add_argument("--input", required=True, help="Path to results.json")
    args = parser.parse_args()
    payload = receive_results(Path(args.input))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
