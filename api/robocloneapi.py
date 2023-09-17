from tkinter import Canvas

class AdvancedRobot:
    def __init__(self):
        self._x: int = 50
        self._y: int = 50
        self._robotHeading: int = 0
        self._gunHeading: int = 0
        self._radarHeading: int = 0

        # Drawing stuff
        self._myID: int = None
        self._images: list = [None, None, None]
        self._partIDS: list[int] = []

        self._lastX = self._x
        self._lastY = self._y
        self._lastRobotHeading = self._robotHeading
        self._lastGunHeading = self._gunHeading
        self._lastRadarHeading = self._radarHeading

        # Amount of degrees to turn
        self._robotHeadingTarget: int = 0
        self._gunHeadingTarget: int = 0
        self._radarHeadingTarget: int = 0

    # Public methods ===========================================================
    def getX(self) -> int: return self._x
    def getY(self) -> int: return self._y
    def getRobotHeading(self) -> int: return self._robotHeading
    def getGunHeading(self) -> int: return self._gunHeading
    def getRadarHeading(self) -> int: return self._radarHeading

    # events
    def run(self) -> None: pass

    # Private-Internal/External methods =================================================
    def getParts(self) -> list[int]: return self._partIDS
    def setParts(self, parts: list[int]) -> None: self._partIDS = parts
    def hasChanged(self) -> bool:
        result = self._lastX != self._x or self._lastY != self._y or self._lastRobotHeading != self._robotHeading or self._lastGunHeading != self._gunHeading or self._lastRadarHeading != self._radarHeading
        if result:
            self._lastX = self._x
            self._lastY = self._y
            self._lastRobotHeading = self._robotHeading
            self._lastGunHeading = self._gunHeading
            self._lastRadarHeading = self._radarHeading
        return result
    
    def unregister(self, canvas: Canvas) -> None:
        for part in self._partIDS:
            canvas.delete(part)