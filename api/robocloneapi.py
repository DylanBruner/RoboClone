from security.classprotection import ProtectedClass

class AdvancedRobot(ProtectedClass):
    _x: int = 0
    _y: int = 0

    def __init__(self):
        self._enable()

    @ProtectedClass.secure()
    def testFunc(self):
        self._x += 1