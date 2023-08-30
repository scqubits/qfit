
from typing import Callable, Any, Dict

class RegistryEntry:
    def __init__(
        self, 
        name: str,
        value: Any,
        quantity_type: str,
        setter: Callable[[Any], None],
        getter: Callable[[], Any],
    ):
        self.name = name
        self.value = value
        self.quantity_type = quantity_type
        self.setter = setter
        self.getter = getter

    def _refresh(self):
        self.value = self.getter()

    def export(self) -> Dict[str, Any]:
        self._refresh()
        return {self.name: self.value}
    
    def _processValue(self, value):
        """
        Based on the type of the entry, process the value.
        Currently, we do no processing.
        """
        return value

    def _load(self, name, value, quantity_type):
        if self.name != name:
            raise ValueError("The name of the entry should be the same.")
        if self.quantity_type != quantity_type:
            raise ValueError("The type of the entry should be the same.")
        
        self.value = value
        self.setter(self.value)
    
    def loadByEntry(self, existed_entry: "RegistedEntry"):
        """Load the entry from existed entry. They should have the same 
        and the same type.
        """
        self._load(
            existed_entry.name,
            self._processValue(existed_entry.value),
            existed_entry.quantity_type,
        )

    def loadByAttribute(self, value, quantity_type):
        """Load the entry from existed entry. They should have the same 
        and the same type.
        """
        self._load(
            self.name,
            self._processValue(value),
            quantity_type,
        )

        
class Registry:
    _registry: Dict[str, RegistryEntry] = {}
    def __init__(self):
        pass

    def register(
        self,
        item: RegistryEntry
    ):
        self._registry[item.name] = item
    
    def export(self) -> Dict[str, Any]:
        full_dict = {}
        for entry in self._registry.values():
            full_dict.update(entry.export())
        
        return full_dict
    
    def exportPkl(self,):
        pass
    
