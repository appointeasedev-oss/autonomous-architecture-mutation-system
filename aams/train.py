from __future__ import annotations

import hashlib
from typing import Any, Dict


def _stable_hash(spec: Dict[str, Any]) -> int:
    encoded = str(sorted(spec.items())).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    return int(digest[:8], 16)


def train_micro_model(spec: Dict[str, Any]) -> Dict[str, float]:
    """
    Simulate a micro-training loop deterministically from the architecture spec.

    This is a placeholder for real training that keeps CI fast and reproducible.
    """
    seed = _stable_hash(spec)

    base_loss = 3.5
    depth_bonus = (12 - spec["n_layers"]) * 0.03
    width_bonus = (768 - spec["d_model"]) / 2048

    attention_bonus = {
        "mhsa": 0.0,
        "gqa": -0.05,
        "mqa": -0.02,
        "linear": 0.07,
    }[spec["attention"]]

    ffn_bonus = {
        "gelu": 0.02,
        "swiglu": -0.03,
    }[spec["ffn"]]

    residual_bonus = {
        "pre_norm": -0.04,
        "post_norm": 0.01,
    }[spec["residual"]]

    loss = base_loss + depth_bonus + width_bonus + attention_bonus + ffn_bonus + residual_bonus
    loss = max(1.5, min(5.0, loss))

    params = spec["n_layers"] * spec["d_model"] * 8_000
    latency = (spec["n_layers"] * spec["d_model"]) / 200

    return {
        "loss": round(loss, 4),
        "params": float(params),
        "latency": round(latency, 3),
        "seed": float(seed % 10_000),
    }
