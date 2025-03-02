from typing import Callable, Any, Dict, Literal, Union
import dill
from qfit.version import version
from abc import ABC

QuantityType = Union[Literal["r+"], Literal["r"]]


def READONLY_SETTER(*args, **kwargs):
    raise ValueError("Cannot set value to a read-only entry.")


class Registrable(ABC):
    """
    Mix-in class that makes descendant classes registerable.

    The descendant class should implement the registerAll() method, which
    returns a dictionary of RegistryEntry objects.
    """

    def _toRegistryEntry(self, attribute: str = "value") -> "RegistryEntry":
        """
        Convert an attribute to a RegistryEntry object. The name of the
        RegistryEntry object is not complete, and should be updated later.

        Parameters
        ----------
        attribute : str
            Name of the attribute to be registered.

        Returns
        -------
        RegistryEntry
            The RegistryEntry object.
        """
        name = self.__class__.__name__ + "." + attribute

        def setter_func(value):
            setattr(self, attribute, value)

        return RegistryEntry(
            name=name,
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
    Registry entry is connected to a single quantity/object in the application.
    It stores the name, type, getter and setter for the quantity, and provides
    methods to store and load the quantity.

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
        """
        Grab the value of the entry and export it as a dictionary.

        Returns
        -------
        Dict[str, Any]
            A length-one dictionary containing the name and value of the entry.
        """
        return {self.name: self.getter()}

    def load(self, value):
        """Load the entry from existed entry. They should have the same
        and the same type.
        """
        self.setter(value)


version_entry = RegistryEntry(
    "version",
    "r",
    lambda version=version: version,
)


class Registry:
    """
    The Registry is a singleton object. It is "connected" the global
    quantities and objects in the application. It can grab the current
    state & data of the application and export them to a dictionary or a file.
    And in the same way, it can load the state & data from a dictionary or a
    file.

    It is a collection of RegistryEntry objects and provides methods to
    register, export, and load the entries.
    """

    def __init__(self):
        self._registry: Dict[str, RegistryEntry] = {
            "version": version_entry,
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

        Parameters
        ----------
        obj : Any
            The object to be registered.
        """
        if isinstance(obj, Registrable):
            reg_dict = obj.registerAll()
            self._registry.update(reg_dict)
        else:
            name = obj.__class__.__name__
            obj_wrap = [obj]  # list wrapper to make the object mutable
            entry = RegistryEntry(
                name,
                "r",
                lambda: obj_wrap[0],
            )
            self._registry[name] = entry

    def exportDict(self) -> Dict[str, Any]:
        """
        Grab the current state & data of the application and export them as a
        dictionary.

        Returns
        -------
        Dict[str, Any]
            A dictionary of the current state & data of the application.
        """
        full_dict: Dict[str, Any] = {}
        for entry in self._registry.values():
            full_dict.update(entry.export())

        return full_dict

    def exportPkl(self, filename: str) -> None:
        """
        Export the current state & data of the application to a file.

        Parameters
        ----------
        filename : str
            Name of the file to be exported.
        """
        try:
            with open(filename, "wb") as f:
                dill.dump(self.exportDict(), f)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found. Cannot export data.")

    @staticmethod
    def dictFromFile(filename: str) -> Union[Dict[str, Any], None]:
        """
        Load the state & data of the application from a file.

        Parameters
        ----------
        filename : str
            Name of the file to be loaded.
        """
        try:
            with open(filename, "rb") as f:
                return dill.load(f)
        except FileNotFoundError:
            return None  # indicate that the file is not found

    def setByDict(self, registryDict: Dict[str, Any]):
        """
        Load the state & data of the application from a dictionary.

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
        for name in set(registryDict.keys()).union(self._registry.keys()):
            # we don't need to set read-only entries
            if self._registry[name].quantity_type == "r":
                continue

            try:
                value = registryDict[name]
            except KeyError:
                print(
                    f"Key {name} not found in file. "
                    "We apologize that it's usually due to the version mismatch. "
                    "Please contact the developer for retrieving the data."
                )
                continue

            try:
                self._registry[name].load(value)
            except KeyError:
                print(
                    f"Key {name} not found in the current app. "
                    "We apologize that it's usually due to the version mismatch. "
                    "Please contact the developer for retrieving the data."
                )
                continue

    def clear(self):
        """Clear the registry."""
        self._registry.clear()
        self._registry.update({"version": version_entry})
