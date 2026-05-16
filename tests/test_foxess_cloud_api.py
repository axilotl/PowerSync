"""Regression tests for FoxESS Cloud API helpers."""

from __future__ import annotations

import asyncio
import hashlib
import importlib
import sys
import types
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = ROOT / "custom_components" / "power_sync"
_SENTINEL = object()


@pytest.fixture()
def foxess_api_module():
    saved_modules = {
        name: sys.modules.get(name, _SENTINEL)
        for name in ("power_sync", "power_sync.foxess_api", "power_sync.const")
    }

    power_sync = types.ModuleType("power_sync")
    power_sync.__path__ = [str(COMPONENT_ROOT)]
    sys.modules["power_sync"] = power_sync

    try:
        yield importlib.import_module("power_sync.foxess_api")
    finally:
        sys.modules.pop("power_sync.foxess_api", None)
        for name, module in saved_modules.items():
            if module is _SENTINEL:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


def test_signature_uses_literal_crlf_separator(foxess_api_module, monkeypatch):
    monkeypatch.setattr(foxess_api_module.time, "time", lambda: 1712345678.901)

    client = foxess_api_module.FoxESSCloudClient("api-key", "INV123")
    headers = client._generate_signature("/op/v0/device/list")

    expected = hashlib.md5(
        b"/op/v0/device/list\\r\\napi-key\\r\\n1712345678901"
    ).hexdigest()
    crlf_signature = hashlib.md5(
        b"/op/v0/device/list\r\napi-key\r\n1712345678901"
    ).hexdigest()
    assert headers["timestamp"] == "1712345678901"
    assert headers["signature"] == expected
    assert headers["signature"] != crlf_signature


def test_real_data_query_uses_v1_sns_shape(foxess_api_module, monkeypatch):
    client = foxess_api_module.FoxESSCloudClient("api-key", "INV123")
    calls = []

    async def fake_post(path, payload, *, write=False):
        calls.append((path, payload, write))
        return {"ok": True}

    monkeypatch.setattr(client, "_post", fake_post)

    result = asyncio.run(client.get_real_data())

    assert result == {"ok": True}
    assert calls == [
        (
            "/op/v1/device/real/query",
            {
                "sns": ["INV123"],
                "variables": [
                    "pvPower",
                    "gridConsumptionPower",
                    "feedinPower",
                    "loadsPower",
                    "batPower",
                    "SoC",
                    "workMode",
                    "generationPower",
                    "chargePower",
                    "dischargePower",
                    "chargeEnergyToTal",
                    "dischargeEnergyToTal",
                ],
            },
            False,
        )
    ]


def test_scheduler_set_uses_v3_groups_and_extra_param(foxess_api_module, monkeypatch):
    client = foxess_api_module.FoxESSCloudClient("api-key", "INV123")
    calls = []

    async def fake_post(path, payload, *, write=False):
        calls.append((path, payload, write))
        return {"ok": True}

    monkeypatch.setattr(client, "_post", fake_post)

    asyncio.run(
        client.set_scheduler(
            "INV123",
            [
                {
                    "startHour": 1,
                    "startMinute": 30,
                    "endHour": 2,
                    "endMinute": 0,
                    "workMode": "ForceCharge",
                    "minSocOnGrid": 20,
                    "fdSoc": 90,
                    "fdPwr": 5000,
                    "maxSoc": 95,
                }
            ],
        )
    )

    path, payload, write = calls[0]
    assert path == "/op/v3/device/scheduler/enable"
    assert write is True
    assert payload["deviceSN"] == "INV123"
    assert payload["groups"][0]["workMode"] == "ForceCharge"
    assert payload["groups"][0]["extraParam"] == {
        "minSocOnGrid": 20.0,
        "fdSoc": 90.0,
        "fdPwr": 5000.0,
        "maxSoc": 95.0,
        "importLimit": 30000.0,
        "exportLimit": 30000.0,
        "pvLimit": 30000.0,
        "reactivePower": 0.0,
    }
    assert "minSocOnGrid" not in payload["groups"][0]
    assert "fdPwr" not in payload["groups"][0]


def test_setting_soc_and_modbus_passthrough_payloads(foxess_api_module, monkeypatch):
    client = foxess_api_module.FoxESSCloudClient("api-key", "INV123")
    post_calls = []
    get_calls = []

    async def fake_post(path, payload, *, write=False):
        post_calls.append((path, payload, write))
        return {"ok": True}

    async def fake_get(path, params):
        get_calls.append((path, params))
        return {"ok": True}

    monkeypatch.setattr(client, "_post", fake_post)
    monkeypatch.setattr(client, "_get", fake_get)

    asyncio.run(client.set_device_setting("WorkMode", "SelfUse"))
    asyncio.run(client.get_battery_soc())
    asyncio.run(client.set_battery_soc(120, -5))
    asyncio.run(client.send_modbus_command("LOGGER1", "AQIDBA==", timeout=12))

    assert post_calls[0] == (
        "/op/v0/device/setting/set",
        {"sn": "INV123", "key": "WorkMode", "value": "SelfUse"},
        True,
    )
    assert get_calls == [("/op/v0/device/battery/soc/get", {"sn": "INV123"})]
    assert post_calls[1] == (
        "/op/v0/device/battery/soc/set",
        {"sn": "INV123", "minSoc": 100, "minSocOnGrid": 0},
        True,
    )
    assert post_calls[2] == (
        "/op/v0/module/modbus/commands",
        {"sn": "LOGGER1", "timeout": 12, "data": "AQIDBA=="},
        True,
    )


def test_scheduler_helpers_filter_hidden_defaults_and_extract_serials(foxess_api_module):
    assert foxess_api_module._extract_device_sn({"deviceSN": "AAA"}) == "AAA"
    assert foxess_api_module._extract_device_sn({"sn": "BBB"}) == "BBB"
    assert foxess_api_module._extract_device_sn({"serialNumber": "CCC"}) == "CCC"

    filtered = foxess_api_module.filter_public_scheduler_groups(
        [
            {"isRemainMode": True, "workMode": "SelfUse"},
            {
                "startHour": 0,
                "startMinute": 0,
                "endHour": 23,
                "endMinute": 59,
                "workMode": "SelfUse",
            },
            {
                "startHour": 6,
                "startMinute": 0,
                "endHour": 7,
                "endMinute": 30,
                "workMode": "ForceDischarge",
                "fdPwr": 3000,
            },
        ]
    )

    assert len(filtered) == 1
    assert filtered[0]["workMode"] == "ForceDischarge"
    assert filtered[0]["extraParam"]["fdPwr"] == 3000.0


def test_price_conversion_emits_scheduler_v3_extra_params(foxess_api_module):
    groups = foxess_api_module.convert_prices_to_foxess_schedule(
        buy_prices=[
            {"timeRange": "00:00-00:30", "price": 1.0},
            {"timeRange": "00:30-01:00", "price": 30.0},
        ],
        sell_prices=[
            {"timeRange": "00:00-00:30", "price": 0.0},
            {"timeRange": "00:30-01:00", "price": 50.0},
        ],
        min_soc=25,
        charge_soc=85,
    )

    assert [group["workMode"] for group in groups] == [
        "ForceCharge",
        "ForceDischarge",
    ]
    assert groups[0]["extraParam"]["minSocOnGrid"] == 25.0
    assert groups[0]["extraParam"]["fdSoc"] == 85.0
    assert groups[1]["extraParam"]["fdSoc"] == 25.0
    assert "fdPwr" not in groups[0]
