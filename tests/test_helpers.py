"""Tests for qfit.utils.helpers."""
import numpy as np
import pytest

from qfit.utils.helpers import (
    DictItem,
    OrderedDictMod,
    isValid1dArray,
    isValid2dArray,
    makeUnique,
    remove_nones,
    transposeEach,
    ySnap,
    _find_lorentzian_peak,
)


pytestmark = pytest.mark.unit


class TestArrayValidation:
    def test_isValid1dArray_monotonic_increasing(self):
        assert isValid1dArray(np.array([1.0, 2.0, 3.0]))

    def test_isValid1dArray_non_monotonic(self):
        assert not isValid1dArray(np.array([1.0, 3.0, 2.0]))

    def test_isValid1dArray_skip_monotonic(self):
        assert isValid1dArray(np.array([3.0, 1.0, 2.0]), checkMonotonic=False)

    def test_isValid1dArray_2d_row(self):
        assert isValid1dArray(np.array([[1.0, 2.0, 3.0]]))

    def test_isValid2dArray_valid(self):
        assert isValid2dArray(np.ones((3, 4)))

    def test_isValid2dArray_vector_rejected(self):
        assert not isValid2dArray(np.array([1.0, 2.0, 3.0]))

    def test_isValid2dArray_integer_rejected(self):
        assert not isValid2dArray(np.ones((3, 4), dtype=int))


class TestMakeUnique:
    def test_makeUnique_no_duplicates(self):
        assert makeUnique(["a", "b", "c"]) == ["a", "b", "c"]

    def test_makeUnique_with_duplicates(self):
        assert makeUnique(["a", "b", "a"]) == ["a", "b", "a (1)"]


class TestTransposeEach:
    def test_transposeEach(self):
        a = np.array([[1, 2], [3, 4]])
        result = transposeEach([a])
        assert np.array_equal(result[0], a.T)


class TestRemoveNones:
    def test_remove_nones(self):
        assert remove_nones({"a": 1, "b": None}) == {"a": 1}


class TestOrderedDictMod:
    def test_equality_with_numpy(self):
        d1 = OrderedDictMod({"x": np.array([1.0, 2.0])})
        d2 = OrderedDictMod({"x": np.array([1.0, 2.0])})
        assert d1 == d2

    def test_dict_item_equality(self):
        assert DictItem("k", 1.0) == DictItem("k", 1.0)
        assert not (DictItem("k", 1.0) == DictItem("k", 2.0))


class TestPeakFinding:
    def test_find_lorentzian_peak_at_center(self):
        data = 1.0 / (1.0 + (np.arange(50) - 25.0) ** 2)
        peak = _find_lorentzian_peak(data)
        assert abs(peak - 25) <= 2

    def test_ySnap_lorentzian(self):
        x = np.linspace(0, 1, 50)
        y = np.linspace(4.0, 5.0, 40)
        z = np.zeros((len(y), len(x)))
        mid = len(y) // 2
        z[mid, :] = 1.0
        snapped = ySnap(x, y, z, (0.5, y[mid]), half_y_range=0.2)
        assert y.min() <= snapped <= y.max()
