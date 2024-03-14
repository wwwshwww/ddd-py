from dataclasses import dataclass
from typing import Optional


@dataclass
class FilteringOptions:
    provider_subject_google: Optional[str] = None
