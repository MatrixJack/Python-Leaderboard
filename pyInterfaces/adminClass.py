# -[ Python Modules ]- #
import tkinter
import sys

sys.path.append("./")

import pyModules.dialogue as dialogue
import pyInterfaces.interfaceClass as interfaceClass

# -[ Classes ]- #
class adminInterface(interfaceClass.interface):
    def __init__(self, master, register, destroy):
        self.name = "admin"
        self.enabled = True

        self.destroyCallback = destroy
        self.master = master
        self.register = register

        self.specialCharacters = "\"'!£$%^&*()_+-=][}{'#~@;:,./<>?|\\¬`"
        self.cache = {}

        self.frame = super()
        self.frame.__init__(self)

        self.elements = {}

        if self.enabled:
            self.master.protocol("WM_DELETE_WINDOW", self.onClose)

            self.master["bg"] = register.get("adm_background_color")
            self.master.title("Administrator Menu")
            self.master.geometry("300x120")
            self.master.resizable(False, False)

            self.register.set("adminInterface", self)

            self.createElements()
            self.packElements()

    def onClose(self):
        self.destroyCallback(self.master)

    def checkNameIntegrity(self, text):
        if any(character in self.specialCharacters for character in text):
            return False
        else:
            return True

    def checkPointsIntegrity(self, text):
        chunk = {}
        
        try:
            chunk[0] = int(text)
        except:
            return False

        if chunk[0]:
            return True

    def onAppendRequest(self):
        interface = self.register.get("boardInterface")
        variables = self.register.get("teamVariables")

        name = self.elements["teamNameBox"].get()
        points = self.elements["teamPointsBox"].get()

        if self.checkPointsIntegrity(points) and self.checkNameIntegrity(name):
            if variables.get(name) == None:
                if int(points) <= self.register.get("max_points") and int(points) >= 0:
                    variables[name] = int(points)
                    interface.updateBoard()
                else:
                    dialogue.createWarning("Warning", "Exceeded points limit!", self.register.get("adm_font"))
            else:
                dialogue.createWarning("Warning", "That team already exists!", self.register.get("adm_font"))
        else:
            dialogue.createWarning("Warning", "The TeamName or Points is malformed!", self.register.get("adm_font"))

    def onRemoveRequest(self):
        interface = self.register.get("boardInterface")
        variables = self.register.get("teamVariables")

        name = self.elements["teamNameBox"].get()

        if self.checkNameIntegrity(name):
            if variables.get(name) != None:
                variables.pop(name)
                interface.updateBoard()
            else:
                dialogue.createWarning("Warning", "That team doesn't exists!", self.register.get("adm_font"))
        else:
            dialogue.createWarning("Warning", "The TeamName or Points is malformed!", self.register.get("adm_font"))

    def onCleanRequest(self):
        interface = self.register.get("boardInterface")

        self.register.set("teamVariables", {})

        interface.updateBoard()

    def onSaveRequest(self):
        sqlStreamer = self.register.get("sqlStream")
        variables = self.register.get("teamVariables")

        if self.cache["variablecache"] == variables: return
        self.cache["variablecache"] = variables

        for teamName in variables:
            teamPoints = variables[teamName]

            sqlStreamer.executeSQL(f"""INSERT INTO {sqlStreamer.getHostTableName()} (team_name, team_points)
            VALUES ('{teamName}', '{teamPoints}')""", False)

        sqlStreamer.commit()

    def onModifyRequest(self):
        interface = self.register.get("boardInterface")
        variables = self.register.get("teamVariables")

        name = self.elements["teamNameBox"].get()
        points = self.elements["teamPointsBox"].get()

        if self.checkPointsIntegrity(points) and self.checkNameIntegrity(name):
            if variables.get(name) != None:
                if int(points) <= self.register.get("max_points") and int(points) >= 0:
                    variables[name] = int(points)
                    interface.updateBoard()
                else:
                    dialogue.createWarning("Warning", "Exceeded points limit!", self.register.get("adm_font"))
            else:
                dialogue.createWarning("Warning", "That team doesn't exists!", self.register.get("adm_font"))
        else:
            dialogue.createWarning("Warning", "The TeamName or Points is malformed!", self.register.get("adm_font"))

    def createElements(self):
        # -[ Frames ]- #
        mainWidgets = self.frame.create(
            "mainWidgets", 
            "Frame",
            bg=self.register.get("adm_label_color")
        )
        
        teamNameFrame = self.frame.oCreate(
            "teamNameWidgets", 
            "Frame", 
            mainWidgets,
            bg=self.register.get("adm_label_color")
        )

        teamPointsFrame = self.frame.oCreate(
            "teamPointsWidgets", 
            "Frame", 
            mainWidgets,
            bg=self.register.get("adm_label_color")
        )

        buttonWidgets = self.frame.oCreate(
            "buttonWidgets", 
            "Frame", 
            mainWidgets,
            bg=self.register.get("adm_label_color")
        )

        bottombuttonWidgets = self.frame.oCreate(
            "bottombuttonWidgets", 
            "Frame", 
            mainWidgets,
            bg=self.register.get("adm_label_color")
        )

        # -[ Widgets ]- #
        self.frame.oCreate(
            "appendBtn", 
            "Button", 
            buttonWidgets, 
            text="Append", 
            font=self.register.get("adm_font"),
            command=self.onAppendRequest,
            bg=self.register.get("adm_label_color"),
            fg=self.register.get("adm_title_text_color"),
            highlightthickness=0
        )

        self.frame.oCreate(
            "removeBtn", 
            "Button", 
            buttonWidgets, 
            text="Remove", 
            font=self.register.get("adm_font"),
            command=self.onRemoveRequest,
            bg=self.register.get("adm_label_color"),
            fg=self.register.get("adm_title_text_color"),
            highlightthickness=0
        )

        self.frame.oCreate(
            "modifyBtn", 
            "Button", 
            buttonWidgets, 
            text="Modify", 
            font=self.register.get("adm_font"),
            command=self.onModifyRequest,
            bg=self.register.get("adm_label_color"),
            fg=self.register.get("adm_title_text_color"),
            highlightthickness=0
        )

        self.frame.oCreate(
            "clearBtn", 
            "Button", 
            bottombuttonWidgets, 
            text="Clear", 
            font=self.register.get("adm_font"),
            command=self.onCleanRequest,
            bg=self.register.get("adm_label_color"),
            fg=self.register.get("adm_title_text_color"),
            highlightthickness=0
        )

        self.frame.oCreate(
            "saveBtn", 
            "Button", 
            bottombuttonWidgets, 
            text="Save", 
            font=self.register.get("adm_font"),
            command=self.onCleanRequest,
            bg=self.register.get("adm_label_color"),
            fg=self.register.get("adm_title_text_color"),
            highlightthickness=0
        )

        self.frame.oCreate(
            "teamNameLabel", 
            "Label", 
            teamNameFrame, 
            text="Team Name: ",
            font=self.register.get("adm_font"),
            bg=self.register.get("adm_label_color"),
            fg=self.register.get("adm_title_text_color"),
            highlightthickness=0
        )

        self.frame.oCreate(
            "teamPointsLabel", 
            "Label", 
            teamPointsFrame, 
            text="Team Points: ",
            font=self.register.get("adm_font"),
            bg=self.register.get("adm_label_color"),
            fg=self.register.get("adm_title_text_color"),
            highlightthickness=0
        )

        self.frame.oCreate(
            "teamNameBox", 
            "TextBox", 
            teamNameFrame,
            font=self.register.get("adm_font"),
            bg=self.register.get("adm_label_color"),
            fg=self.register.get("adm_text_color"),
            highlightthickness=0
        )

        self.frame.oCreate(
            "teamPointsBox", 
            "TextBox", 
            teamPointsFrame,
            font=self.register.get("adm_font"),
            bg=self.register.get("adm_label_color"),
            fg=self.register.get("adm_text_color"),
            highlightthickness=0
        )

        #self.frame.colorOnHover(appendBtn, self.register.get("adm_button_down_color"))
        #self.frame.colorOnHover(removeBtn, self.register.get("adm_button_down_color"))
        #self.frame.colorOnHover(modifyBtn, self.register.get("adm_button_down_color"))

    def packElements(self):
        # -[ Frames ]- #
        self.elements["mainWidgets"].pack(expand = True)
        self.elements["teamNameWidgets"].pack(side = tkinter.TOP)
        self.elements["teamPointsWidgets"].pack(side = tkinter.TOP)
        self.elements["bottombuttonWidgets"].pack(side = tkinter.BOTTOM)
        self.elements["buttonWidgets"].pack(side = tkinter.BOTTOM)

        # -[ Widgets ]- #
        self.elements["teamNameLabel"].pack(side = tkinter.LEFT)
        self.elements["teamPointsLabel"].pack(side = tkinter.LEFT)

        self.elements["teamNameBox"].pack(side = tkinter.RIGHT)
        self.elements["teamPointsBox"].pack(side = tkinter.RIGHT)

        self.elements["saveBtn"].pack(side = tkinter.LEFT)
        self.elements["clearBtn"].pack(side = tkinter.LEFT)
        self.elements["appendBtn"].pack(side = tkinter.LEFT)
        self.elements["removeBtn"].pack(side = tkinter.LEFT)
        self.elements["modifyBtn"].pack(side = tkinter.LEFT)

    def startThread(self):
        self.frame.mainloop()
