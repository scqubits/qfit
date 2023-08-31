from typing import Callable, Any, Dict, Literal, Union
import pickle

from abc import ABC

QuantityType = Union[Literal["r+"], Literal["r"]]


def READONLY_SETTER(*args, **kwargs):
    raise ValueError("Cannot set value to read-only entry.")


class Registerable(ABC):
    """Mix-in class that makes descendant classes registerable."""

    def registerAll(self) -> Dict[str, "RegistryEntry"]:
        """Register all the quantities in the class. This should be
        implemented by the descendant class.
        """
        raise NotImplementedError


class RegistryEntry:
    """
    Registry entry for a single quantity, storing the name, type, getter,
    and setter.

    Parameters
    ----------
    name : str
        Name of the quantity.
    quantity_type : str
        Type of the quantity. "r+" (read and write) and "r" (read-only)
        are supported. When "r+" is used, a setter must be provided.
        Usually, read-only quantities have their own way of setting and
        can't be simply set by a function.
    getter : Callable[[], Any]
        Getter function for the quantity.
    setter : Union[Callable[[Any], None], None]
        Setter function for the quantity. This is required when "r+" is
        used.

    """

    def __init__(
        self,
        name: str,
        quantity_type: QuantityType,
        getter: Callable[[], Any],
        setter: Union[Callable[[Any], None], None] = None,
    ):
        if quantity_type not in ["r+", "r"]:
            raise ValueError(f"Quantity type {quantity_type} not supported.")
        if quantity_type == "r":
            setter = READONLY_SETTER
        elif setter is None:
            raise ValueError(f"Quantity type {quantity_type} requires a setter.")

        self.name = name
        self.quantity_type = quantity_type
        self.getter = getter
        self.setter = setter

    def __repr__(self):
        return f"RegistryEntry({self.name}, {self.getter()}, {self.quantity_type})"

    def export(self) -> Dict[str, Any]:
        return {self.name: self.getter()}

    def _processValue(self, value):
        """
        Based on the type of the entry, process the value.
        Currently, we do no processing.
        """
        return value

    def load(self, value):
        """Load the entry from existed entry. They should have the same
        and the same type.
        """
        self.setter(self._processValue(value))


class Registry:
    _registry: Dict[str, RegistryEntry] = {}

    def __init__(self):
        pass

    def register(
        self,
        obj: Any,
    ):
        """Register the object to the registry."""
        try:
            reg_dict = obj.registerAll()
            self._registry.update(reg_dict)
        except AttributeError:
            name = obj.__class__.__name__
            entry = RegistryEntry(
                name,
                "r",
                lambda: obj,
            )
            self._registry[name] = entry

    def export(self) -> Dict[str, Any]:
        full_dict: Dict[str, Any] = {}
        for entry in self._registry.values():
            full_dict.update(entry.export())

        return full_dict

    def exportPkl(self, filename: str) -> None:
        try:
            with open(filename, "wb") as f:
                pickle.dump(self.export(), f)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found. Cannot export data.")

    def loadPkl(self, filename: str) -> None:
        """
        Skip the entries that are
        - neither in the file nor in the current registry
        - read-only
        """
        try:
            with open(filename, "rb") as f:
                data: Dict[str, Any] = pickle.load(f)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found. Cannot load data.")
            return

        for name, value in data.items():
            try:
                if self._registry[name].quantity_type == "r":
                    continue
                self._registry[name].load(value)
            except KeyError:
                print(f"Key {name} not found in registry. Skipping.")
                continue
