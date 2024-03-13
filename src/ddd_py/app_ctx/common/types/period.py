from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Period:
    start_date_inclusive: datetime
    end_date_exclusive: datetime

    def __post_init__(self):
        if self.end_date_exclusive <= self.start_date_inclusive:
            raise AttributeError("End date must be greater than start date")
