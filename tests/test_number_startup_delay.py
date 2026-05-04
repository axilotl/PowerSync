"""Regression test: capability-gated task must not be created for non-Tesla installs.

HA's bootstrap wrap-up waits for all tasks registered via hass.async_create_task()
to drain. The _add_capability_gated_numbers task polls for 120 s when no Tesla
site is present, causing a visible startup delay for every non-Tesla user.

The fix gates hass.async_create_task() behind the same tesla_site_id check
already used for BackupReserveNumber.
"""

from __future__ import annotations

import ast
from pathlib import Path

NUMBER_PATH = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "power_sync"
    / "number.py"
)


def _find_function(tree: ast.AST, name: str) -> ast.AsyncFunctionDef | ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    raise AssertionError(f"function '{name}' not found in {NUMBER_PATH}")


def _all_create_task_calls(tree: ast.AST) -> list[ast.Call]:
    """Return every hass.async_create_task() Call node in the tree."""
    calls = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "async_create_task"
        ):
            calls.append(node)
    return calls


def _tesla_site_id_check_linenos(setup_fn: ast.AsyncFunctionDef) -> set[int]:
    """Return line numbers of If-nodes in setup_fn that test tesla_site_id."""
    linenos: set[int] = set()
    for node in ast.walk(setup_fn):
        if not isinstance(node, ast.If):
            continue
        test = node.test
        # Matches bare `if tesla_site_id:` (Name node)
        if isinstance(test, ast.Name) and test.id == "tesla_site_id":
            linenos.add(node.lineno)
    return linenos


def test_capability_gated_task_guarded_by_tesla_site_id():
    """hass.async_create_task for _add_capability_gated_numbers must sit inside
    an `if tesla_site_id:` block, not at the top level of async_setup_entry."""
    source = NUMBER_PATH.read_text()
    tree = ast.parse(source)

    setup_fn = _find_function(tree, "async_setup_entry")
    create_task_calls = _all_create_task_calls(setup_fn)

    assert create_task_calls, "Expected at least one hass.async_create_task() call"

    guard_linenos = _tesla_site_id_check_linenos(setup_fn)
    assert guard_linenos, (
        "No `if tesla_site_id:` guard found in async_setup_entry — "
        "the capability-gated task would run for all users"
    )

    lines = source.splitlines()

    for call in create_task_calls:
        call_line = call.lineno
        # Find the innermost If-guard that contains this call line.
        enclosing_guards = [ln for ln in guard_linenos if ln < call_line]
        assert enclosing_guards, (
            f"hass.async_create_task() at line {call_line} is NOT inside any "
            f"`if tesla_site_id:` block — non-Tesla users will wait 120 s at startup.\n"
            f"  Call site: {lines[call_line - 1].strip()}"
        )


def test_capability_gated_numbers_inner_function_unchanged():
    """_add_capability_gated_numbers itself should still poll for tesla_capabilities."""
    tree = ast.parse(NUMBER_PATH.read_text())
    setup_fn = _find_function(tree, "async_setup_entry")

    # The inner function must still exist inside async_setup_entry
    inner = None
    for node in ast.walk(setup_fn):
        if (
            isinstance(node, ast.AsyncFunctionDef)
            and node.name == "_add_capability_gated_numbers"
        ):
            inner = node
            break

    assert inner is not None, "_add_capability_gated_numbers not found inside async_setup_entry"

    # It must still reference "tesla_capabilities" (unchanged polling logic)
    names = {
        node.value if isinstance(node, ast.Constant) else None
        for node in ast.walk(inner)
    }
    assert "tesla_capabilities" in names, (
        "_add_capability_gated_numbers no longer references 'tesla_capabilities' — "
        "the inner polling logic may have been removed unintentionally"
    )
