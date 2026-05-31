# QFit controller connections

Auto-generated documentation for signal/slot wiring. Regenerate:

```bash
python tests/scripts/generate_connections.py
```

**Edges parsed:** 116

## Clusters

| Cluster | Controller | Layer |
|---------|--------------|-------|
| A_import | meas_data_ctrl | Import → post-init |
| B_calibrate | calibration_ctrl, plotting (cali) | Calibrate |
| C_extract | extracting_ctrl, plotting (extract) | Extract |
| D_plot | plotting_ctrl | Canvas / plot bus |
| E_prefit | prefit_ctrl | Pre-fit sim |
| F_fit | fit_ctrl | Fit optimization |
| G_io | io_ctrl | Save/load |
| H_status | status.py | Status bar |

## Tests mapping

- **Layer 1:** `test_gui_stateful_fuzz.py`, `test_async_chaos.py`
- **Layer 2:** `test_connection_contracts.py` (~12 fan-out contracts)
- **Layer 3:** `tests/integration/test_scenario_*.py`
- **Layer 4:** `assert_public_api_consistent` in `tests/support/app_harness.py`

See [COVERAGE.md](COVERAGE.md) for the full GUI assurance strategy.
