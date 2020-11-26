# -[ Python Modules ]- #
import tkinter
import sys

sys.path.append("./")

import pyInterfaces.adminClass
import pyInterfaces.boardClass
import pyInterfaces.masterClass

# -[ Variables ]- #
memory_intf = {}

# -[ Classes ]- #
class createInterfaceClasses():
    def __init__(self, register):
        if "admin" in memory_intf: return
        if "board" in memory_intf: return

        self.window = tkinter.Tk()
        self.window.withdraw()

        self.masterInterface = pyInterfaces.masterClass.masterInterface(self.window, register)
        self.masterInterface.buildInterface(pyInterfaces.adminClass.adminInterface)
        self.masterInterface.buildInterface(pyInterfaces.boardClass.boardInterface)

    def startThreads(self):
        self.masterInterface.mainloop()