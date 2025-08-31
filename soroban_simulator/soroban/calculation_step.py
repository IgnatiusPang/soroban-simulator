
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CalculationStep:
    """A single step in a soroban calculation."""
    step_description: str
    soroban_state: List[int]
    current_value: int
    markers: Optional[List] = None
