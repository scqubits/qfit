from typing import Callable, Any, Dict, Literal, Union
import pickle
from qfit.version import version

from abc import ABC

QuantityType = Union[Literal["r+"], Literal["r"]]


def READONLY_SETTER(*args, **kwargs):
    raise ValueError("Cannot set value to read-only entry.")


class Registrable(ABC):
    """Mix-in class that makes descendant classes registerable."""

    def _toRegistryEntry(self, attribute: str = "value") -> "RegistryEntry":
        """
        Convert an attribute to a RegistryEntry object. The name of the
        RegistryEntry object is not complete, and should be updated later.
        """

        def setter_func(value):
            setattr(self, attribute, value)

        return RegistryEntry(
            name=attribute,
            quantity_type="r+",
            getter=lambda: getattr(self, attribute),
            setter=setter_func,
        )

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
    _registry: Dict[str, RegistryEntry] = {
        "version": RegistryEntry(
            "version",
            "r",
            lambda: version,
        ),
    }

    def __getitem__(self, key: str) -> Any:
        return self._registry[key].getter()
    
    def keys(self):
        return self._registry.keys()
    
    def values(self):
        return self._registry.values()
    
    def items(self):
        return self._registry.items()

    def register(
        self,
        obj: Any,
    ):
        """
        Register the object to the registry.
        
        There are two ways to register an object:
        1. The object is a Registrable object. In this case, the
        registerAll() method will be called.
        2. The object is not a Registrable object. In this case, the object
        will be directly saved and this entry will be read-only.
        """
        try:
            reg_dict = obj.registerAll()
            self._registry.update(reg_dict)
        except AttributeError:
            name = obj.__class__.__name__
            obj_wrap = [obj]    # list wrapper to make the object mutable
            entry = RegistryEntry(
                name,
                "r",
                lambda: obj_wrap[0],
            )
            self._registry[name] = entry

    def exportDict(self) -> Dict[str, Any]:
        full_dict: Dict[str, Any] = {}
        for entry in self._registry.values():
            full_dict.update(entry.export())

        return full_dict

    def exportPkl(self, filename: str) -> None:
        try:
            with open(filename, "wb") as f:
                pickle.dump(self.exportDict(), f)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found. Cannot export data.")

    @staticmethod
    def fromFile(filename: str) -> Union[Dict[str, Any], None]:
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None  # indicate that the file is not found

    def setByDict(self, registryDict: Dict[str, Any]):
        """
        Skip the entries that are
        - neither in the file nor in the current registry
        - read-only

        Parameters
        ----------
        filename : str
            Name of the file to be loaded.

        Returns
        -------
        Dict[str, Any]
            A dictionary of the loaded data.
        """
        for name, value in registryDict.items():
            try:
                if self._registry[name].quantity_type == "r":
                    continue
                self._registry[name].load(value)
            except KeyError:
                print(f"Key {name} not found in registry. Skipping. "
                      "We apologize that it's usually due to the version mismatch. "
                      "Please contact the developer for retrieving the data.")
                continue

    def clear(self):
        self._registry.clear()
