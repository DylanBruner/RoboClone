import inspect, hashlib
from typing import Any

"""
TODO: Fix these issues:
 - re-write this whole class with what i now know
"""

class ProtectedClass:
    _protected: dict[object] = {}
    _hidden: dict[object] = {}
    _rw_permission: list[type] = [] # can add classes to this list to allow them to read/write/delete protected and hidden variables
    _secondaryAccessor: type = None

    """
    Functions must be decorated with @ProtectedClass.secure() to be protected.
    They also must be wrapped in order to modify any private variables.
    """
    @classmethod
    def secure(self, read: bool = True, write: bool = True, delete: bool = True, protected: bool = True):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self._protected[ProtectedClass._getFunctionHash(func)] = {"read": read, "write": write, "delete": delete, "protected": protected,
                                                                      "wrapper_hash": ProtectedClass._getFunctionHash(wrapper)}
            return wrapper
        return decorator
    
    @classmethod
    def hidden(self, func: object):
        self._hidden[ProtectedClass._getFunctionHash(func)] = True
        print(self._hidden)
        return func
    
    # Internal functions ======================================================
    def _hasPermission(self, frame: inspect.FrameInfo, permissions: list[str]) -> bool:
        caller_frame = frame.f_back
        if 'self' in caller_frame.f_locals:
            caller_hash = ProtectedClass._getFunctionHash(caller_frame)
            if caller_hash in self._protected:
                return any([self._protected[caller_hash][permission] for permission in permissions])
        return False
            
    @staticmethod
    def _getFunctionHash(func: callable or inspect.FrameInfo) -> str:
        if isinstance(func, inspect.FrameInfo):
            func = func.f_code
        return hashlib.sha256(inspect.getsource(func).encode()).hexdigest()
    
    def __getattribute__(self, __name: str) -> Any:
        if inspect.currentframe().f_back.f_code.co_filename == __file__:
            # This is a call from within this class, prevent recursion
            return super().__getattribute__(__name)

        if __name.startswith("_") and not self._hasPermission(inspect.currentframe(), ["read"]):
            raise AttributeError(f"Access to {__name} denied")
        
        # check if it's a function
        if (val := getattr(self, __name, None)) is not None and callable(val):
            func_hash = ProtectedClass._getFunctionHash(val)
            if func_hash in self._hidden:
                raise AttributeError(f"Cannot read a hidden function {__name}")
            
        return super().__getattribute__(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__:
            # This is a call from within this class, prevent recursion
            return super().__setattr__(__name, __value)
        
        if __name.startswith("_") and not self._hasPermission(inspect.currentframe(), ["write"]):
            raise AttributeError(f"Access to {__name} denied")

        # check if the __name variable exists, also check if it's a function
        if (val := getattr(self, __name, None)) is not None and callable(val):
            # if it's a protected variable raise an error
            func_hash = ProtectedClass._getFunctionHash(val)
            for key in self._protected:
                if self._protected[key]["wrapper_hash"] == func_hash:
                    func_hash = key
                    break

            if func_hash in self._protected and self._protected[func_hash]["protected"]:
                raise AttributeError(f"Cannot modify the value of a protected function {__name}")
            
            # check if it's hidden
            if func_hash in self._hidden:
                raise AttributeError(f"Cannot modify a hidden function {__name}")
            
        return super().__setattr__(__name, __value)

    def __delattr__(self, __name: str) -> None:
        if inspect.currentframe().f_back.f_code.co_filename == __file__:
            # This is a call from within this class, prevent recursion
            return super().__delattr__(__name)
        
        if __name.startswith("_") and not self._hasPermission(inspect.currentframe(), ["delete"]):
            raise AttributeError(f"Access to {__name} denied")
        
        # check if the __name variable exists, also check if it's a function
        if (val := getattr(self, __name, None)) is not None and callable(val):
            # if it's a protected variable raise an error
            func_hash = ProtectedClass._getFunctionHash(val)
            for key in self._protected:
                if self._protected[key]["wrapper_hash"] == func_hash:
                    func_hash = key
                    break

            if func_hash in self._protected and self._protected[func_hash]["protected"]:
                raise AttributeError(f"Cannot modify the value of a protected function {__name}")
            
            # check if it's hidden
            if func_hash in self._hidden:
                raise AttributeError(f"Cannot delete a hidden function {__name}")
            
        return super().__delattr__(__name)