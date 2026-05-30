# qfit test coverage

Last updated: 2026-05-30

Human-maintained inventory of what the test suite covers. An agent maintaining tests should read this file first, then open the linked test file for a module before editing production code.

---

## How to run

```bash
conda activate qfit          # or your env with qfit installed
pip install -e ".[test]"
export QT_QPA_PLATFORM=offscreen   # required on Linux CI; recommended locally

pytest -m "not slow" -v              # default CI job (~116 tests, ~18 s)
pytest -m slow -v                  # nightly: E2E, Quick Start sweep, notebook
pytest -m chaos -v                 # stateful fuzz only
pytest --cov=qfit --cov-report=term-missing -m "not slow"
```

**CI:** `.github/workflows/test.yml` — Ubuntu + macOS fast job; scheduled Ubuntu slow job.

**Markers:** `unit`, `gui`, `integration`, `chaos`, `slow`, `chaos_long` (see `pyproject.toml`).

---

## Test pattern legend

| Code | Name | Meaning |
|------|------|---------|
| A | Round-trip | Encode/decode or save/load restores input |
| B | Reference | Expected value from formula/constants independent of implementation |
| C | Identity | Structural relation (equality, sum-to-one, ordering) |
| D | Property | Shape, bounds, raises, type checks |
| E | Oracle | Compared to scipy/numpy/manual reimplementation |
| F | Cross-backend | Two code paths must agree (e.g. GUI vs YAML script API) |
| G | Smoke | Runs without crash; checks one invariant |
| H | Fixture | Depends on heavy file or HilbertSpace setup |
| I | Integration | Real scqubits / multi-component workflow |
| K | Mode invariant | GUI page ↔ internal mode flags stay consistent |
| N | Navigation fuzz | Random or fixed page/tool sequences; no crash + K |
| P | Synthetic canvas event | Matplotlib click injected via `PlottingCtrl`; no pixels |
| R | Registry torture | `.qfit` save/load after navigation or chaos |
| W | Widget contract | pytest-qt widget validation / enabled state |
| — | Skipped | Intentionally untested (reason in Deferred) |

Preferred order for pure logic: **A > B > C > D > E**.

---

## Suite summary

| Metric | Value |
|--------|-------|
| Test files | ~38 under `tests/` |
| Test count | 116 (`not slow`); +5 slow |
| Line coverage | ~68% of `qfit/` (includes generated `ui_designer/` at 100% compile-time lines) |
| Runtime | ~18 s without coverage (`not slow`) |

### GUI assurance layers (L1–L4)

Layers **reduce risk** of signal-chain bugs; they do **not** prove zero UI bugs in all action orderings.

| Layer | Purpose | Key files |
|-------|---------|-----------|
| **L1 — Situational fuzz** | Sample many UI contexts; crash/hang/invariant checks | `tests/test_gui_stateful_fuzz.py`, `tests/test_async_chaos.py`, `tests/support/fuzz_engine.py`, `tests/support/invariants.py` (K0–K6) |
| **L2 — Wiring safety** | ~12 P0 fan-out connection contracts | `tests/test_connection_contracts.py`, `tests/CONNECTIONS.md` |
| **L3 — User scenarios** | End-to-end stories with public-API or cost oracles | `tests/integration/test_scenario_*.py` |
| **L4 — Consistency** | Getters match UI; save/reload mid-flow | `assert_public_api_consistent` in `tests/support/app_harness.py`, `tests/test_registry_torture.py` |

**Foundation:** `tests/support/app_harness.py` — sole owner of `fit._*` access; GUI act via view widgets; assert via `get_*` / status bar / harness `get_cost()`.

Regenerate connection map: `python tests/scripts/generate_connections.py`

### What the app does (context for gaps)

QFit is a **PySide6 GUI** for fitting superconducting-circuit parameters to spectroscopy data. User workflow:

1. **Import** — load `.h5`/`.mat`/image, pick x/y axes  
2. **Calibrate** — map raw voltage → flux, raw frequency → GHz  
3. **Extract** — click peaks on canvas, label transitions  
4. **Pre-fit** — sliders + automatic scqubits sweeps  
5. **Fit** — numerical optimization (`wrapped_optimizer` + `FitModel`)

