from api.robocloneapi import AdvancedRobot
from entities.bullet import Bullet

class BattleField:
    def __init__(self):

        self.width  = 800
        self.height = 600

        self._robots: list[AdvancedRobot] = [
            AdvancedRobot(),
            AdvancedRobot()
        ]
        self._bullets: list[Bullet] = []

        self._robots[1]._x = 90
        self._robots[1]._y = 90
        
    def getHeight(self) -> int: return self.height
    def getWidth(self) -> int: return self.width
    def getRobots(self) -> list[AdvancedRobot]: return self._robots