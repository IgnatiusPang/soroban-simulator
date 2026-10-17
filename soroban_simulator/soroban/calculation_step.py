
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Union, Any

@dataclass
class CalculationStep:
    """A single step in a soroban calculation."""
    step_description: str
    soroban_state: List[int]
    current_value: Union[int, Decimal]
    markers: Optional[List[Any]] = None