Shared state that tests focus on: `PlottingCtrl.dataDestination`, `CaliParamModel.caliStatus`, `QuantumModel.sweepUsage`, registry `.qfit` I/O.

---

## Test harness (`tests/conftest.py`)

| Fixture | Scope | Description |
|---------|-------|-------------|
| `qapp` | session | `QApplication`; sets `qfit.settings.EXECUTED_IN_IPYTHON = True` so `Fit` never calls `app.exec_()` |
| `fluxonium_resonator_hs` | session | scqubits HilbertSpace (fluxonium + resonator), truth params |
| `synthetic_h5_path` | session | `tests/fixtures/synthetic_twotone.h5` (generated if missing) |
| `headless_fit` | function | Fresh `Fit` on **import** page with synthetic h5 loaded |
| `loaded_fit` | module | Same as above but past import (axes set, `continueToPostImportStages` called) |
| `opened_quick_start` | module | `Fit.open(example_data/QFit_Quick_Start.qfit)` |

**Helpers:** `tests/helpers.py` re-exports from `tests/support/invariants.py` and `tests/support/app_harness.py`.

**Support modules:**

| Module | Role |
|--------|------|
| `tests/support/app_harness.py` | Build/open Fit, views/models accessors, workflow setup, `get_cost()` |
| `tests/support/invariants.py` | K0–K6 global invariants after fuzz/scenario steps |
| `tests/support/fuzz_engine.py` | State-aware event FSM for Layer 1 fuzz |

**Critical maintainer notes:**

- Teardown calls `MainWindow.hide()` only — **`close()` blocks pytest** indefinitely.  
- `loaded_fit` is **module-scoped** (one Fit per test file) for speed; use `headless_fit` when import page must be pristine.  
- `QuantumModel._autoRun = False` on fixtures to avoid background sweeps hanging the process.  
- `interruptCali()` is wired to **page nav button clicks**, not `PageView.switchToPage()`. Tests that assert cali interrupt must use `click_page_button(fit, "extract")`.

### Synthetic fixture

| File | Generator | Contents |
|------|-----------|----------|
| `tests/fixtures/synthetic_twotone.h5` | `tests/fixtures/generate_synthetic_h5.py` | 20×40 grid: `voltage`, `freq`, `mags`; Lorentzian dips from fluxonium-resonator eigenvalues + noise |
| `example_data/QFit_Quick_Start.qfit` | (committed example) | Full tutorial session for load/navigation tests |
| `example_data/qfit_config.yaml` | — | Multi-file partial_twotone import config |

---

## Coverage by package area

### `qfit/settings.py` — [`test_settings.py`](test_settings.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `COST_FUNCTION_TYPE` | tested | D | Must be `MSE` or `RMSE` |
| `color_dict` | tested | D | Keys for colormaps |
| `EXECUTED_IN_IPYTHON` | indirect | — | Forced `True` in conftest |
| Other constants | — | — | Display/cost defaults untested |

---

### `qfit/utils/helpers.py` — [`test_helpers.py`](test_helpers.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `isValid1dArray` | tested | B, D | Monotonic and non-monotonic cases |
| `isValid2dArray` | tested | D | Valid 2D vs vector/int rejection |
| `makeUnique` | tested | B | Duplicate name suffixing |
| `transposeEach` | tested | A | Matrix transpose list |
| `remove_nones` | tested | D | Dict filter |
| `OrderedDictMod` | tested | C | NumPy-aware equality |
| `DictItem` | tested | C | Equality |
| `_find_lorentzian_peak` | tested | D | Peak near center of synthetic Lorentzian |
| `ySnap` | tested | G | Returns y in range |
| `hasIdenticalRows` / `hasIdenticalCols` | deferred | D | Used by measurement import |
| `clearLayout` / `clearChildren` / `modifyStyleSheet` | deferred | W | Qt UI helpers |
| `disableButton` | deferred | W | |
| `Cmap` / `filter` | deferred | — | Plot styling |
| `labelLinesWithNans` | deferred | H | Matplotlib integration |
| `_find_continuous_segments` / `_check_position_overlap` | deferred | — | Plot label placement |
| `block_exec` / `block_exec_until` / `block_exec_until_success` | deferred | W | Jupyter + QTimer loop |
| `datetime_dir` | deferred | — | Export paths |

---

