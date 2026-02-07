from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from aams.config import CURRENT_SPEC_PATH, HISTORY_DIR


def load_current_spec() -> Dict[str, Any]:
    with CURRENT_SPEC_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_current_spec(spec: Dict[str, Any]) -> None:
    CURRENT_SPEC_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CURRENT_SPEC_PATH.open("w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=2, sort_keys=True)


def archive_spec(spec: Dict[str, Any], suffix: str) -> Path:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = HISTORY_DIR / f"arch_spec_{timestamp}_{suffix}.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(spec, handle, indent=2, sort_keys=True)
    return path
