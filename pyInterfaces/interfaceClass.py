# -[ Python Modules ]- #
import tkinter

# -[ Variables ]- #
tkinter_typ = {
    "Button": tkinter.Button,
    "Label": tkinter.Label,
    "TextBox": tkinter.Entry,
    "Frame": tkinter.Frame,
}

# -[ Classes ]- #
class interface(tkinter.Frame):
    def __init__(self, interface):
        self.interface = interface

        super().__init__(self.interface.master)

    # -[ Create ]- #
    def create(self, indexName, elementType, **args):
        if self.interface == None: return

        element = tkinter_typ[elementType](self.interface.master, args)

        self.interface.elements[indexName] = element

        return element

    #def colorOnHover(self, button, color):
    #    origionalBG = button["bg"]

    #    def onHover(_):
    #        button["background"] = color

    #    def onRelease(_):
    #        button["background"] = origionalBG

    #    button.bind("<Enter>", onHover)
    #    button.bind("<Leave>", onRelease)

    # -[ Overidable Create ]- #
    def oCreate(self, indexName, elementType, master, **args):
        if self.interface == None: return

        element = tkinter_typ[elementType](master, args)

        self.interface.elements[indexName] = element

        return element