### `qfit/utils/export.py` — [`test_export.py`](test_export.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `FullCalibrationResult.get_mapped_sweep_params` | tested | B | Affine x map |
| `FullCalibrationResult.get_mapped_y` | tested | B | Affine y map |
| `ExtractedPointsResult.list_figures` | tested | D | |
| `ExtractedPointsResult.list_transitions` | tested | D | Missing figure raises |
| `PartialCalibrationResult` | deferred | B | Per-figure linear maps |
| `getExtractedPoints` | indirect | G | Via `Fit.get_extracted_points()` |
| `getCircuitParametersFromParamset` | indirect | G | Via `Fit.get_circuit_parameters()` |
| `getCalibrationResultFromParamset` | indirect | G | Via `Fit.get_calibration_result()` |
| `parseMappedParamName` | indirect | B | Used in FullCalibrationResult test setup |
| `augmented_raw_matrix` | deferred | — | Registry/cali export |
| `returnPrecursorFullXCalibration` / partial/y variants | deferred | B | Precursor cali reconstruction |

---

### `qfit/utils/load_reg_dict.py` — [`test_load_reg_dict.py`](test_load_reg_dict.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `_extract_version` | tested | D | Parses `3.0.1`; missing → `1.0.0` |
| `parseRegDict` | partial | D | Current `3.0.x` passthrough; v0 rejected |
| `_parseRegDict10xTo20x` | deferred | S | Needs golden v1 `.qfit` dict snippets in `tests/data/` |
| `_parseRegDict20x_21xTo22x` | deferred | S | |
| `_parseRegDict22xTo23x` | deferred | S | |
| `_parseMeasData10x_20x` / tag/cali migrators | deferred | S | |

---

### `qfit/utils/run_by_scripts.py` — [`test_run_by_scripts.py`](test_run_by_scripts.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `combinePath` | tested | D | Path joining |
| `dataPathsFromYaml` | tested | G | Reads `example_data/qfit_config.yaml` |
| `applyImport` | tested | F, G | Moves headless Fit to calibrate page |
| `applyFilters` | deferred | I | |
| `applyCalibration` | deferred | I | |
| `applyExtraction` | deferred | I | |
| `applyPrefit` | deferred | I | |
| `applyFit` | deferred | I | Full YAML pipeline |
| `applyConfigYaml` | deferred | I | End-to-end script entry |
| `generate_yaml_template` | deferred | G | Public API in `qfit/__init__.py` |

---

### `qfit/utils/wrapped_optimizer.py` — [`test_wrapped_optimizer.py`](test_wrapped_optimizer.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `Optimization.run` | tested | B, G | L-BFGS-B on 2D quadratic; fixed param |
| `OptTraj.final_target` / `final_para` | tested | B | Properties (not callables) |
| `MultiOpt` | deferred | I | Multi-start optimization |
| `OptTraj.save` / plotting | deferred | — | CSV/plot export |

---

### `qfit/models/registry.py` — [`test_registry.py`](test_registry.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `RegistryEntry` (r+) | tested | A, D | get/set/export |
| `RegistryEntry` (r) | tested | D | Readonly setter raises |
| `Registry.exportDict` | tested | A | Includes `version` |
| `Registry.register` | tested | G | Plain object registration |
| `Registry.clear` | tested | D | Keeps version |
| `Registry.exportPkl` / `dictFromFile` | tested | A | Via [`test_io_ctrl.py`](test_io_ctrl.py) |
| `Registry.setByDict` | indirect | R | Via `.qfit` reload tests |
| `Registrable._toRegistryEntry` | deferred | — | Covered via model registration indirectly |

---

### `qfit/models/data_structures.py` — [`test_data_structures.py`](test_data_structures.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `Tag` | tested | C, D | NO_TAG, DRESSED, equality, `transitionStr` |
| `Status` | tested | D | `__str__` contains type |
| `MeasRawXYConfig` | tested | D | Axis selection storage |
| `ExtrTransition` | tested | D | Empty count |
| `ExtrSpectra` / `FullExtr` | indirect | G | Via extraction workflow tests |
| `DeviTransition` / `DeviSpectra` / `FullDevi` | deferred | — | Fit deviation weighting |
| `PlotElement` hierarchy | deferred | — | Image/Meshgrid/Scatter/Spectrum/VLine |
| `ParamBase` / `SliderParam` / `FitParam` / `CaliTableRowParam` | deferred | D | Param table cells |
| `MeasMetaInfo` / `FilterConfig` | deferred | — | Import metadata |

