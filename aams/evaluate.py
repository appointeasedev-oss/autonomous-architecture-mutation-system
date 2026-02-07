from __future__ import annotations

from typing import Dict


def compute_fitness(metrics: Dict[str, float]) -> float:
    loss = metrics["loss"]
    latency = metrics["latency"]
    params = metrics["params"]

    return round(loss + 0.005 * latency + 0.0000001 * params, 4)
