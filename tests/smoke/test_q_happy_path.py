"""Smoke: ``q`` resolves a signature in a subprocess (PS-211).

Subprocess-driven (``sys.executable -c ...``) so this proves the
installed package resolves its hard dependencies — an in-process call
would not. Hermetic: stdlib ``json`` target, no network, no
credentials, no writes outside tmp dirs.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

pytestmark = pytest.mark.smoke

CODE = "\n".join(
    [
        "import scitex_introspect as ix",
        "info = ix.q('json.loads')",
        "print((info['success'], info['name']))",
    ]
)


def test_q_signature_in_subprocess() -> None:
    # Arrange
    argv = [sys.executable, "-c", CODE]

    # Act
    completed = subprocess.run(argv, capture_output=True, text=True, timeout=30)

    # Assert
    assert (completed.returncode, completed.stdout.strip()) == (0, "(True, 'loads')")
