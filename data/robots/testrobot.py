import api.robocloneapi as robocloneapi

class robot(robocloneapi.AdvancedRobot):
    def __init__(self):
        print(self._x, self._y)