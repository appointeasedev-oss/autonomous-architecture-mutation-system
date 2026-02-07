from __future__ import annotations

import copy
import random
from typing import Any, Dict, Tuple

from aams.config import (
    ALLOWED_ATTENTION,
    ALLOWED_FFN,
    ALLOWED_POS_ENCODING,
    ALLOWED_RESIDUAL,
)


def _cycle_option(current: str, options: list[str]) -> str:
    if current not in options:
        return options[0]
    index = options.index(current)
    return options[(index + 1) % len(options)]


def mutate_spec(spec: Dict[str, Any], seed: int | None = None) -> Tuple[Dict[str, Any], str]:
    rng = random.Random(seed)
    mutation_choices = [
        "attention",
        "ffn",
        "residual",
        "pos_encoding",
        "layers",
        "width",
    ]
    mutation = rng.choice(mutation_choices)
    mutated = copy.deepcopy(spec)

    if mutation == "attention":
        mutated["attention"] = _cycle_option(spec["attention"], ALLOWED_ATTENTION)
    elif mutation == "ffn":
        mutated["ffn"] = _cycle_option(spec["ffn"], ALLOWED_FFN)
    elif mutation == "residual":
        mutated["residual"] = _cycle_option(spec["residual"], ALLOWED_RESIDUAL)
    elif mutation == "pos_encoding":
        mutated["pos_encoding"] = _cycle_option(spec["pos_encoding"], ALLOWED_POS_ENCODING)
    elif mutation == "layers":
        delta = rng.choice([-1, 1])
        mutated["n_layers"] = max(2, min(12, spec["n_layers"] + delta))
    elif mutation == "width":
        delta = rng.choice([-64, 64])
        mutated["d_model"] = max(128, min(768, spec["d_model"] + delta))

    return mutated, mutation
