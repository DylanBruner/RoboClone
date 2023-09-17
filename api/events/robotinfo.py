import math

class RobotStatus(object):
    def __init__(self):
        self._energy: float
        self._x: float
        self._y: float
        self._bodyHeading: float
        self._gunHeading: float
        self._radarHeading: float
        self._velocity: float
        self._bodyTurnRemaining: float
        self._radarTurnRemaining: float
        self._gunTurnRemaining: float
        self._distanceRemaining: float
        self._gunHeat: float
        self._time: float
        self._others: int
        self._numSentries: int
        self._roundNum: int
        self._numRounds: int
    
    def getEnergy(self) -> float: return self._energy
    def getX(self) -> float: return self._x
    def getY(self) -> float: return self._y
    def getBodyHeading(self) -> float: return self._bodyHeading
    def getBodyHeadingRadians(self) -> float: return math.radians(self._bodyHeading)
    def getGunHeading(self) -> float: return self._gunHeading
    def getGunHeadingRadians(self) -> float: return math.radians(self._gunHeading)
    def getRadarHeading(self) -> float: return self._radarHeading
    def getRadarHeadingRadians(self) -> float: return math.radians(self._radarHeading)
    def getVelocity(self) -> float: return self._velocity
    def getBodyTurnRemaining(self) -> float: return self._bodyTurnRemaining
    def getBodyTurnRemainingRadians(self) -> float: return math.radians(self._bodyTurnRemaining)
    def getRadarTurnRemaining(self) -> float: return self._radarTurnRemaining
    def getRadarTurnRemainingRadians(self) -> float: return math.radians(self._radarTurnRemaining)
    def getGunTurnRemaining(self) -> float: return self._gunTurnRemaining
    def getGunTurnRemainingRadians(self) -> float: return math.radians(self._gunTurnRemaining)
    def getDistanceRemaining(self) -> float: return self._distanceRemaining
    def getGunHeat(self) -> float: return self._gunHeat
    def getTime(self) -> float: return self._time
    def getOthers(self) -> int: return self._others
    def getNumSentries(self) -> int: return self._numSentries
    def getRoundNum(self) -> int: return self._roundNum
    def getNumRounds(self) -> int: return self._numRounds
    def getDistance(self) -> float: ...
    def getGunCoolingRate(self) -> float: ...
    def getGunHeat(self) -> float: ...

class BattleResults:
    def __init__(self, teamLeaderName: str, rank: int, score: float, survival: float, lastSurvivorBonus: float, bulletDamage: float, 
                 bulletDamageBonus: float, ramDamage: float, ramDamageBonus: float, firsts: int, seconds: int, thirds: int):
        self._teamLeaderName: str = teamLeaderName
        self._rank: int = rank
        self._score: float = score
        self._survival: float = survival
        self._lastSurvivorBonus: float = lastSurvivorBonus
        self._bulletDamage: float = bulletDamage
        self._bulletDamageBonus: float = bulletDamageBonus
        self._ramDamage: float = ramDamage
        self._ramDamageBonus: float = ramDamageBonus
        self._firsts: int = firsts
        self._seconds: int = seconds
        self._thirds: int = thirds
    
    def getBulletDamage(self) -> float: return self._bulletDamage
    def getBulletDamageBonus(self) -> float: return self._bulletDamageBonus
    def getFirsts(self) -> int: return self._firsts
    def getLastSurvivorBonus(self) -> float: return self._lastSurvivorBonus
    def getRamDamage(self) -> float: return self._ramDamage
    def getRamDamageBonus(self) -> float: return self._ramDamageBonus
    def getRank(self) -> int: return self._rank
    def getScore(self) -> float: return self._score
    def getSeconds(self) -> int: return self._seconds
    def getSurvival(self) -> float: return self._survival
    def getTeamLeaderName(self) -> str: return self._teamLeaderName
    def getThirds(self) -> int: return self._thirds