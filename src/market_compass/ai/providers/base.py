from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..contracts import AnalystResponse, ProviderStatus


class ProviderError(RuntimeError):
    pass


class AnalystProvider(ABC):
    id: str
    label: str
    lane: str
    model: str
    cloud: bool

    @abstractmethod
    def status(self) -> ProviderStatus:
        raise NotImplementedError

    @abstractmethod
    def analyze(self, report: dict[str, Any], question: str, depth: str) -> AnalystResponse:
        raise NotImplementedError
