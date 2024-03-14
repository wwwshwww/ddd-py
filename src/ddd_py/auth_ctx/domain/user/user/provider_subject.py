from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderSubject:
    value: str
