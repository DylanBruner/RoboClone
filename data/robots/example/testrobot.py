import time
from api.robocloneapi import AdvancedRobot

class robot(AdvancedRobot):
    def run(self):
        while True:
            self.ahead(100)
            self.turnGunRight(360)
            self.back(100)
            self.turnGunRight(360)
            time.sleep(1)

EXPORT = [robot]