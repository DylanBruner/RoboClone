import time
from api.robocloneapi import AdvancedRobot

class robot(AdvancedRobot):
    def __init__(self):
        print("woah im a robot")
    
    def run(self):
        while True:
            self.setAhead(50)
            while self.getDistanceRemaining() > 0:
                time.sleep(0.1)
            self.setBack(50)