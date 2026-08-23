# blas_threads.py
#
# Limit OpenBLAS / OpenMP threads used by NumPy and SciPy.
#
# Typical qfit Hilbert spaces are small. On Apple Silicon, the default
# OpenBLAS thread count (one per core) makes scipy.linalg.expm tens of
# times slower and can overflow Qt worker stacks (see SweepRunner).
# NumPy and SciPy often ship *different* libopenblas copies; both must
# be limited.
############################################################################

from __future__ import annotations

import ctypes
import os
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

_DEFAULT_THREADS = 1
_ENV_KEYS = (
    "OPENBLAS_NUM_THREADS",
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)
_LIB_PATTERNS = (
    "libopenblas*.dylib",
    "libopenblasp*.dylib",
    "libopenblas.so*",
    "libopenblasp*.so*",
    "*openblas*.dll",
)


def _resolved_thread_count(n: Optional[int] = None) -> int:
    if n is not None:
        return max(1, int(n))
    existing = os.environ.get("OPENBLAS_NUM_THREADS") or os.environ.get(
        "OMP_NUM_THREADS"
    )
    if existing:
        try:
            return max(1, int(existing))
        except ValueError:
            pass
    return _DEFAULT_THREADS


def apply_blas_thread_env(n: Optional[int] = None) -> int:
    """
    Set thread-count environment variables if the user has not already.

    Call this before importing NumPy / SciPy when possible.
    """
    n = _resolved_thread_count(n)
    for key in _ENV_KEYS:
        os.environ.setdefault(key, str(n))
    return n


def _package_search_roots() -> List[Tuple[Path, bool]]:
    """
    Return (directory, recurse) pairs.

    Recurse only into NumPy / SciPy packages (they vendor OpenBLAS in
    hidden ``.dylibs`` / ``.libs`` folders). Conda ``env/lib`` is
    searched one level.
    """
    roots: List[Tuple[Path, bool]] = []
    for mod_name in ("numpy", "scipy"):
        try:
            mod = __import__(mod_name)
        except ImportError:
            continue
        pkg = Path(mod.__file__).resolve().parent
        roots.append((pkg, True))
        for parent in pkg.parents:
            lib = parent / "lib"
            if lib.is_dir():
                roots.append((lib, False))
                break
    return roots


def _iter_openblas_libs(roots: Iterable[Tuple[Path, bool]]) -> List[Path]:
    found: List[Path] = []
    seen: set[str] = set()
    for root, recurse in roots:
        if not root.exists():
            continue
        for pattern in _LIB_PATTERNS:
            matches = root.rglob(pattern) if recurse else root.glob(pattern)
            for path in matches:
                if not path.is_file():
                    continue
                try:
                    key = str(path.resolve())
                except OSError:
                    key = str(path)
                if key in seen:
                    continue
                seen.add(key)
                found.append(path)
    return found


def _set_openblas_threads_on_lib(path: Path, n: int) -> bool:
    # CDLL (cdecl) is correct for OpenBLAS on macOS, Linux, and Windows.
    # SciPy/NumPy have already loaded the library; this attaches by path.
    try:
        lib = ctypes.CDLL(str(path))
    except OSError:
        return False
    setter = getattr(lib, "openblas_set_num_threads", None)
    if setter is None:
        setter = getattr(lib, "goto_set_num_threads", None)
    if setter is None:
        return False
    setter.argtypes = [ctypes.c_int]
    setter(int(n))
    return True


def configure_blas_threads(n: Optional[int] = None) -> int:
    """
    Cap BLAS threads for already-loaded NumPy / SciPy OpenBLAS libraries.

    Safe to call more than once. Honors OPENBLAS_NUM_THREADS / OMP_NUM_THREADS
    if the user set them.
    """
    n = apply_blas_thread_env(n)
    try:
        import numpy  # noqa: F401
        import scipy.linalg  # load SciPy's vendored OpenBLAS
    except ImportError:
        pass

    try:
        from threadpoolctl import threadpool_limits

        threadpool_limits(limits=n)
    except ImportError:
        pass

    for path in _iter_openblas_libs(_package_search_roots()):
        _set_openblas_threads_on_lib(path, n)
    return n
