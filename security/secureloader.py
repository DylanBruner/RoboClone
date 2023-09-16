import importlib.machinery
from api.robocloneapi import AdvancedRobot

class SecureLoader:
    """
    Patch a child class to call the parent class' __init__ method before its own.
    It also makes sure the the parent class' __init__ method is called even if the child 
    class doesn't call it.
    """
    @staticmethod
    def patch_init(child_class):
        parent_class = child_class.__bases__[0]
        child_init = child_class.__init__ if "__init__" in child_class.__dict__ else None

        def new_init(self, *args, **kwargs):
            parent_class.__init__(self, *args, **kwargs)

            if child_init:
                child_init(self, *args, **kwargs)

        child_class.__init__ = new_init
        return child_class
    
    @staticmethod
    def loadRobot(filename: str) -> object:
        loader = importlib.machinery.SourceFileLoader("robot", filename)
        module = loader.load_module()

        # Find the robot class
        robotClass = None
        for name, obj in module.__dict__.items():
            if isinstance(obj, type) and issubclass(obj, AdvancedRobot):
                robotClass = obj
                # print("Found robot class: " + name)
                break
        
        if robotClass:
            robotClass = SecureLoader.patch_init(robotClass)
            robot_instance = robotClass()
            return robot_instance
        else:
            print("Robot class not found in the loaded module.")
            return None
