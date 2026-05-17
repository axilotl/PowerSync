"""Tests for price spike alert timestamp formatting."""

from __future__ import annotations

import sys
import types
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent / "custom_components" / "power_sync"
_ps = types.ModuleType("power_sync")
_ps.__path__ = [str(ROOT)]
sys.modules["power_sync"] = _ps

homeassistant = types.ModuleType("homeassistant")
homeassistant_util = types.ModuleType("homeassistant.util")
homeassistant_dt = types.ModuleType("homeassistant.util.dt")
homeassistant_dt.now = lambda: datetime.now().astimezone()
homeassistant_util.dt = homeassistant_dt
homeassistant.util = homeassistant_util
sys.modules.setdefault("homeassistant", homeassistant)
sys.modules.setdefault("homeassistant.util", homeassistant_util)
sys.modules.setdefault("homeassistant.util.dt", homeassistant_dt)

from power_sync.tariff_converter import (  # noqa: E402
    format_spike_alert_time,
    spike_alert_key_time,
    spike_is_imminent,
)


BRISBANE = ZoneInfo("Australia/Brisbane")


def test_spike_alert_time_labels_today_in_local_time():
    now = datetime(2026, 5, 17, 12, 46, tzinfo=BRISBANE)

    assert (
        format_spike_alert_time("2026-05-17T18:30:00+10:00", now=now)
        == "Today 6:30 pm"
    )


def test_spike_alert_time_labels_tomorrow():
    now = datetime(2026, 5, 17, 12, 46, tzinfo=BRISBANE)

    assert (
        format_spike_alert_time("2026-05-18T17:00:00+10:00", now=now)
        == "Tomorrow 5:00 pm"
    )


def test_spike_alert_time_converts_utc_to_local_day():
    now = datetime(2026, 5, 17, 12, 46, tzinfo=BRISBANE)

    assert (
        format_spike_alert_time("2026-05-17T07:30:00Z", now=now)
        == "Today 5:30 pm"
    )


def test_spike_alert_key_distinguishes_same_time_on_different_days():
    today_key = spike_alert_key_time("2026-05-17T17:00:00+10:00")
    tomorrow_key = spike_alert_key_time("2026-05-18T17:00:00+10:00")

    assert today_key != tomorrow_key


def test_spike_is_imminent_only_for_current_or_next_hour():
    now = datetime(2026, 5, 17, 12, 46, tzinfo=BRISBANE)

    assert spike_is_imminent("2026-05-17T13:30:00+10:00", now=now) is True
    assert spike_is_imminent("2026-05-17T14:00:00+10:00", now=now) is False
