import math

class Bullet:
    def __init__(self, firer: str, location: tuple[int, int], power: float, heading: float):
        self._firer = firer
        self._victim = None
        self._isActive = True
        self._location = location
        self._power = power
        self._heading = heading
        self._velocity = 20 - 3 * power
    
    def _step(self, time_delta: float) -> None:
        # Calculate the change in position using velocity and heading based on the time passed
        delta_x = self.velocity * math.cos(math.radians(self.heading)) * time_delta
        delta_y = self.velocity * math.sin(math.radians(self.heading)) * time_delta

        # Update the bullet's location
        self.location = (self.location[0] + delta_x, self.location[1] + delta_y)

    # public methods
    def getHeading(self) -> float: return self._heading
    def getHeadingRadians(self) -> float: return math.radians(self._heading)
    def getPower(self) -> float: return self._power
    def getVelocity(self) -> float: return self._velocity
    def getName(self) -> str: return self._firer
    def getVictim(self) -> str: return self._victim
    def getX(self) -> float: return self._location[0]
    def getY(self) -> float: return self._location[1]
    def isActive(self) -> bool: return self._isActive