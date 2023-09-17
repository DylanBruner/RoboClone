import time, os
import tkinter as tk
from ui.battleview import BattleView
from ui.battlefield import BattleField

"""
Sizes
 - battle field: 800x600
 - bottom pannel: 912x43
 - right pannel: 111x573
"""

class MainWindow:
    DEFAULT_WINDOW_SIZE = (915, 690)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RoboClone")
        self.root.geometry(f"{self.DEFAULT_WINDOW_SIZE[0]}x{self.DEFAULT_WINDOW_SIZE[1]}")
        self.root.iconbitmap("images/robocode.ico")
        self.root.resizable(True, True)

        self.setupMenubar()
        self.setupPannels()
        self.setupCanvas()

        self.battleField = BattleField()
        self.battleView  = BattleView(self.battlecanvas, self.battleField)

        self.root.protocol("WM_DELETE_WINDOW", self.onWindowClose)
        self.root.mainloop()

    def setupPannels(self) -> None:
        # bottom pannel ===================================================================================================
        self.bottompannel = tk.Frame(self.root, width=912, height=43, bg="#f0f0f0")

        #Pause/Debug, Next Turn, Stop, Restart
        pauseButton = tk.Button(self.bottompannel, text="Pause/Debug", height=1, relief=tk.SOLID, bg="#f0f0f0", borderwidth=0,
                                activebackground="#e0e0e0", command=self.pauseBattle)
        pauseButton.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=(10, 0))

        nextTurnButton = tk.Button(self.bottompannel, text="Next Turn", height=1, relief=tk.SOLID, bg="#f0f0f0", borderwidth=0,
                                    activebackground="#e0e0e0", command=self.nextTurn)
        nextTurnButton.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        stopButton = tk.Button(self.bottompannel, text="Stop", height=1, relief=tk.SOLID, bg="#f0f0f0", borderwidth=0,
                                activebackground="#e0e0e0", command=self.stopBattle)
        stopButton.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        restartButton = tk.Button(self.bottompannel, text="Restart", height=1, relief=tk.SOLID, bg="#f0f0f0", borderwidth=0,
                                    activebackground="#e0e0e0", command=self.restartBattle)
        restartButton.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # separatorLine = tk.Canvas(self.bottompannel, width=1, bg="gray")
        # separatorLine.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        slider = tk.Scale(self.bottompannel, from_=0, to=1000, orient=tk.HORIZONTAL, length=400, showvalue=0, tickinterval=100,
                        resolution=1, command=self.sliderChange)
        slider.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=(10, 0), pady=(20, 0))


        self.bottompannel.pack(side=tk.BOTTOM, fill=tk.X, expand=False)


        # right pannel ====================================================================================================
        self.rightpannel = tk.Frame(self.root, width=111, height=573, bg="#f0f0f0")
        mainBattleLogButton = tk.Button(self.rightpannel, text="Main Battle Log", width=11, height=1, relief=tk.SOLID, bg="#fdfdfd", borderwidth=1, 
                                        activebackground="#e0e0e0")
        mainBattleLogButton.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
        self.rightpannel.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    """
    Sets up the canvas for the battle field.
    """
    def setupCanvas(self) -> None:
        self.battlecanvas = tk.Canvas(self.root, width=800, height=600, bg="black")
        self.battlecanvas.pack(side=tk.TOP, expand=True, padx=0)

    """
    Sets up the menubar for the main window.
    """
    def setupMenubar(self) -> None:
        menubar = tk.Menu(self.root)
        battlemenu = tk.Menu(menubar, tearoff=0)
        battlemenu.add_command(label="New", accelerator="Ctrl+N", command=self.newBattle)
        battlemenu.add_command(label="Open", accelerator="Ctrl+O", command=self.openBattle)
        battlemenu.add_separator()
        battlemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.saveBattle)
        battlemenu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.saveBattleAs)
        battlemenu.add_separator()
        battlemenu.add_command(label="Open Record", accelerator="Ctrl+Shift+O", command=self.openRecord)
        battlemenu.add_command(label="Save Record", accelerator="Ctrl+R", command=self.saveRecord)
        battlemenu.add_command(label="Import XML Record", accelerator="Ctrl+I", command=self.importXMLRecord)
        battlemenu.add_command(label="Export XML Record", accelerator="Ctrl+X", command=self.exportXMLRecord)
        battlemenu.add_separator()
        battlemenu.add_command(label="Take Screenshot", accelerator="Ctrl+T", command=self.takeScreenshot)
        battlemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Battle", menu=battlemenu)

        robotmenu = tk.Menu(menubar, tearoff=0)
        robotmenu.add_command(label="Source Editor", accelerator="Ctrl+E", command=self.sourceEditor)
        robotmenu.add_separator()
        robotmenu.add_command(label="Import robot or team", command=self.importRobot)
        robotmenu.add_command(label="Package robot or team", command=self.packageRobot)
        robotmenu.add_separator()
        robotmenu.add_command(label="Create a robot team", command=self.createTeam)
        menubar.add_cascade(label="Robot", menu=robotmenu)

        optionsmenu = tk.Menu(menubar, tearoff=0)
        optionsmenu.add_command(label="Preferences", command=self.preferences)
        optionsmenu.add_command(label="Default window size", command=self.defaultWindowSize)
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Show current rankings", command=self.showRankings)
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Recalculate CPU constant", command=self.recalculateCPUConstant)
        optionsmenu.add_command(label="Clean robot cache", command=self.cleanRobotCache)
        menubar.add_cascade(label="Options", menu=optionsmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

    def newBattle(self) -> None: print(self.root.winfo_width(), self.root.winfo_height())
    def openBattle(self) -> None: ...
    def saveBattle(self) -> None: ...
    def saveBattleAs(self) -> None: ...
    def openRecord(self) -> None: ...
    def saveRecord(self) -> None: ...
    def importXMLRecord(self) -> None: ...
    def exportXMLRecord(self) -> None: ...
    def takeScreenshot(self) -> None: ...

    def sourceEditor(self) -> None: ...
    def importRobot(self) -> None: ...
    def packageRobot(self) -> None: ...
    def createTeam(self) -> None: ...

    def preferences(self) -> None: ...
    def defaultWindowSize(self) -> None:
        self.root.geometry(f"{self.DEFAULT_WINDOW_SIZE[0]}x{self.DEFAULT_WINDOW_SIZE[1]}")
    def showRankings(self) -> None: ...
    def recalculateCPUConstant(self) -> None: ...
    def cleanRobotCache(self) -> None: ...

    def pauseBattle(self) -> None: ...
    def nextTurn(self) -> None: ...
    def stopBattle(self) -> None: ...
    def restartBattle(self) -> None: ...
    def sliderChange(self, value: int) -> None: ...

    def onWindowClose(self):
        self.root.destroy()
        # os._exit(0)
        

if __name__ == "__main__":
    win = MainWindow()