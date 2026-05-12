"""Tests for Tesla Hermes signaling diagnostics."""

from __future__ import annotations

import asyncio
import base64
import importlib.util
import json
import sys
from pathlib import Path


ROOT = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "power_sync"
    / "powerwall_local"
)


def _load_signaling_module():
    name = "powerwall_signaling_test_module"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, ROOT / "signaling.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


signaling = _load_signaling_module()


def _jwt_with_scopes(scopes: list[str]) -> str:
    header = {"alg": "RS256", "typ": "JWT"}
    payload = {"scp": scopes}

    def enc(data: dict) -> str:
        raw = json.dumps(data, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(raw).decode().rstrip("=")

    return f"{enc(header)}.{enc(payload)}.sig"


class _FakeResponse:
    status = 403

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def text(self):
        return '{"response":null,"error":"Unauthorized missing scopes","error_description":""}'


class _FakeSession:
    post_calls = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    def post(self, *args, **kwargs):
        type(self).post_calls += 1
        return _FakeResponse()


def test_decode_jwt_scopes_supports_tesla_scp_claim():
    token = _jwt_with_scopes(["openid", "energy_device_data"])

    assert signaling._decode_jwt_scopes(token) == [
        "openid",
        "energy_device_data",
    ]


def test_missing_scope_response_stops_before_raw_websocket_fallback(monkeypatch, caplog):
    async def get_token():
        return _jwt_with_scopes(["openid", "offline_access", "energy_device_data"])

    caplog.set_level("WARNING")
    _FakeSession.post_calls = 0
    monkeypatch.setattr(signaling.aiohttp, "ClientSession", _FakeSession)
    monkeypatch.setattr(signaling, "HERMES_JWT_URLS", ["https://fleet.test/hermes"])

    client = signaling.TeslaSignalingClient(get_token, "1152100--TEST")

    result = asyncio.run(client._get_hermes_jwt())

    assert result is None
    assert client._auth_denied is True
    assert client._stop_event.is_set() is True
    assert client.state == signaling.SignalingState.UNAVAILABLE
    assert client._hermes_jwt is None
    assert client._hermes_jwt_is_fallback is False
    assert client.health_status()["unavailable_reason"] == (
        "Tesla rejected the access token for Hermes JWT exchange "
        "because it is missing required scopes"
    )
    assert _FakeSession.post_calls == 1
    assert "missing required scopes" in caplog.text
    assert "Fleet API telemetry may still work" in caplog.text
    assert "Likely missing scope(s): user_data" in caplog.text
    assert not [record for record in caplog.records if record.levelname == "ERROR"]
