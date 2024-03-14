from dataclasses import dataclass


@dataclass(frozen=True)
class AppRoute:
    """application URL when user requested authentication"""

    value: str