---

### `qfit/models/parameter_settings.py` — [`test_parameter_settings.py`](test_parameter_settings.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `DEFAULT_PARAM_MINMAX` | tested | D | Min < max for EJ, EC |
| `QSYS_PARAM_NAMES` | tested | D | Fluxonium, Oscillator keys |
| `ParameterType` | — | — | Literal type only |

---

### `qfit/models/measurement_data.py` — [`test_measurement_data.py`](test_measurement_data.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `GenericH5Reader.fromFile` | tested | H, G | `synthetic_twotone.h5` |
| `ImageFileReader.fromFile` | tested | H, G | `example_data/transmons.jpg` |
| `MatlabReader.fromFile` | tested | H, G | `example_data/spec_scan_*.mat` |
| `LabberH5Reader` | deferred | H | No Labber fixture in repo |
| `CSVReader` | deferred | H | |
| `MeasDataSet` | indirect | G | Via Fit fixtures (import, store config) |
| `MeasurementData` methods | partial | — | transpose, filters, clip — untested directly |
| `NumericalMeasurementData.principalZ` | indirect | G | Image reader |

---

### `qfit/models/calibration.py` — [`test_calibration_model.py`](test_calibration_model.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `CaliParamModel.interruptCali` | tested | K | Clears `caliStatus`; tested via button click in chaos/mode tests |
| `CaliParamModel._figNames` | tested | G | Matches loaded measurement names |
| `CaliParamModel` x/y calibration math | deferred | B | 2-point linear map, `sendXCaliFunc` |
| `CaliParamModel.storeParamAttr` | deferred | W | Table edit → model |
| `CaliParamModel.plotCaliPtExtractStart/Finished` | deferred | P, K | Canvas → cali table |

---

### `qfit/models/numerical_model.py` — [`test_numerical_model.py`](test_numerical_model.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `QuantumModel.updateModeOnPageChange` | tested | K | prefit/fit/none for all pages |
| `QuantumModel.readyToOpt` | tested | D | False without extracted data |
| `QuantumModel.sweep2SpecCost` | deferred | I | Needs extracted points + sweep |
| `QuantumModel._runSweepInThread` | deferred | I | QThreadPool; disabled via `_autoRun=False` in tests |
| `SweepRunner` | deferred | I | Background scqubits sweep |

---

### `qfit/models/fit.py` — [`test_fit_model.py`](test_fit_model.py)

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `FitModel` existence | tested | G | On `loaded_fit` |
| `FitModel.runOptimization` | deferred | I | Real fit on synthetic data not run in CI |
| `FitRunner` | deferred | I | QThreadPool fit thread |
| `FitHSParams` / `FitCaliParams` | indirect | G | Exist on Fit instance |

---

### `qfit/models/extracted_data.py`

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `ActiveExtractedData.append` | indirect | G | [`integration/test_synthetic_fit.py`](integration/test_synthetic_fit.py) |
| `AllExtractedData.rowCount` / `switchFig` | indirect | G | Navigation + workflow tests |
| `AllExtractedData.insertRow` / `removeRow` | deferred | W | Labeling UI |
| `ActiveExtractedData.remove` | deferred | P | Click-near-point delete |

---

### `qfit/models/prefit.py` / `qfit/models/parameter_set.py` / `qfit/models/status.py`

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `PrefitHSParams` / `PrefitCaliParams` | indirect | G | `get_hilbertspace(source="prefit")` |
| `ParamSet` / `HSParamSet` / `SweepParamSet` | deferred | I | HS param sync |
| `StatusModel` | deferred | W | Status bar updates |

---

### `qfit/core/qfit.py` — Fit public API

