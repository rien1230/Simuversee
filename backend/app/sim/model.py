# holds ticks(number) and it increases by 1 we 'step' and must output a simple message .
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
import random


@dataclass

class SimModel:
    #initialises randomness but if same seed=same behaviour
    seed: int
    tick: int = 0
    #random number generator
    rng: random.Random = field(init=False, repr=False)
#runs after dataclass is generated
    def __post_init__(self) -> None:
        # Deterministic RNG (useful later when I add random behaviour)
        self.rng = random.Random(self.seed)

    def step(self) -> Dict[str, Any]:

        self.tick += 1

        diff: Dict[str, Any] = {
            "tick": self.tick,
            "agents": [],  # later: list of agent states
            "ties": [],    # later: relationship edges
            "events": [],  # later: any events that happened this tick
        }
        return diff
