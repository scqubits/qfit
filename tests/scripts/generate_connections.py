#!/usr/bin/env python
"""Generate tests/connections.yaml and tests/CONNECTIONS.md from controller connects."""
from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterator

REPO = Path(__file__).resolve().parents[2]
CONTROLLERS = REPO / "qfit" / "controllers"
OUT_YAML = REPO / "tests" / "connections.yaml"
OUT_MD = REPO / "tests" / "CONNECTIONS.md"

CLUSTER_BY_FILE = {
    "meas_data_ctrl.py": "A_import",
    "calibration_ctrl.py": "B_calibrate",
    "extracting_ctrl.py": "C_extract",
    "plotting_ctrl.py": "D_plot",
    "prefit_ctrl.py": "E_prefit",
    "fit_ctrl.py": "F_fit",
    "io_ctrl.py": "G_io",
    "status.py": "H_status",
}


def _iter_connect_calls(path: Path) -> Iterator[tuple[int, str]]:
    text = path.read_text()
    for i, line in enumerate(text.splitlines(), start=1):
        if ".connect(" in line:
            yield i, line.strip()


def generate_yaml() -> str:
    lines = ["# Auto-generated connection inventory", "edges:"]
    for path in sorted(CONTROLLERS.glob("*.py")):
        cluster = CLUSTER_BY_FILE.get(path.name, "other")
        for lineno, src in _iter_connect_calls(path):
            lines.append(f"  - cluster: {cluster}")
            lines.append(f"    file: {path.relative_to(REPO)}")
            lines.append(f"    line: {lineno}")
            lines.append(f"    code: {src!r}")
    return "\n".join(lines) + "\n"


def generate_md(edge_count: int) -> str:
    return f"""# QFit controller connections

Auto-generated documentation for signal/slot wiring. Regenerate:

```bash
python tests/scripts/generate_connections.py
```

**Edges parsed:** {edge_count}

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
"""


def main() -> None:
    yaml_text = generate_yaml()
    edge_count = yaml_text.count("- cluster:")
    OUT_YAML.write_text(yaml_text)
    OUT_MD.write_text(generate_md(edge_count))
    print(f"Wrote {OUT_YAML} ({edge_count} edges)")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
