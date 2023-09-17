import random, threading
from PIL import Image, ImageTk
from tkinter import Canvas
from api.robocloneapi import AdvancedRobot
from ui.battle.battlefield import BattleField
from pygame.time import Clock
from helper.garbagefix import GarbageFix

class BattleView:
    IMAGE_DUMP: dict = GarbageFix(5)
    GROUND_TILES = [Image.open(f"images/ground/blue_metal/blue_metal_{i}.png") for i in range(0, 4)]
    GROUND_TILE_WIDTH: int = GROUND_TILES[0].width
    CANVAS: Canvas = None

    def __init__(self, canvas: Canvas, battleField: BattleField):
        self.CANVAS = BattleField.CANVAS = canvas
        self.battleField = battleField
        self.groundImage = self.createGroundImage()
        self.idleImage   = self.createIdleImage()

        self.groundImageID = self.CANVAS.create_image(0, 0, image=self.groundImage, anchor="nw")
        self.idleImageID   = self.CANVAS.create_image(0, 0, image=self.idleImage, anchor="nw")

        self.running = True
        self.mainThread = threading.Thread(target=self.mainloop)
        self.mainThread.daemon = True
        self.mainThread.start()

    def createIdleImage(self) -> ImageTk:
        logo = Image.open("images/logo.png")

        idleImage = Image.new("RGBA", (self.battleField.getWidth(), self.battleField.getHeight()))
        idleImage.paste((0, 0, 0), (0, 0, self.battleField.getWidth(), self.battleField.getHeight()))

        logoX = (self.battleField.getWidth() - logo.width) / 2
        logoY = (self.battleField.getHeight() - logo.height) / 2

        idleImage.paste(logo, (int(logoX), int(logoY)))

        return ImageTk.PhotoImage(idleImage)

    def createGroundImage(self) -> ImageTk:
        NUM_HORZ_TILES = self.battleField.getWidth() / self.GROUND_TILE_WIDTH + 1
        NUM_VERT_TILES = self.battleField.getHeight() / self.GROUND_TILE_WIDTH + 1

        groundImage = Image.new("RGBA", (self.battleField.getWidth(), self.battleField.getHeight()))

        for i in range(0, int(NUM_HORZ_TILES)):
            for j in range(0, int(NUM_VERT_TILES)):
                groundImage.paste(random.choice(self.GROUND_TILES), (i * self.GROUND_TILE_WIDTH, j * self.GROUND_TILE_WIDTH))

        
        return ImageTk.PhotoImage(groundImage)

    # Body, Turret, Radar
    def drawRobot(self, robot: AdvancedRobot) -> None:
        forceRedraw = False
        if len(robot.getParts()) == 0:
            forceRedraw = True
            x, y = robot.getX(), robot.getY()

            robot._images[0] = body_image = Image.open("images/robot/body.png")
            robot._images[1] = turret_image = Image.open("images/robot/turret.png")
            robot._images[2] = radar_image = Image.open("images/robot/radar.png")

            body = Image.new("RGBA", (body_image.width * 2, body_image.height * 2))
            turret = Image.new("RGBA", (turret_image.width * 4, turret_image.height * 4))
            radar = Image.new("RGBA", (radar_image.width * 2, radar_image.height * 2))

            # Calculate the center position for pasting the images
            body_center = (body.width // 2, body.height // 2)
            turret_center = (turret.width // 2, turret.height // 2)
            radar_center = (radar.width // 2, radar.height // 2)

            # Paste the original images centered on the larger canvases
            body.paste(body_image, (body_center[0] - body_image.width // 2, body_center[1] - body_image.height // 2))
            turret.paste(turret_image, (turret_center[0] - turret_image.width // 2, turret_center[1] - turret_image.height // 2))
            radar.paste(radar_image, (radar_center[0] - radar_image.width // 2, radar_center[1] - radar_image.height // 2))

            robot._images[0] = body_image = body
            robot._images[1] = turret_image = turret
            robot._images[2] = radar_image = radar



            self.IMAGE_DUMP[f'body-{robot._myID}'] = ImageTk.PhotoImage(body_image)
            self.IMAGE_DUMP[f'turret-{robot._myID}'] = ImageTk.PhotoImage(turret_image)
            self.IMAGE_DUMP[f'radar-{robot._myID}'] = ImageTk.PhotoImage(radar_image)

            robot.setParts(
                [
                    self.CANVAS.create_image(x, y, image=self.IMAGE_DUMP[f'body-{robot._myID}'], anchor="nw"),
                    self.CANVAS.create_image(x, y, image=self.IMAGE_DUMP[f'turret-{robot._myID}'], anchor="nw"),
                    self.CANVAS.create_image(x, y, image=self.IMAGE_DUMP[f'radar-{robot._myID}'], anchor="nw")
                ]
            )

        if robot.hasChanged() or forceRedraw:
            x, y = robot.getX(), robot.getY()

            self.IMAGE_DUMP[f'body-{robot._myID}'] = ImageTk.PhotoImage(i1 := robot._images[0].rotate(robot.getRobotHeading()))
            self.IMAGE_DUMP[f'turret-{robot._myID}'] = ImageTk.PhotoImage(i2 := robot._images[1].rotate(robot.getGunHeading()))
            self.IMAGE_DUMP[f'radar-{robot._myID}'] = ImageTk.PhotoImage(i3 := robot._images[2].rotate(robot.getRadarHeading()))

            # update the images
            self.CANVAS.itemconfig(robot.getParts()[0], image=self.IMAGE_DUMP[f'body-{robot._myID}'])
            self.CANVAS.itemconfig(robot.getParts()[1], image=self.IMAGE_DUMP[f'turret-{robot._myID}'])
            self.CANVAS.itemconfig(robot.getParts()[2], image=self.IMAGE_DUMP[f'radar-{robot._myID}'])

            # move all the parts to be centered on the robot
            i = 0
            for part in robot.getParts():
                height, width = robot._images[i].height, robot._images[i].width
                self.CANVAS.coords(part, x - width / 2, y - height / 2)
                i += 1

    
    def mainloop(self) -> None:
        clock = Clock()
        lastState = 0
        try:
            while self.running:
                if self.battleField.getState() != lastState:
                    lastState = self.battleField.getState()
                    if lastState == 1:
                        self.CANVAS.itemconfig(self.idleImageID, state="hidden")
                        self.CANVAS.itemconfig(self.groundImageID, state="normal")
                    elif lastState == 0:
                        self.CANVAS.itemconfig(self.idleImageID, state="normal")
                        self.CANVAS.itemconfig(self.groundImageID, state="hidden")


                for robot in self.battleField.getRobots():
                    self.drawRobot(robot)
                clock.tick(60)
        except Exception as e:
            if self.running:
                raise e
        print("BattleView thread stopped")
        self.running = True # Signal that the thread has stopped