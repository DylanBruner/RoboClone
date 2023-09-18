
import inspect
from typing import Any

"""
Adding security to this class would theoretically only limit access via outside classes (i think... maybe... idk)
"""
class ProtectedClassMeta(type):
    def __delattr__(self, __name: str) -> None:
        return super().__delattr__(__name)

    def __getattribute__(self, __name: str) -> Any:
        return super().__getattribute__(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setattr__(__name, __value)

class ProtectedClass(object, metaclass=ProtectedClassMeta):
    def __init__(self):
        self.p_attribute_data = {
            "enabled": False,
            "security_overrides": [],
            "attributes": {
                "_enableSecurity": {
                    "read": True,    # Allows the function to be read aka called
                    "write": False,  # Prevents the function from being overwritten
                    "delete": False, # Prevents the function from being deleted
                    "override": True # Gives the function permission to bypass security
                },
                "p_attribute_data": {
                    "read": False,
                    "write": False,
                    "delete": False,
                }
            }
        }

    # Secure access stuffs ========================================================
    def _enableSecurity(self) -> None:
        self.p_attribute_data["enabled"] = True
    
    """
    Add a security override to the class
    """
    def _addSecurityOverride(self, func: str) -> None:
        if self.p_attribute_data["enabled"]: raise RuntimeError("Cannot add security override after security is enabled")
        if (attribute := self.p_attribute_data["attributes"].get(func, None)) is not None:
            attribute["override"] = True
        else:
            self.p_attribute_data["attributes"][func] = {
                "read": True,
                "write": True,
                "delete": True,
                "override": True
            }
    
    """
    Modify the permissions of an attribute
    """
    def _setPermission(self, _attribute: str, data: dict) -> None:
        # if we aren't enabled or the caller is in the bypass list, allow it
        func_name = inspect.currentframe().f_back.f_code.co_name
        if ((attribute := self.p_attribute_data["attributes"].get(func_name, None)) is not None and attribute.get("override", False)) or not self.p_attribute_data["enabled"]:
            if self.p_attribute_data["attributes"].get(_attribute, None) is None:
                self.p_attribute_data["attributes"][attribute] = data
            else:
                self.p_attribute_data["attributes"][_attribute].update(data)
        else: raise PermissionError(f"Cannot set permission for attribute {_attribute} on class {self.__class__.__name__} (class)")
    
    def _setPermissions(self, _attributes: list[str], data: dict) -> None:
        func_name = inspect.currentframe().f_back.f_code.co_name
        if ((attribute := self.p_attribute_data["attributes"].get(func_name, None)) is not None and attribute.get("override", False)) or not self.p_attribute_data["enabled"]:
            for attribute in _attributes:
                if self.p_attribute_data["attributes"].get(_attributes, None) is None:
                    self.p_attribute_data["attributes"][_attributes] = data
                else:
                    self.p_attribute_data["attributes"][_attributes].update(data)
        else: raise PermissionError(f"Cannot set permissions for attributes {_attributes} on class {self.__class__.__name__} (class)")

    """
    Automatically set permissions for all attributes within a class
    """
    def _mapCurrent(self, permission_tree: 'PermissionTree') -> None:
        func_name = inspect.currentframe().f_back.f_code.co_name
        if ((attribute := self.p_attribute_data["attributes"].get(func_name, None)) is not None and attribute.get("override", False)) or not self.p_attribute_data["enabled"]:
            
            for thing in dir(self):
                if thing.startswith('_'): continue # ignore the builtins, anything nammed with _ by the user will need to be manually set
                if (attribute := self.p_attribute_data["attributes"].get(thing, None)) is not None: continue # ignore anything that's already been set
                thing_name = str(thing)
                thing = getattr(self, thing)

                for _type, permission in permission_tree._tree.items():
                    try:
                        if _type(thing):
                            self.p_attribute_data["attributes"][thing_name] = permission
                            break
                    except Exception as e:
                        print("Error while applying filter to attribute", thing_name, ":", e)

        else: 
            raise PermissionError(f"Cannot map current permissions on class {self.__class__.__name__} (class)")

    # Variable protection internals ===============================================
    def __getattribute__(self, __name: str) -> Any:
        if inspect.currentframe().f_back.f_code.co_filename == __file__: return super().__getattribute__(__name)
        # external access                                                                               - bandaid fix for the fact that the class is recompiled causing it's src to change
        if inspect.getfile(self.__class__) != (file := inspect.currentframe().f_back.f_code.co_filename) and not 'data/robots' in file:
            return super().__getattribute__(__name)

        allowed = False

        if (attribute := self.p_attribute_data["attributes"].get(__name, None)) is not None:
            allowed = attribute["read"]
        
        # get the function that attempted to get the attribute
        func_name = inspect.currentframe().f_back.f_code.co_name
        if func_name == '<module>': raise PermissionError(f"Cannot get attribute {__name} on class {self.__class__.__name__} from outside a class")
        if (attribute := self.p_attribute_data["attributes"].get(func_name, None)) is not None:
            allowed = attribute.get("override", False) or allowed # if it's allowed via r/w/d flags, or if it's allowed via override, allow it
        
        if allowed or not self.p_attribute_data["enabled"]:
            return super().__getattribute__(__name)
        raise PermissionError(f"Cannot get attribute {__name} on class {self.__class__.__name__} (class)")

    def __setattr__(self, __name: str, __value: Any) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__: return super().__setattr__(__name, __value)
        # get the callers file
        if inspect.getfile(self.__class__) != inspect.currentframe().f_back.f_code.co_filename:
            return super().__setattr__(__name, __value)

        allowed = False

        if (attribute := self.p_attribute_data["attributes"].get(__name, None)) is not None:
            allowed = attribute["write"]
        
        # get the function that attempted to set the attribute
        func_name = inspect.currentframe().f_back.f_code.co_name
        if func_name == '<module>': raise PermissionError(f"Cannot set attribute {__name} on class {self.__class__.__name__} from outside a class")
        if (attribute := self.p_attribute_data["attributes"].get(func_name, None)) is not None:
            allowed = attribute.get("override", False) or allowed
        
        if allowed or not self.p_attribute_data["enabled"]:
            return super().__setattr__(__name, __value)
        raise PermissionError(f"Cannot set attribute {__name} on class {self.__class__.__name__} (class)")
    
    def __delattr__(self, __name: str) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__: return super().__delattr__(__name)
        # get the callers file
        if inspect.getfile(self.__class__) != inspect.currentframe().f_back.f_code.co_filename:
            return super().__delattr__(__name)
        
        allowed = False

        if (attribute := self.p_attribute_data["attributes"].get(__name, None)) is not None:
            allowed = attribute["delete"]

        # get the function that attempted to delete the attribute
        func_name = inspect.currentframe().f_back.f_code.co_name
        if func_name == '<module>': raise PermissionError(f"Cannot delete attribute {__name} on class {self.__class__.__name__} from outside a class")
        if (attribute := self.p_attribute_data["attributes"].get(func_name, None)) is not None:
            allowed = attribute.get("override", False) or allowed

        if allowed or not self.p_attribute_data["enabled"]:
            return super().__delattr__(__name)
        raise PermissionError(f"Cannot delete attribute {__name} on class {self.__class__.__name__} (class)")
    

class PermissionTree:
    def __init__(self):
        self._tree: dict[callable, dict[str, bool]] = {}
    
    """
    Returns self to allow for chaining
    """
    def setPermissionForType(self, filter: callable, permission: dict[str, bool]) -> 'PermissionTree':
        self._tree[filter] = permission
        return self