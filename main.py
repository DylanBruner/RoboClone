import threading
from ui.mainwindow import MainWindow
from security.securitysetup import SecurityManager
from helper.justimportit import JustImportIt

threading.Thread.daemon = True # make all threads daemons by default

win = MainWindow()