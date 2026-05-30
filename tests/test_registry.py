"""Tests for qfit.models.registry."""
import pytest

from qfit.models.registry import READONLY_SETTER, Registry, RegistryEntry


pytestmark = pytest.mark.unit


class TestRegistryEntry:
    def test_read_write_round_trip(self):
        store = {"v": 0}
        entry = RegistryEntry(
            "test.value",
            "r+",
            getter=lambda: store["v"],
            setter=lambda x: store.update(v=x),
        )
        entry.load(42)
        assert entry.getter() == 42
        assert entry.export() == {"test.value": 42}

    def test_readonly_rejects_set(self):
        entry = RegistryEntry("ro", "r", getter=lambda: 1)
        with pytest.raises(ValueError, match="read-only"):
            entry.load(2)

    def test_r_plus_requires_setter(self):
        with pytest.raises(ValueError, match="requires a setter"):
            RegistryEntry("x", "r+", getter=lambda: 1)

    def test_invalid_quantity_type(self):
        with pytest.raises(ValueError, match="not supported"):
            RegistryEntry("x", "w", getter=lambda: 1, setter=lambda v: None)


class TestRegistry:
    def test_export_includes_version(self):
        reg = Registry()
        exported = reg.exportDict()
        assert "version" in exported

    def test_register_plain_object(self):
        reg = Registry()

        class Dummy:
            pass

        obj = Dummy()
        reg.register(obj)
        assert "Dummy" in reg.keys()

    def test_clear_keeps_version(self):
        reg = Registry()
        reg.clear()
        assert "version" in reg.keys()
