from dataclasses import dataclass


@dataclass(frozen=True)
class ClientState:
    """application URL when user requested authentication"""

    value: str
