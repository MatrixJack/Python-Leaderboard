# -[ Python Modules ]- #
import tkinter

# -[ Python buffs ]- #
def createWarning(name, description, font = "Helvetica"):
    master = tkinter.Tk()

    master.geometry("300x50")
    master.title(name)
    
    master.resizable(False, False)

    messageLabel = tkinter.Label(master, text = description, font = font) 
    messageLabel.pack(side=tkinter.TOP, expand=tkinter.YES)

    master.mainloop()