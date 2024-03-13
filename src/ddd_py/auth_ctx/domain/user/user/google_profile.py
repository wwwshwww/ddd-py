from dataclasses import dataclass

from .provider_subject import ProviderSubject

@dataclass(frozen=True)
class GoogleProfile:
    provider_subject: ProviderSubject
    