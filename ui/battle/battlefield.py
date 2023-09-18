import random, threading
from api.robocloneapi import AdvancedRobot
from entities.bullet import Bullet
from helper.justimportit import JustImportIt
from security.secureloader import SecureLoader
try: from ui.battlecreator import RobotPackage, Robot
except ImportError: JustImportIt.resolve(mode=JustImportIt.UNSAFE)

class BattleField:
    _width: int = 800
    _height: int = 600
    _robots: list[AdvancedRobot] = []
    _bullets: list[Bullet] = []
    _base_robots: list[Robot] = []
    _state = 0

    CANVAS = None

    def __init__(self):
        ...

    def getHeight(self) -> int: return self._height
    def getWidth(self) -> int: return self._width
    def getRobots(self) -> list[AdvancedRobot]: return self._robots
    def getState(self) -> int: return self._state

    @classmethod
    def setupNewBattle(self, robots: list[Robot]) -> None:
        self._base_robots = robots
        self._state = 1
        for robot in robots:
            self._robots.append((robot := SecureLoader().loadRobot(robot.file_location)))
            robot._x = random.randint(60, self._width - 60)
            robot._y = random.randint(60, self._height - 60)
            robot._myID = len(self._robots) - 1
        
        for robot in self._robots:
            print("Starting run thread")
            threading.Thread(target=robot.run).start()
    
    @classmethod
    def stopBattle(self) -> None:
        self._state = 0
        for robot in self._robots:
            robot._unregister(self.CANVAS)
        self._bullets = []

    @classmethod
    def pauseBattle(self) -> None:
        ...

    @classmethod
    def restartBattle(self) -> None:
        BattleField.stopBattle()
        BattleField.setupNewBattle(self._base_robots)