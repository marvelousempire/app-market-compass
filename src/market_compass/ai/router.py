from __future__ import annotations

import os
from typing import Any

from .contracts import AnalystRequest, AnalystResponse, ProviderStatus
from .providers import (
    AnalystProvider,
    AnthropicProvider,
    GroundedMockProvider,
    OpenAICompatibleProvider,
    ProviderError,
    ResponsesProvider,
)


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


class AnalystRouter:
    def __init__(self, providers: list[AnalystProvider] | None = None):
        self.providers = providers or self._from_environment()
        self.cloud_enabled = _env("MARKET_COMPASS_CLOUD_ENABLED").lower() in {"1", "true", "yes"}

    @staticmethod
    def _from_environment() -> list[AnalystProvider]:
        providers: list[AnalystProvider] = [GroundedMockProvider()]
        local = [
            ("nephew-m5", "Nephew · Five Mac MLX", "m5-mlx", "NEPHEW_M5"),
            ("nephew-dgx", "Nephew · DGX Spark vLLM", "dgx-vllm", "NEPHEW_DGX"),
            ("ollama", "Ollama Recovery", "ollama", "OLLAMA"),
        ]
        for id_, label, lane, prefix in local:
            base = _env(f"{prefix}_API_BASE")
            model = _env(f"{prefix}_MODEL")
            if base or model:
                providers.append(OpenAICompatibleProvider(
                    id=id_, label=label, lane=lane, model=model, base_url=base,
                    api_key=_env(f"{prefix}_API_KEY"), cloud=False,
                ))
        cloud = [
            ResponsesProvider(
                id="openai-pro", label="OpenAI · GPT Pro", lane="cloud-openai",
                model=_env("OPENAI_MARKET_MODEL", "gpt-5.6-sol"),
                base_url=_env("OPENAI_API_BASE", "https://api.openai.com/v1"),
                api_key=_env("OPENAI_API_KEY"), cloud=True, reasoning_mode="pro", timeout=600,
            ),
            AnthropicProvider(
                id="anthropic", label="Anthropic · Claude", lane="cloud-anthropic",
                model=_env("ANTHROPIC_MARKET_MODEL", "claude-fable-5"),
                base_url=_env("ANTHROPIC_API_BASE", "https://api.anthropic.com/v1"),
                api_key=_env("ANTHROPIC_API_KEY"), cloud=True, timeout=600,
            ),
            OpenAICompatibleProvider(
                id="perplexity", label="Perplexity · Research", lane="cloud-perplexity",
                model=_env("PERPLEXITY_MARKET_MODEL", "sonar-deep-research"),
                base_url=_env("PERPLEXITY_API_BASE", "https://api.perplexity.ai"),
                api_key=_env("PERPLEXITY_API_KEY"), cloud=True, timeout=600,
            ),
            ResponsesProvider(
                id="xai", label="xAI · Grok Heavy", lane="cloud-xai",
                model=_env("XAI_MARKET_MODEL", "grok-4.6"),
                base_url=_env("XAI_API_BASE", "https://api.x.ai/v1"),
                api_key=_env("XAI_API_KEY"), cloud=True, timeout=600,
            ),
        ]
        providers.extend(cloud)
        return providers

    def statuses(self) -> list[ProviderStatus]:
        statuses = []
        for provider in self.providers:
            status = provider.status()
            if provider.cloud and status.configured and not self.cloud_enabled:
                status = status.model_copy(update={
                    "configured": False,
                    "healthy": False,
                    "reason": "Credentials found, but server-side cloud permission is disabled.",
                })
            statuses.append(status)
        return statuses

    def _eligible(self, request: AnalystRequest) -> list[AnalystProvider]:
        return [
            p for p in self.providers
            if p.status().configured
            and (not p.cloud or (request.cloud_allowed and self.cloud_enabled))
        ]

    def select(self, request: AnalystRequest) -> AnalystProvider:
        eligible = self._eligible(request)
        if request.provider != "auto":
            provider = next((p for p in eligible if p.id == request.provider), None)
            if provider:
                return provider
            raise ProviderError(
                f"Provider '{request.provider}' is unavailable or requires cloud approval/configuration."
            )
        preferences = (
            ["nephew-dgx", "nephew-m5", "openai-pro", "anthropic", "xai", "perplexity", "ollama", "grounded-offline"]
            if request.depth == "super-heavy" else
            ["nephew-m5", "nephew-dgx", "ollama", "grounded-offline"]
        )
        for provider_id in preferences:
            match = next((p for p in eligible if p.id == provider_id), None)
            if match:
                return match
        raise ProviderError("No eligible analyst provider is configured.")

    def analyze(self, request: AnalystRequest) -> AnalystResponse:
        return self.select(request).analyze(request.report, request.question, request.depth)

    def health(self) -> dict[str, Any]:
        statuses = self.statuses()
        return {
            "status": "ok" if any(x.healthy for x in statuses) else "degraded",
            "configured": sum(x.configured for x in statuses),
            "providers": [x.model_dump(mode="json") for x in statuses],
        }
