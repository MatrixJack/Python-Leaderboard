# -[ Python Modules ]- #
import tkinter
import sys

sys.path.append("./")

import pyInterfaces.interfaceClass as interfaceClass

# -[ Classes ]- #
class masterInterface(interfaceClass.interface):
    def __init__(self, master, register):
        self.name = "master"
        self.master = master
        self.register = register

        self.register.set("guiMaster", master)

        self.canSysExit = False
        self.windowsAlive = 0

        self.frame = super()
        self.frame.__init__(self)

    def tkChildClosing(self, window):
        window.destroy()

        self.windowsAlive += -1
        if self.windowsAlive == 0:
            sqlStreamer = self.register.get("sqlStream")
            variables = self.register.get("teamVariables")

            for teamName in variables:
                teamPoints = variables[teamName]

                sqlStreamer.executeSQL(f"""INSERT INTO {sqlStreamer.getHostTableName()} (team_name, team_points)
                VALUES ('{teamName}', '{teamPoints}')""", False)

            sqlStreamer.commit()
            sqlStreamer.disconnect()
            
            sys.exit()

    def buildInterface(self, interfaceClass):
        self.childWindow = tkinter.Toplevel(self.master)

        interfaceClass(self.childWindow, self.register, self.tkChildClosing)
        
        self.windowsAlive += 1
        if self.canSysExit != True: self.canSysExit = True
