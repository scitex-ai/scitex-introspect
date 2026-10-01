"""E2E: q → resolve_object → list_api pipeline on stdlib json (PS-212).

No network, no mocks — drives the real introspection helpers end to
end. Gated on ``RUN_E2E=1`` so the default unit run stays fast.
"""

from __future__ import annotations

import os

import pytest

pytestmark = [pytest.mark.e2e, pytest.mark.skipif(os.environ.get("RUN_E2E") != "1", reason="RUN_E2E!=1")]


def test_introspection_pipeline_roundtrip() -> None:
    import json

    import scitex_introspect as ix

    # Arrange
    target = "json.loads"

    # Act
    info = ix.q(target)
    resolved, error = ix.resolve_object(target)
    df = ix.list_api(json, columns=["Name"])

    # Assert
    assert (info["success"], info["name"], resolved is json.loads, len(df) > 0) == (True, "loads", True, True)
