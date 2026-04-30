"""Tests for Powerwall local login rate-limit handling."""

from __future__ import annotations

import asyncio
import importlib.util
import sys
import types
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest


ROOT = Path(__file__).resolve().parent.parent / "custom_components" / "power_sync"
PKG = "power_sync_rate_limit_test"
LOCAL_PKG = f"{PKG}.powerwall_local"


def _ensure_test_package() -> None:
    pkg = types.ModuleType(PKG)
    pkg.__path__ = [str(ROOT)]
    sys.modules[PKG] = pkg

    local_pkg = types.ModuleType(LOCAL_PKG)
    local_pkg.__path__ = [str(ROOT / "powerwall_local")]
    sys.modules[LOCAL_PKG] = local_pkg


def _load_module(name: str, path: Path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_ensure_test_package()
transport_mod = _load_module(
    f"{LOCAL_PKG}.transport",
    ROOT / "powerwall_local" / "transport.py",
)
client_mod = _load_module(
    f"{LOCAL_PKG}.client",
    ROOT / "powerwall_local" / "client.py",
)


class _FakeResponse:
    def __init__(
        self,
        status: int,
        *,
        body: str = "",
        json_body: dict | None = None,
        headers: dict | None = None,
        delay: float = 0.0,
    ) -> None:
        self.status = status
        self.headers = headers or {}
        self._body = body
        self._json_body = json_body or {}
        self._delay = delay

    async def __aenter__(self):
        if self._delay:
            await asyncio.sleep(self._delay)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def text(self) -> str:
        return self._body

    async def json(self) -> dict:
        return self._json_body


class _FakeSession:
    def __init__(self, calls: dict[str, int], response: _FakeResponse) -> None:
        self._calls = calls
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def post(self, *args, **kwargs):
        self._calls["post"] = self._calls.get("post", 0) + 1
        return self._response


def _transport_with_response(response: _FakeResponse):
    transport = transport_mod.TEDAPIv1rTransport.__new__(
        transport_mod.TEDAPIv1rTransport
    )
    transport._host = "gateway.local"
    transport._customer_password = "password"
    transport._token = None
    transport._din = None
    transport._login_lock = asyncio.Lock()
    transport._login_backoff_until = 0.0
    transport._login_backoff_seconds = 0.0
    transport._last_login_backoff_log = 0.0

    calls: dict[str, int] = {}

    async def _session():
        return _FakeSession(calls, response)

    transport._session = _session
    return transport, calls


def test_v1r_login_429_sets_backoff_and_skips_retry():
    async def _run():
        transport, calls = _transport_with_response(
            _FakeResponse(
                429,
                body='{"code":429,"message":"API Limit Reached"}',
            )
        )

        assert await transport.login() is False
        assert calls["post"] == 1
        assert transport.login_backoff_remaining > 0

        assert await transport.login() is False
        assert calls["post"] == 1

    asyncio.run(_run())


def test_v1r_login_lock_collapses_concurrent_attempts():
    async def _run():
        transport, calls = _transport_with_response(
            _FakeResponse(200, json_body={"token": "token-123"}, delay=0.01)
        )

        results = await asyncio.gather(*(transport.login() for _ in range(5)))

        assert results == [True] * 5
        assert calls["post"] == 1
        assert transport._token == "token-123"

    asyncio.run(_run())


def test_snapshot_fails_fast_when_login_is_rate_limited():
    async def _run():
        client = client_mod.PowerwallLocalClient.__new__(
            client_mod.PowerwallLocalClient
        )
        client._transport = SimpleNamespace(
            login=AsyncMock(return_value=False),
            login_backoff_remaining=42.0,
        )
        client._unsigned = None

        with pytest.raises(
            client_mod.PowerwallUnreachableError,
            match="Gateway login rate-limited",
        ):
            await client.get_snapshot()

        client._transport.login.assert_awaited_once()

    asyncio.run(_run())
