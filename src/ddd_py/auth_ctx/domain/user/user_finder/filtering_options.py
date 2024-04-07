from dataclasses import dataclass


@dataclass
class FilteringOptions:
    provider_subject_google: str | None = None
