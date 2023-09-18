from api.robocloneapi import AdvancedRobot
from security.classprotection import ProtectedClass
from helper.eventqueue import EventQueue
from api.events.event import *
from tkinter import Canvas

class RoboHandler:
    def __init__(self, robot: AdvancedRobot):
        self._robot = robot
        self._eventQueue = EventQueue()


        # Drawing stuff
        self._myID = None
        self._images = [None, None, None]
        self._partIDS = []

        # Current Info
        self._energy = 100
        self._x = -1
        self._y = -1
        self._robotHeading = -1
        self._gunHeading = -1
        self._radarHeading = -1

        # Target Info
        self._robotHeadingTarget = 0
        self._gunHeadingTarget = 0
        self._radarHeadingTarget = 0
        self._robotMoveTarget = 0
        self._movementStopped = False

        # Shooting
        self._firePower = 0
        self._gunHeat = 0

        self._registerEvents()
    
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
    
    def _registerEvents(self):
        self._eventQueue.register(self._robot.onScannedRobot, ScannedRobotEvent)
        self._eventQueue.register(self._robot.onHitByBullet, HitByBulletEvent)
        self._eventQueue.register(self._robot.onBulletHit, BulletHitEvent)
        self._eventQueue.register(self._robot.onBulletHitBullet, BulletHitBulletEvent)
        self._eventQueue.register(self._robot.onBulletMissed, BulletMissedEvent)
        self._eventQueue.register(self._robot.onHitRobot, HitRobotEvent)
        self._eventQueue.register(self._robot.onHitWall, HitWallEvent)
        self._eventQueue.register(self._robot.onRobotDeath, RobotDeathEvent)
        self._eventQueue.register(self._robot.onDeath, DeathEvent)
        self._eventQueue.register(self._robot.onRoundEnded, RoundEndedEvent)
        self._eventQueue.register(self._robot.onBattleEnded, BattleEndedEvent)
        self._eventQueue.register(self._robot.onSkippedTurn, SkippedTurnEvent)
        self._eventQueue.register(self._robot.onStatus, StatusEvent)
        self._eventQueue.register(self._robot.onWin, WinEvent)
        # self._eventQueue.register(self._robot.onPaint, PaintEvent)