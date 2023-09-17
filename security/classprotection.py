import inspect, traceback
from typing import Any

"""
TODO: Fix these issues:
 - re-write this whole class with what i now know
"""

import inspect, hashlib
from typing import Any

"""
Some notes
 - You must be inside a class to access protected methods of another class or the same class
 - Variable access
  - if the variable is prefixed with "l_" it may only be accessed by the class it is defined in,
    - This may not be bypassed via ProtectedClass.l_bypassClasses
"""

class SecurityManagerMeta(type):
    def __setattr__(self, __name: str, __value: Any) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__:
            return super().__setattr__(__name, __value)
        raise AttributeError(f"Cannot set attribute {__name} on class {self.__name__}")
    
    def __delattr__(self, __name: str) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__:
            return super().__delattr__(__name)
        raise AttributeError(f"Cannot delete attribute {__name} on class {self.__name__}")
    
    def __getattribute__(self, __name: str) -> Any:
        if inspect.currentframe().f_back.f_code.co_filename == __file__:
            return super().__getattribute__(__name)
        if __name.startswith('_'): raise AttributeError(f"Cannot access attribute {__name} on class {self.__name__}")
        return super().__getattribute__(__name)
    
class SecurityManager(object, metaclass=SecurityManagerMeta):
    _bypassClasses: list[type] = [] # Classes that can bypass the security manager
    _enabled: bool = False # Whether or not the security manager is enabled

    @classmethod
    def enable(cls) -> None:
        cls._enabled = True
    
    @classmethod
    def isEnabled(cls) -> bool:
        return cls._enabled
    
    @classmethod
    def addBypass(cls, bypass: type) -> None:
        if cls._enabled: raise RuntimeError("Cannot add bypass class after security manager is enabled")
        cls._bypassClasses.append(bypass)

class ProtectedClassMeta(type):
    def __setattr__(cls, __name: str, __value: Any) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__: # prevent recursion
            return super().__setattr__(__name, __value)
        
        if __name.startswith('_'):
            caller_class = None
            frame = inspect.currentframe()
            while frame:
                # Check if 'self' exists in the local variables of the frame
                if 'self' in frame.f_locals:
                    caller_class = frame.f_locals['self'].__class__
                    break
                frame = frame.f_back  # Move to the previous frame
            
            if caller_class not in SecurityManager._bypassClasses and caller_class != cls:
                raise AttributeError(f"Cannot set protected variable {__name} on class {cls.__name__}")
        return super().__setattr__(__name, __value)

    def __delattr__(cls, __name: str) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__: # prevent recursion
            return super().__delattr__(__name)
        
        if __name.startswith('_'):
            caller_class = None
            frame = inspect.currentframe()
            while frame:
                # Check if 'self' exists in the local variables of the frame
                if 'self' in frame.f_locals:
                    caller_class = frame.f_locals['self'].__class__
                    break
                frame = frame.f_back
            if caller_class not in SecurityManager._bypassClasses and caller_class != cls:
                raise AttributeError(f"Cannot delete protected variable {__name} on class {cls.__name__}")
        return super().__delattr__(__name)
    
    def __getattribute__(cls, __name: str) -> Any:
        if inspect.currentframe().f_back.f_code.co_filename == __file__: # prevent recursion
            return super().__getattribute__(__name)
        
        if __name.startswith('_'):
            caller_class = None
            frame = inspect.currentframe()
            while frame:
                # Check if 'self' exists in the local variables of the frame
                if 'self' in frame.f_locals:
                    caller_class = frame.f_locals['self'].__class__
                    break
                frame = frame.f_back
            if caller_class not in SecurityManager._bypassClasses and caller_class != cls:
                raise AttributeError(f"Cannot access protected variable {__name} on class {cls.__name__}")
        return super().__getattribute__(__name)


class ProtectedClass(object, metaclass=ProtectedClassMeta):
    _readOnlyVariables: dict[str, list[str]] = {} # {class: [variables]}

    def __init__(self):
        ...

    # function decorator that makes it read only
    @classmethod
    def readOnly(self, func: Any) -> Any:
        # get the class the function is in
        class_name = func.__qualname__.split(".")[0]
        func_name  = func.__qualname__.split(".")[1]

        self._readOnlyVariables.setdefault(class_name, []).append(func_name)
        return func


    # Instance variable protection =================================================
    def __getattribute__(self, __name: str) -> Any:
        if inspect.currentframe().f_back.f_code.co_filename == __file__ or not SecurityManager.isEnabled():
            return super().__getattribute__(__name)
        if __name.startswith('l_'): raise AttributeError(f"Cannot access local variable {__name}")

        if __name.startswith('_'):
            caller_class = getattr(inspect.currentframe().f_back.f_locals.get("self", None), "__class__", None)
            if caller_class not in SecurityManager._bypassClasses and caller_class != self.__class__:
                raise AttributeError(f"Cannot access protected method {__name}")

        return super().__getattribute__(__name)
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__ or not SecurityManager.isEnabled():
            return super().__setattr__(__name, __value)
        if __name.startswith('l_'): raise AttributeError(f"Cannot set local variable {__name}")

        # check if the variable is read only
        if __name in self._readOnlyVariables.get(self.__class__.__name__, []): raise AttributeError(f"Cannot set read-only variable {__name}")

        if __name.startswith('_'):
            caller_class = getattr(inspect.currentframe().f_back.f_locals.get("self", None), "__class__", None)
            if caller_class not in SecurityManager._bypassClasses and caller_class != self.__class__:
                raise AttributeError(f"Cannot set protected method {__name}")
        
        return super().__setattr__(__name, __value)
    
    def __delattr__(self, __name: str) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__ or not SecurityManager.isEnabled():
            return super().__delattr__(__name)
        if __name.startswith('l_'): raise AttributeError(f"Cannot delete local variable {__name}")
        if __name in self._readOnlyVariables: raise AttributeError(f"Cannot delete read-only variable {__name}")

        # check if the variable is read only
        if __name in self._readOnlyVariables.get(self.__class__.__name__, []): raise AttributeError(f"Cannot delete read-only variable {__name}")

        if __name.startswith('_'):
            caller_class = getattr(inspect.currentframe().f_back.f_locals.get("self", None), "__class__", None)
            if caller_class not in SecurityManager._bypassClasses and caller_class != self.__class__:
                raise AttributeError(f"Cannot delete protected method {__name}")
        
        return super().__delattr__(__name) # Fails when trying to delete a class variable