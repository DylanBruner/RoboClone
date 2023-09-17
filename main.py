import threading
from ui.mainwindow import MainWindow

threading.Thread.daemon = True # make all threads daemons by default

win = MainWindow()