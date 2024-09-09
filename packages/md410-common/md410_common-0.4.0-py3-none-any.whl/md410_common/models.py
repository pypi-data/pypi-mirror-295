from datetime import datetime
from typing import Any, ClassVar, List, Optional

try:
    import constants
except ImportError:
    from . import constants

from pydantic import BaseModel


class Registration(BaseModel):
    reg_num: Optional[int]
    first_names: str
    last_name: str
    name_badge: str
    cell: str
    email: str
    dietary: Optional[str]
    disability: Optional[str]
    lion: bool
    club: str
    timestamp: datetime
    reg_num_string: Optional[str]
    full_name: Optional[str]
    auto_name_badge: Optional[bool]
    cost: Optional[int]
    deleted: bool = False
    partial_reg: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.reg_num:
            self.reg_num_string = f"MY{self.reg_num:03}"
        self.full_name = f"{self.first_names} {self.last_name}"
        if not self.name_badge:
            self.name_badge = self.full_name
            self.auto_name_badge = True
        self.cost = {
            (False, False): constants.COST_FULL_REG_NON_LION,
            (False, True): constants.COST_FULL_REG_LION,
            (True, False): constants.COST_PARTIAL_REG_NON_LION,
            (True, True): constants.COST_PARTIAL_REG_LION,
        }[(self.partial_reg, self.lion)]
