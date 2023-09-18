========== [CURRENT TODO LIST (i'm sure more will be added)] ==========

security:
  - classprotection.py
    - You can overwrite functions using def (possibly only when the class is initilized)
    - It's possible that any user defined functions and variables will be given permissions when they shouldn't be
    - imports need to be greatly limited
      - imports from advancedrobot should be hidden from the child
      - only whitelisted imports should be allowed (math, ...)
    - Do a general stress test of the permission system

  - general security
    - diskIO needs to be limited to certian folders and a certian amount of data stored

robocodeapi.py:
  - Implement all of the getters/setters
  - AntiCheat
  - Seperate stdout & stderr
  - See if it isn't possible to break up the file a bit
  - Decide whether or not setAdjustGunForRobotTurn and the others should actually be a thing, or if they'll default to all seperate 

misc:
  - Implement the main game loop
  - A rules object needs to be created that the robots can get to
  
ui:
  - Logging / debug menu like robocode
  - Allowing the robots to paint via onPaint