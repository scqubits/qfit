#!/usr/bin/env python
"""Generate tests/fixtures/synthetic_twotone.h5 for the test suite.

Run once after changing truth parameters or grid size:
    python tests/fixtures/generate_synthetic_h5.py
"""
from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np
import scqubits as scq

TRUTH_PARAMS = {
    "EJ": 3.2,
    "EC": 0.95,
    "EL": 0.23,
    "E_osc": 6.035,
    "g": 0.106,
}

N_VOLTAGE = 20
N_FREQ = 40
NOISE_STD = 0.08
RNG_SEED = 42


def build_hilbert_space() -> scq.HilbertSpace:
    fluxonium = scq.Fluxonium(
        EJ=TRUTH_PARAMS["EJ"],
        EC=TRUTH_PARAMS["EC"],
        EL=TRUTH_PARAMS["EL"],
        flux=0.5,
        cutoff=40,
        truncated_dim=4,
        id_str="Fluxonium",
    )
    resonator = scq.Oscillator(
        E_osc=TRUTH_PARAMS["E_osc"],
        l_osc=1.0,
        truncated_dim=3,
        id_str="Resonator",
    )
    hs = scq.HilbertSpace([fluxonium, resonator])
    hs.add_interaction(
        g=TRUTH_PARAMS["g"],
        op1=fluxonium.n_operator,
        op2=resonator.annihilation_operator,
        add_hc=True,
        id_str="res-qubit",
    )
    return hs


def transition_frequencies_ghz(hs: scq.HilbertSpace, flux_values: np.ndarray) -> np.ndarray:
    """Plasmon transition frequency (GHz) vs external flux."""
    freqs = []
    for flux in flux_values:
        hs["Fluxonium"].flux = float(flux)
        hs.generate_lookup()
        evals = hs.eigenvals(evals_count=3)
        freqs.append(float(evals[2] - evals[0]))
    return np.array(freqs)


def synthesize_mags(
    voltage: np.ndarray,
    freq: np.ndarray,
    peak_freqs_ghz: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """Build magnitude grid with Lorentzian dips at transition lines."""
    mags = 0.85 + 0.05 * rng.standard_normal((len(voltage), len(freq)))
    gamma = 0.04
    for i, peak in enumerate(peak_freqs_ghz):
        line = 1.0 / (1.0 + ((freq - peak) / gamma) ** 2)
        mags[i, :] -= 0.35 * line
    mags = np.clip(mags, 0.05, 1.0)
    mags += NOISE_STD * rng.standard_normal(mags.shape)
    return np.clip(mags, 0.0, 1.0)


def write_synthetic_h5(path: Path) -> None:
    rng = np.random.default_rng(RNG_SEED)
    hs = build_hilbert_space()

    voltage = np.linspace(-0.4, 0.4, N_VOLTAGE)
    flux_values = 0.5 + voltage / 2.0
    peak_freqs = transition_frequencies_ghz(hs, flux_values)

    f_min, f_max = peak_freqs.min() - 0.3, peak_freqs.max() + 0.3
    freq = np.linspace(f_min, f_max, N_FREQ)
    mags = synthesize_mags(voltage, freq, peak_freqs, rng)

    path.parent.mkdir(parents=True, exist_ok=True)
    with h5py.File(path, "w") as f:
        f.create_dataset("voltage", data=voltage)
        f.create_dataset("freq", data=freq)
        f.create_dataset("mags", data=mags)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "synthetic_twotone.h5"
    write_synthetic_h5(out)
    print(f"Wrote {out}")
