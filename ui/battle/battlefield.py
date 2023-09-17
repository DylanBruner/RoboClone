from api.robocloneapi import AdvancedRobot
from entities.bullet import Bullet
from helper.justimportit import JustImportIt
try: from ui.battlecreator import RobotPackage, Robot
except ImportError: JustImportIt.resolve(mode=JustImportIt.UNSAFE)

class BattleField:
    _width: int = 800
    _height: int = 600
    _robots: list[AdvancedRobot] = []
    _bullets: list[Bullet] = []

    def __init__(self):
        # JustImportIt.fix()
        # print(RobotPackage('test', [Robot('test', None)]))
        print(RobotPackage)

    def getHeight(self) -> int: return self._height
    def getWidth(self) -> int: return self._width
    def getRobots(self) -> list[AdvancedRobot]: return self._robots

    @classmethod
    def setupNewBattle(self, robots: list['RobotPackage']) -> None:
        print(robots)