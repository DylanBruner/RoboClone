from api.robocloneapi import AdvancedRobot
from security.classprotection import ProtectedClass
from tkinter import Canvas

class RoboHandler:
    def __init__(self, robot: AdvancedRobot):
        self.robot = robot
        self._x = -1
        self._y = -1
        self._robotHeading = -1
        self._gunHeading = -1
        self._radarHeading = -1

        # Drawing stuff
        self._myID = None
        self._images = [None, None, None]
        self._partIDS = []

        # Amount of degrees to turn
        self._robotHeadingTarget = 0
        self._gunHeadingTarget = 0
        self._radarHeadingTarget = 0
        self._robotMoveTarget = 0
        self._movementStopped = False

        # Shooting
        self._firePower = 0
        self._gunHeat = 0

    
    def _getParts(self) -> list[int]: return self._partIDS
    def _setParts(self, parts: list[int]) -> None: self._partIDS = parts
    def _hasChanged(self) -> bool:
        result = self._lastX != self._x or self._lastY != self._y or self._lastRobotHeading != self._robotHeading or self._lastGunHeading != self._gunHeading or self._lastRadarHeading != self._radarHeading
        if result:
            self._lastX = self._x
            self._lastY = self._y
            self._lastRobotHeading = self._robotHeading
            self._lastGunHeading = self._gunHeading
            self._lastRadarHeading = self._radarHeading
        return result
    
    def _unregister(self, canvas: Canvas) -> None:
        for part in self._partIDS:
            canvas.delete(part)