# -[ Python Modules ]- #
import tkinter
import sys

sys.path.append("./")

import pyInterfaces.interfaceClass as interfaceClass

# -[ Classes ]- #
class boardInterface(interfaceClass.interface):
    def __init__(self, master, register, destroy):
        self.name = "board"
        self.enabled = True

        self.settingsResizable = register.get("ldb_resizable")
        self.settingsSize = register.get("ldb_size")

        self.destroyCallback = destroy
        self.master = master
        self.register = register

        self.frame = super()
        self.frame.__init__(self)

        self.elements = {}
        self.table = {}

        if self.enabled:
            self.master.protocol("WM_DELETE_WINDOW", self.onClose)

            self.master["bg"] = register.get("ldb_background_color")
            self.master.title("Leaderboard Menu")
            self.master.resizable(self.settingsResizable, self.settingsResizable)

            self.register.set("boardInterface", self)

            self.createElements()
            self.gridElements()

            self.cleanBoard()
            self.updateBoard()

    def onClose(self):
        self.destroyCallback(self.master)

    def cleanBoard(self):
        for x in range(self.register.get("list_size")):
            setTable = self.table[x]

            setTable["name"].configure(text="-")
            setTable["points"].configure(text="0")

    def generateTeamList(self):
        variables = self.register.get("teamVariables")
        teamsTable = {}
        variableIndex = 0

        for teamName in variables:
            if variableIndex > self.register.get("list_size"): break
            teamName = teamName
            teamPoints = variables[teamName]

            teamsTable[teamName] = teamPoints
            variableIndex += 1

        return sorted(teamsTable.items(), key=lambda x: x[1], reverse=True) 

    def updateBoard(self):
        teamList = self.generateTeamList()
        teamIndex = 0

        self.cleanBoard()

        for teamValue in teamList:
            teamName, teamPoints = teamValue

            teamInterface = self.table[teamIndex]

            teamInterface["name"].configure(text=str(teamName))
            teamInterface["points"].configure(text=str(teamPoints))

            teamIndex += 1


    def initialzieWindowSize(self):
        setYScale = str(int(19 * self.register.get("list_size")) + 19)
        setXScale = str(int(self.elements["teamNameLabel"]["width"] + self.elements["teamPointsLabel"]["width"]))

        if self.settingsSize == "?x?": 
            self.master.geometry(f"{setXScale}x{setYScale}")
        else:
            self.master.geometry(self.settingsSize)

    def createElements(self):
        self.frame.create(
            "teamNameLabel", 
            "Label", 
            text="Team Name", 
            font=self.register.get("ldb_font"),
            bg=self.register.get("ldb_label_color"),
            fg=self.register.get("ldb_title_text_color")
        )

        self.frame.create(
            "teamPointsLabel", 
            "Label", 
            text="Team Points", 
            font=self.register.get("ldb_font"),
            bg=self.register.get("ldb_label_color"),
            fg=self.register.get("ldb_title_text_color")
        )

        for x in range(self.register.get("list_size")):
            widgetName = self.frame.create(
                f"{x}-1", 
                "Label", 
                text="-",
                font=self.register.get("ldb_font"),
                bg=self.register.get("ldb_label_color"),
                fg=self.register.get("ldb_text_color"),
                relief=self.register.get("ldb_relief"),
                width=self.register.get("ldb_width")
            )

            widgetPoints = self.frame.create(
                f"{x}-2", 
                "Label", 
                text="0",
                font=self.register.get("ldb_font"), 
                bg=self.register.get("ldb_label_color"),
                fg=self.register.get("ldb_text_color"),
                relief=self.register.get("ldb_relief"),
                width=self.register.get("ldb_width")
            )

            self.table[x] = {
                "name": widgetName,
                "points": widgetPoints
            }

    def gridElements(self):
        self.elements["teamNameLabel"].grid(column=0, row=0)
        self.elements["teamPointsLabel"].grid(column=1, row=0)

        for x in range(self.register.get("list_size")):
            setTable = self.table[x]

            setTable["name"].grid(column=0, row=(x + 1))
            setTable["points"].grid(column=1, row=(x + 1))

    def startThread(self):
        self.frame.mainloop()
