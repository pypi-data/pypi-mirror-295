# This code is a Qiskit project.

# (C) Copyright IBM 2024.

# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for the optimization_settings module."""

from __future__ import annotations

import pytest
from circuit_knitting.cutting.cut_finding.optimization_settings import (
    OptimizationSettings,
)


@pytest.mark.parametrize(
    "max_gamma, max_backjumps ",
    [(0, 1), (-1, 0), (1, -1)],
)
def test_optimization_parameters(max_gamma: int, max_backjumps: int):
    """Test optimization parameters for being valid data types."""

    with pytest.raises(ValueError):
        _ = OptimizationSettings(max_gamma=max_gamma, max_backjumps=max_backjumps)


def test_gate_cut_types(LO: bool = True, LOCC_ancillas: bool = False):
    """Test default gate cut types."""
    op = OptimizationSettings(LO, LOCC_ancillas)
    op.set_gate_cut_types()
    assert op.gate_cut_LO is True
    assert op.gate_cut_LOCC_with_ancillas is False


def test_wire_cut_types(
    LO: bool = True, LOCC_ancillas: bool = False, LOCC_no_ancillas: bool = False
):
    """Test default wire cut types."""
    op = OptimizationSettings(LO, LOCC_ancillas, LOCC_no_ancillas)
    op.set_wire_cut_types()
    assert op.wire_cut_LO
    assert op.wire_cut_LOCC_with_ancillas is False
    assert op.wire_cut_LOCC_no_ancillas is False


def test_all_cut_search_groups():
    """Test for the existence of all cut search groups."""
    assert OptimizationSettings(
        LO=True, LOCC_ancillas=True, LOCC_no_ancillas=True
    ).get_cut_search_groups() == [None, "GateCut", "WireCut"]
