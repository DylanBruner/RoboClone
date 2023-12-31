import math
from io import TextIOWrapper
from api.events.event import *
from security.classprotection import ProtectedClass, PermissionTree
from helper.eventqueue import EventQueue
from tkinter import Canvas


class AdvancedRobot(ProtectedClass):
    def __init__(self):
        super().__init__()

    # (yes, this indentation is correct)
    # Below this is all of the private data that the use can not directly obtain ================================================================================
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

        self._lastState = 0 # Use by _hasChanged to determine if the robot has changed since the last time it was drawn

        self._registerEvents()

    # Permissions ======================================================================================================
        """
        The permmission 'override' allows the code within the function to do whatever it wants,
        it does not allow the user to override the function itself.

        Apply base permissions to the class,
         - All functions should be read only (callable-only)
         - All other variables should be completly hidden
         NOTE: Anything created post-mapCurrent will not be affected by this (which is good, we dont want to mess with user defined stuff)
        """ # Oh and no, setting 'everything' to false doesn't actually set everything. Just things without permissions already set
        self._mapCurrent(PermissionTree().setPermissionForType(lambda a: callable(a), {'read': True, 'write': False, 'delete': False, 'override': True}))
        self._mapCurrent(PermissionTree().setPermissionForType(lambda x: True, {'read': False, 'write': False, 'delete': False, 'override': False}))

        # More specific permissions
        for func in dir(self):
            if func.startswith('_') and not func.startswith('__') and callable(getattr(self, func)) and not func == '_init__':
                self._setPermission(func, {'read': False, 'write': False, 'delete': False, 'override': True})

        self._enableSecurity() # Turn on security
        # self._init__() # Call the user defined init function, (no that's not a typo, it's a hack to initialize 
                       #                                       the security stuff before the user can run code)

    def _registerEvents(self):
        self._eventQueue.register(self.onScannedRobot, ScannedRobotEvent)
        self._eventQueue.register(self.onHitByBullet, HitByBulletEvent)
        self._eventQueue.register(self.onBulletHit, BulletHitEvent)
        self._eventQueue.register(self.onBulletHitBullet, BulletHitBulletEvent)
        self._eventQueue.register(self.onBulletMissed, BulletMissedEvent)
        self._eventQueue.register(self.onHitRobot, HitRobotEvent)
        self._eventQueue.register(self.onHitWall, HitWallEvent)
        self._eventQueue.register(self.onRobotDeath, RobotDeathEvent)
        self._eventQueue.register(self.onDeath, DeathEvent)
        self._eventQueue.register(self.onRoundEnded, RoundEndedEvent)
        self._eventQueue.register(self.onBattleEnded, BattleEndedEvent)
        self._eventQueue.register(self.onSkippedTurn, SkippedTurnEvent)
        self._eventQueue.register(self.onStatus, StatusEvent)
        self._eventQueue.register(self.onWin, WinEvent)
        # self._eventQueue.register(self._robot.onPaint, PaintEvent)
    
    def _getParts(self) -> list[int]: return self._partIDS
    def _setParts(self, parts: list[int]) -> None: self._partIDS = parts
    def _hasChanged(self) -> bool:
        current_sum = self._x + self._y + self._robotHeading + self._gunHeading + self._radarHeading + self._energy + self._gunHeat
        if current_sum != self._lastState:
            self._lastX = self._x
            self._lastY = self._y
            self._lastRobotHeading = self._robotHeading
            self._lastGunHeading = self._gunHeading
            self._lastRadarHeading = self._radarHeading
            self._lastEnergy = self._energy
            self._lastState = current_sum
        return self._lastState != current_sum
    
    def _unregister(self, canvas: Canvas) -> None:
        for part in self._partIDS:
            canvas.delete(part)

    # Below this is all of the functions that the user can call =================================================================================================

    # Setters ==================================================================
    def ahead(self, distance: float) -> None: ...
    def back(self, distance: float) -> None: ...
    def doNothing(self) -> None: ...
    def fire(self, power: float) -> None: ...
    def resume(self) -> None: ...
    def scan(self) -> None: ...
    # def setAdjustGunForRobotTurn(self, independent: bool) -> None: ...
    # def setAdjustRadarForGunTurn(self, independent: bool) -> None: ...
    # def setAdjustRadarForRobotTurn(self, independent: bool) -> None: ...
    def setAllColors(self, color: str) -> None: ...
    def setBodyColor(self, color: str) -> None: ...
    def setBulletColor(self, color: str) -> None: ...
    def setGunColor(self, color: str) -> None: ...
    def setColors(self, bodyColor: str, gunColor: str, radarColor: str, bulletColor: str = None, scanArcColor: str = None) -> None: ...
    def setDebugProperty(self, key: str, value: str) -> None: ...
    def setGunColor(self, color: str) -> None: ...
    def setRadarColor(self, color: str) -> None: ...
    def setScanColor(self, color: str) -> None: ...
    def stop(self) -> None: ...
    def turnGunLeft(self, degrees: float) -> None: ...
    def turnLeft(self, degrees: float) -> None: ...
    def turnRadarLeft(self, degrees: float) -> None: ...
    def turnRadarRight(self, degrees: float) -> None: ...
    def turnRight(self, degrees: float) -> None: ...
    a = ""
    def execute(self) -> None: ...
    def setTurnLeft(self, degrees: float) -> None: ...
    def setTurnRight(self, degrees: float) -> None: ...
    def setTurnRadarLeft(self, degrees: float) -> None: ...
    def setTurnRadarRight(self, degrees: float) -> None: ...
    def setTurnGunLeft(self, degrees: float) -> None: ...
    def setTurnGunRight(self, degrees: float) -> None: ...
    def setTurnLeftRadians(self, radians: float) -> None: ...
    def setTurnRightRadians(self, radians: float) -> None: ...
    def setTurnRadarLeftRadians(self, radians: float) -> None: ...
    def setTurnRadarRightRadians(self, radians: float) -> None: ...
    def setTurnGunLeftRadians(self, radians: float) -> None: ...
    def setTurnGunRightRadians(self, radians: float) -> None: ...
    def setAhead(self, distance: float) -> None: ...
    def setBack(self, distance: float) -> None: ...
    def setFire(self, power: float) -> None: ...
    def clearAllEvents(self) -> None: ...
    def setMaxTurnRate(self, newMaxTurnRate: float) -> None: ...
    def setMaxVelocity(self, newMaxVelocity: float) -> None: ...
    def setStop(self) -> None: ...
    def setResume(self) -> None: ...
    
    # Getters ==================================================================
    def getAllEvents(self) -> list[Event]: ...
    def getBulletHitEvents(self) -> list[BulletHitEvent]: ...
    def getBulletHitBulletEvents(self) -> list[BulletHitBulletEvent]: ...
    def getBulletMissedEvents(self) -> list[BulletMissedEvent]: ...
    def getHitByBulletEvents(self) -> list[HitByBulletEvent]: ...
    def getStatusEvents(self) -> list[StatusEvent]: ...
    def getHitWallEvents(self) -> list[HitWallEvent]: ...
    def getRobotHitEvents(self) -> list[HitRobotEvent]: ...
    def getRobotDeathEvents(self) -> list[RobotDeathEvent]: ...
    def getScannedRobotEvents(self) -> list[ScannedRobotEvent]: ...
    
    def getDataDirectory(self) -> str: ...
    def getDataFile(self, filename: str, mode: str) -> TextIOWrapper: ...
    def getDataQuotaAvailable(self) -> int: ...
    def getDistanceRemaining(self) -> float: ...
    def getBattleFieldHeight(self) -> float: ...
    def getBattleFieldWidth(self) -> float: ...
    # def getGraphics(self) -> None: ...
    def getGunCoolingRate(self) -> float: ...
    def getHeight(self) -> float: ...
    def getName(self) -> str: ...
    def getNumRounds(self) -> int: ...
    def getNumSentries(self) -> int: ...
    def getOthers(self) -> int: ...
    def getRoundNum(self) -> int: ...
    def getSentryBorderSize(self) -> int: ...
    def getVelocity(self) -> float: ...
    def getWidth(self) -> float: ...
    def getTime(self) -> float: ...

    def getRadarHeadingRadians(self) -> float: return math.radians(self._radarHeading)
    def getRadarHeading(self) -> float: return self._radarHeading
    def getGunHeat(self) -> float: return self._gunHeat
    def getGunTurnRemaining(self) -> float: return self._gunHeadingTarget - self._gunHeading
    def getHeading(self) -> float: return self._robotHeading
    def getGunHeading(self) -> float: return self._gunHeading
    def getGunTurnRemainingRadians(self) -> float: return math.radians(self._gunHeadingTarget - self._gunHeading)
    def getHeadingRadians(self) -> float: return math.radians(self._robotHeading)
    def getEnergy(self) -> float: return self._energy
    def getX(self) -> float: return self._x
    def getY(self) -> float: return self._y
    def getRadarTurnRemaining(self) -> float: return self._radarHeadingTarget - self._radarHeading
    def getRadarTurnRemainingRadians(self) -> float: return math.radians(self._radarHeadingTarget - self._radarHeading)
    def getTurnRemaining(self) -> float: return self._robotHeadingTarget - self._robotHeading
    def getTurnRemainingRadians(self) -> float: return math.radians(self._robotHeadingTarget - self._robotHeading)
    # def isAdjustGunForRobotTurn(self) -> bool: ...
    # def isAdjustRadarForGunTurn(self) -> bool: ...
    # def isAdjustRadarForRobotTurn(self) -> bool: ...

    # events ===================================================================
    def run(self) -> None: print("run() not implemented")
    def onSkippedTurn(self, event: SkippedTurnEvent) -> None: ...
    def onBattleEnded(self, event: BattleEndedEvent) -> None: ...
    def onBulletHit(self, event: BulletHitEvent) -> None: ...
    def onBulletHitBullet(self, event: BulletHitBulletEvent) -> None: ...
    def onBulletMissed(self, event: BulletMissedEvent) -> None: ...
    def onDeath(self, event: DeathEvent) -> None: ...
    def onHitByBullet(self, event: HitByBulletEvent) -> None: ...
    def onHitRobot(self, event: HitRobotEvent) -> None: ...
    def onHitWall(self, event: HitWallEvent) -> None: ...
    # def onPaint(self, event: PaintEvent) -> None: ...
    def onRobotDeath(self, event: RobotDeathEvent) -> None: ...
    def onRoundEnded(self, event: RoundEndedEvent) -> None: ...
    def onScannedRobot(self, event: ScannedRobotEvent) -> None: ...
    def onStatus(self, event: StatusEvent) -> None: ...
    def onWin(self, event: WinEvent) -> None: ...