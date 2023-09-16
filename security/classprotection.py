import inspect
from typing import Any

class ProtectedClass:
    def __getattribute__(self, __name: str) -> Any:
        if __name.startswith("_"):
            raise AttributeError(f"Access to {__name} denied")
        return super().__getattribute__(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name.startswith("_"):
            raise AttributeError(f"Access to {__name} denied")
        return super().__setattr__(__name, __value)

    def __delattr__(self, __name: str) -> None:
        if __name.startswith("_"):
            raise AttributeError(f"Access to {__name} denied")
        return super().__delattr__(__name)