| Symbol | Status | Pattern | Test file |
|--------|--------|---------|-----------|
| `Fit` import / `__version__` | tested | G | `integration/test_fit_public_api.py` |
| `Fit.__new__` / headless construction | tested | G | `conftest.py` |
| `get_hilbertspace` | tested | G | `integration/test_synthetic_fit.py` |
| `get_calibration_result` | tested | G | synthetic + loaded_fit |
| `get_circuit_parameters` | tested | G | synthetic + quick_start |
| `get_extracted_points` | tested | G | synthetic + quick_start |
| `Fit.open` | tested | R, G | `integration/test_quick_start_qfit.py` |
| `Fit.new` / `Fit.new_by_yaml` | deferred | I | Full constructor with exec |
| `create_standalone_canvas` | deferred | I | Extra matplotlib window |
| `show` / `hide` / `close` | deferred | — | Real event loop |

---

### `qfit/core/mainwindow.py`

| Symbol | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `MainWindow` | indirect | G | Constructed by all Fit fixtures |
| `MainWindow.registerAll` | deferred | A | Registry integration |

---

### Controllers

| Module | Status | Pattern | Test file | What is tested |
|--------|--------|---------|-----------|----------------|
| `io_ctrl.py` | partial | A, R | `test_io_ctrl.py` | Registry export to `.qfit`; not full `openFile`/`saveFile` dialogs |
| `plotting_ctrl.py` | partial | P | `test_plotting_ctrl.py` | `canvasClickMonitoring` routing; `toggleSelect`; pan ignores extract |
| `fit_ctrl.py` | partial | G, K | `test_fit_ctrl.py`, `test_async_chaos.py` | `_paramTuningEnabled` disables page buttons |
| `calibration_ctrl.py` | indirect | K | mode/chaos tests | `interruptCali` via page button wiring |
| `meas_data_ctrl.py` | indirect | G | conftest, `test_run_by_scripts.py` | `continueToPostImportStages` |
| `extracting_ctrl.py` | deferred | W | — | Transition list, tagging |
| `prefit_ctrl.py` | deferred | W, I | — | Slider → model, sweep settings |
| `settings.py` (ctrl) | deferred | — | Settings dialog |
| `status.py` (ctrl) | deferred | — | Status bar |
| `help_tooltip.py` | deferred | — | Help buttons |

---

### Views

| Module | Status | Pattern | Notes |
|--------|--------|---------|-------|
| `paging_view.py` — `PageView.switchToPage` | tested | K | Mode invariant tests |
| `paging_view.py` — `setEnabled` | indirect | K | Fit ctrl / async chaos |
| `calibration_view.py` | deferred | W | Table, EXTRACT RAW buttons |
| `importer_view.py` | deferred | W | Axis checkboxes, continue dialog |
| `labeling_view.py` | deferred | W | Transition tags |
| `prefit_view.py` / `fit_view.py` | partial | G | Widget existence; `setEnabled` behavior documented |
| `meas_data_view.py` / `status_bar.py` | deferred | — | |

---

### Widgets

| Module | Status | Pattern | Test file |
|--------|--------|---------|-----------|
| `validated_line_edits.py` | partial | W | `test_validated_line_edits.py` — Float, Int, MultiInts only |
| `validated_line_edits.py` | deferred | W | PositiveFloat, IntTuple, State, MultiIntTuples, MultiStates |
| `mpl_canvas.py` | partial | P | Via PlottingCtrl; no pixel/cursor tests |
| `grouped_sliders.py` | deferred | W | Prefit sliders |
| `custom_table.py` | deferred | W | Fit/cali tables |
| `data_extracting.py` | deferred | W | Transition list widget |
| `gif_tooltip.py` | — | — | Visual/media; out of scope |
| `menu.py` / `settings.py` (widget) | deferred | — | |

---

### `qfit/ui_designer/` (generated)

| Status | Reason |
|--------|--------|
| **—** (skipped) | All `Ui_*` classes generated from `.ui` files; recompiled on UI change. Do not unit test. Behavior covered indirectly when Fit starts. |

---

## GUI / chaos coverage (cross-cutting)

These tests assert **documented current behavior**, not ideal UX. Known quirk: page changes via `switchToPage` do not call `interruptCali`; only nav **button clicks** do.

| Test file | Markers | What it verifies |
|-----------|---------|------------------|
| [`test_mode_invariants.py`](test_mode_invariants.py) | gui, unit | After each page switch: `dataDestination`, `sweepUsage`; cali interrupt on button click |
| [`test_chaos_navigation.py`](test_chaos_navigation.py) | chaos, gui | Fixed page sequences + seeded random nav; no crash; K after each step |
| [`test_async_chaos.py`](test_async_chaos.py) | chaos, gui | Fit disables pages during `_paramTuningEnabled(False)`; prefit↔fit hops survive |
| [`test_registry_torture.py`](test_registry_torture.py) | chaos, gui | Export `.qfit` after navigation; dict parseable |

