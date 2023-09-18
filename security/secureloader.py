import importlib.machinery
from api.robocloneapi import AdvancedRobot

class SecureLoader:
    """
    Patch a child class to call the parent class' __init__ method before its own.
    It also makes sure the the parent class' __init__ method is called even if the child 
    class doesn't call it.

    Currently doesn't work with the security manager.
    """
    def patch_init(self, child_class):
        parent_class = child_class.__bases__[0]
        child_init = child_class.__init__ if "__init__" in child_class.__dict__ else None

        def new_init(self, *args, **kwargs):
            parent_class.__init__(self, *args, **kwargs)

            if child_init:
                child_init(self, *args, **kwargs)

        child_class.__init__ = new_init
        return child_class
    
    def loadRobot(self, filename: str) -> object:
        loader = importlib.machinery.SourceFileLoader("robot", filename)
        module = loader.load_module()

        robotClass = (EXPORT := getattr(module, "EXPORT", None)) and EXPORT[0] or None
        
        if robotClass:
            # robotClass = type(robotClass.__name__, (robotClass,), {})
            # patch the class to use the parent class' __init__ method
            robotClass = type(robotClass.__name__, (robotClass,), {
                '__init__': AdvancedRobot.__init__,
                '_init__': robotClass.__init__
            })
            robot_instance = robotClass()
            return robot_instance
        else:
            print("Robot class not found in the loaded module.")
            return None
