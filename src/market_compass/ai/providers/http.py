from __future__ import annotations

import json
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pydantic import ValidationError

from ...data import SSL_CONTEXT
from ..contracts import AnalystResponse, ModelReceipt, ProviderStatus
from ..prompt import SYSTEM_PROMPT, build_prompt
from .base import AnalystProvider, ProviderError
from .mock import report_hash


def _post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> dict[str, Any]:
    req = Request(
        url, data=json.dumps(payload).encode(), method="POST",
        headers={"Content-Type": "application/json", **headers},
    )
    try:
        with urlopen(req, timeout=timeout, context=SSL_CONTEXT) as response:
            return json.loads(response.read().decode())
    except HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:1000]
        raise ProviderError(f"Provider returned HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ProviderError(f"Provider request failed: {exc}") from exc


def _json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ProviderError("Provider did not return valid analyst JSON.") from exc


class HttpProvider(AnalystProvider):
    def __init__(self, *, id: str, label: str, lane: str, model: str, base_url: str,
                 api_key: str, cloud: bool, timeout: int = 180):
        self.id, self.label, self.lane, self.model = id, label, lane, model
        self.base_url, self.api_key, self.cloud, self.timeout = base_url.rstrip("/"), api_key, cloud, timeout

    def status(self) -> ProviderStatus:
        configured = bool(self.base_url and self.model and (self.api_key or not self.cloud))
        return ProviderStatus(
            id=self.id, label=self.label, lane=self.lane, model=self.model or "unconfigured",
            cloud=self.cloud, configured=configured, healthy=False,
            reason=(
                "Configured; connectivity is checked on the first request."
                if configured else "Required endpoint, model, or key is missing."
            ),
        )

    def _finish(self, raw: dict[str, Any], report: dict[str, Any], elapsed_ms: int) -> AnalystResponse:
        raw["receipt"] = ModelReceipt(
            provider=self.id, model=self.model, lane=self.lane,
            report_hash=report_hash(report), latency_ms=elapsed_ms,
        ).model_dump(mode="json")
        try:
            return AnalystResponse.model_validate(raw)
        except ValidationError as exc:
            raise ProviderError(f"Provider response failed the analyst schema: {exc}") from exc


class OpenAICompatibleProvider(HttpProvider):
    def analyze(self, report: dict[str, Any], question: str, depth: str) -> AnalystResponse:
        started = time.monotonic()
        data = _post_json(
            f"{self.base_url}/chat/completions",
            {"model": self.model, "temperature": 0.1, "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_prompt(report, question, depth)},
            ]},
            {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}, self.timeout,
        )
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return self._finish(_json_object(text), report, int((time.monotonic() - started) * 1000))


class ResponsesProvider(HttpProvider):
    def __init__(self, *args, reasoning_mode: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reasoning_mode = reasoning_mode

    def analyze(self, report: dict[str, Any], question: str, depth: str) -> AnalystResponse:
        started = time.monotonic()
        payload: dict[str, Any] = {
            "model": self.model, "instructions": SYSTEM_PROMPT,
            "input": build_prompt(report, question, depth),
        }
        if self.reasoning_mode:
            payload["reasoning"] = {"mode": self.reasoning_mode, "effort": "high"}
        data = _post_json(
            f"{self.base_url}/responses", payload,
            {"Authorization": f"Bearer {self.api_key}"}, self.timeout,
        )
        text = data.get("output_text", "")
        if not text:
            parts = data.get("output") or []
            text = "".join(
                item.get("text", "") for output in parts for item in output.get("content", [])
                if item.get("type") in {"output_text", "text"}
            )
        return self._finish(_json_object(text), report, int((time.monotonic() - started) * 1000))


class AnthropicProvider(HttpProvider):
    def analyze(self, report: dict[str, Any], question: str, depth: str) -> AnalystResponse:
        started = time.monotonic()
        data = _post_json(
            f"{self.base_url}/messages",
            {"model": self.model, "max_tokens": 5000, "temperature": 0.1,
             "system": SYSTEM_PROMPT,
             "messages": [{"role": "user", "content": build_prompt(report, question, depth)}]},
            {"x-api-key": self.api_key, "anthropic-version": "2023-06-01"}, self.timeout,
        )
        text = "".join(x.get("text", "") for x in data.get("content", []) if x.get("type") == "text")
        return self._finish(_json_object(text), report, int((time.monotonic() - started) * 1000))