---

## Integration tests (`tests/integration/`)

| File | Markers | What it verifies |
|------|---------|------------------|
| [`test_synthetic_fit.py`](integration/test_synthetic_fit.py) | integration, gui | Import → extract points → prefit page; public export APIs on `loaded_fit` |
| [`test_quick_start_qfit.py`](integration/test_quick_start_qfit.py) | integration, gui | Load committed `.qfit`; navigate all pages; export APIs |
| [`test_fit_public_api.py`](integration/test_fit_public_api.py) | integration | `import qfit`; `Fit` class exists |
| [`test_yaml_pipeline.py`](integration/test_yaml_pipeline.py) | integration | YAML lists 6 partial_twotone files |
| [`test_notebook_smoke.py`](integration/test_notebook_smoke.py) | slow | Quick Start notebook is valid JSON nbformat |

**Not yet tested:** full notebook cell execution; real optimization converging to truth params; multi-file YAML fit pipeline.

---

## Deferred (prioritized backlog)

| Area | Symbol / feature | Why deferred | Suggested pattern |
|------|------------------|--------------|-------------------|
| Registry migration | `load_reg_dict` v1→v3 migrators | Need golden dict fixtures | S |
| Script API | `applyConfigYaml`, `applyFit` | Slow; needs full YAML + HS | I, F |
| Calibration math | 2-point x/y affine in `CaliParamModel` | Logic exists; no isolated unit tests | B |
| Numerical sweep | `sweep2SpecCost`, `SweepRunner` | scqubits + thread pool; slow | I, M |
| Real fit | `FitModel.runOptimization` end-to-end | CI time; needs synthetic points + guess params | I |
| Extracting UI | peak delete, y-snap on canvas | Needs synthetic canvas + cali | P |
| Controllers | `extracting_ctrl`, `prefit_ctrl`, `calibration_ctrl` slots | Thin wiring; need widget interaction | W, G |
| Views | importer continue `QMessageBox`, cali table | Dialog + table widgets | W |
| Validators | remaining `*LineEdit` subclasses | Copy pattern from existing tests | W |
| `LabberH5Reader` | Labber-format h5 | No fixture file | H |
| Plot elements | `SpectrumElement`, filters on meas data | Matplotlib-heavy | — |
| App hardening | block nav during async sweep/fit | Product change; tests document current behavior only | K, N |

---

## Out of scope

- `example_notebooks/` — user documentation, not package API (slow JSON smoke only)
- `example_data/` — fixtures, not tested themselves
- `resources/` — UI assets, images, videos
- `qfit/ui_designer/resources_rc.py` — Qt resource binary
- Pixel/visual regression of matplotlib canvas
- `Fit.app.exec_()` interactive event loop
- Windows-specific CI (publish workflow has install smoke only)

---

## Line coverage snapshot

Refresh: `pytest -m "not slow" --cov=qfit --cov-report=term-missing -q`

| Area | Approx. coverage | Largest untested areas |
|------|------------------|------------------------|
| `qfit/utils/` | 50–60% | `run_by_scripts`, `load_reg_dict` migrators, Qt helpers |
| `qfit/models/` | 40–70% | `fit.py`, `measurement_data.py` filters, plot elements |
| `qfit/controllers/` | 30–50% | Most ctrl modules except indirect paths |
| `qfit/views/` | 75–95% | Mostly constructed at Fit startup |
| `qfit/widgets/` | 60–75% | `mpl_canvas` rendering paths |
| `qfit/ui_designer/` | ~100% lines | Generated; not meaningful |
| **Total** | **~68%** | Controllers + script API + fit pipeline |

---

## Changelog

Newest first.

- **2026-05-30:** Expanded COVERAGE.md to per-module symbol inventory; removed planning-phase references; documented harness quirks and deferred backlog.
- **2026-05-30:** Initial suite — 96 tests, synthetic h5 fixture, CI workflow `test.yml`, GUI mode/chaos/registry tests.
