"""State-aware GUI fuzz tests (Layer 1)."""
import random

import pytest

from tests.support.fuzz_engine import LEGACY_FIXED_SEQUENCES, run_fuzz_sequence, run_legacy_page_sequence
from tests.support.invariants import leave_calibrate_interrupts_cali

pytestmark = [pytest.mark.chaos, pytest.mark.gui]


@pytest.mark.parametrize("seed", list(range(5)))
def test_stateful_fuzz_seeded(loaded_fit, qapp, seed):
    rng = random.Random(seed)
    run_fuzz_sequence(loaded_fit, qapp, rng, n_steps=50, skip_k4=True)


@pytest.mark.parametrize("pages", LEGACY_FIXED_SEQUENCES)
def test_legacy_fixed_page_sequences(loaded_fit, qapp, pages):
    run_legacy_page_sequence(loaded_fit, qapp, pages)


def test_cali_extract_then_page_hop(loaded_fit, qapp):
    leave_calibrate_interrupts_cali(loaded_fit, qapp)
    from tests.support.invariants import assert_all_invariants

    assert_all_invariants(loaded_fit, qapp, skip=["K4"])
