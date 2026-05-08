"""Shared pytest hygiene for PowerSync unit tests."""

from __future__ import annotations

import sys

import pytest


@pytest.fixture(autouse=True)
def restore_real_power_sync_const():
    """Prevent module-level const stubs leaking into unrelated tests."""
    const_module = sys.modules.get("power_sync.const")
    if const_module is not None and not getattr(const_module, "__file__", None):
        sys.modules.pop("power_sync.const", None)

    aiohttp_module = sys.modules.get("aiohttp")
    if (
        aiohttp_module is not None
        and not getattr(aiohttp_module, "__file__", None)
        and not hasattr(aiohttp_module, "ClientSession")
    ):
        sys.modules.pop("aiohttp", None)

    yield
