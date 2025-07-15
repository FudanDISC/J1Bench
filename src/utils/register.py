import os
import sys

project_root = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
print(project_root)
if project_root not in sys.path:
    sys.path.append(project_root)


class Registry:
    def __init__(self):
        self._registry = {}
    
    def register(self, alias, class_reference):
        self._registry[alias] = class_reference
        
    def get_class(self, alis):
        return self._registry.get(alis)
    

registry = Registry()
def register_class(alias=None):
    def decorator(cls):
        nonlocal alias
        if alias is None:
            alias = cls.__name__
        registry.register(alias, cls)
        return cls
    return decorator
