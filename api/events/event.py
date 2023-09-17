import math
from entities.bullet import Bullet
from api.events.robotstatus import RobotStatus

class Event(object):
    def __init__(self):
        self._time: float = 0.0

    def getTime(self) -> float: return self._time

class RobotScannedEvent(Event):
    def __init__(self, name: str, energy: float, bearing: float, heading: float, velocity: float, isSentryRobot: bool):
        self._name: str = name
        self._energy: float = energy
        self._bearing: float = bearing
        self._heading: float = heading
        self._velocity: float = velocity
        self._isSentryRobot: bool = isSentryRobot
    
    def getBearing(self) -> float: return self._bearing
    def getBearingRadians(self) -> float: return math.radians(self._bearing)
    def getEnergy(self) -> float: return self._energy
    def getHeading(self) -> float: return self._heading
    def getHeadingRadians(self) -> float: return math.radians(self._heading)
    def getName(self) -> str: return self._name
    def getVelocity(self) -> float: return self._velocity
    def isSentryRobot(self) -> bool: return self._isSentryRobot
    def getDistance(self) -> float: ...

class BulletHitEvent(Event):
    def __init__(self, name: str, energy: float, bullet: Bullet):
        self._name: str = name
        self._energy: float = energy
        self._bullet: Bullet = bullet

    def getBullet(self) -> Bullet: return self._bullet
    def getEnergy(self) -> float: return self._energy
    def getName(self) -> str: return self._name

class BulletHitBulletEvent(Event):
    def __init__(self, bullet: Bullet, hitBullet: Bullet):
        self.bullet: Bullet = bullet
        self.hitBullet: Bullet = hitBullet
    
    def getBullet(self) -> Bullet: return self.bullet
    def getHitBullet(self) -> Bullet: return self.hitBullet

class BulletMissedEvent(Event):
    def __init__(self, bullet: Bullet):
        self.bullet: Bullet = bullet
    
    def getBullet(self) -> Bullet: return self.bullet

class DeathEvent(Event):
    def __init__(self):
        pass

class HitByBulletEvent(Event):
    def __init__(self, bearing: float, bullet: Bullet):
        self._bearing: float = bearing
        self._bullet: Bullet = bullet
    
    def getBearing(self) -> float: return self._bearing
    def getBearingRadians(self) -> float: return math.radians(self._bearing)
    def getBullet(self) -> Bullet: return self._bullet
    def getHeading(self) -> float: return self._bullet.getHeading()
    def getHeadingRadians(self) -> float: return self._bullet.getHeadingRadians()
    def getName(self) -> str: return self._bullet.getName()
    def getPower(self) -> float: return self._bullet.getPower()
    def getVelocity(self) -> float: return self._bullet.getVelocity()

class HitRobotEvent(Event):
    def __init__(self, name: str, bearing: float, energy: float, atFault: bool):
        self._name: str = name
        self._bearing: float = bearing
        self._energy: float = energy
        self._atFault: bool = atFault
    
    def getBearing(self) -> float: return self._bearing
    def getBearingRadians(self) -> float: return math.radians(self._bearing)
    def getEnergy(self) -> float: return self._energy
    def getName(self) -> str: return self._name
    def isMyFault(self) -> bool: return self._atFault

class HitWallEvent(Event):
    def __init__(self, bearing: float):
        self._bearing: float = bearing
    
    def getBearing(self) -> float: return self._bearing
    def getBearingRadians(self) -> float: return math.radians(self._bearing)

class RobotDeathEvent(Event):
    def __init__(self, name: str):
        self._name: str = name
    
    def getName(self) -> str: return self._name

class StatusEvent(Event):
    def __inti__(self, status: RobotStatus):
        self._status: RobotStatus = status
    
    def getStatus(self) -> RobotStatus: return self._status

class WinEvent(Event):
    def __init__(self):
        pass