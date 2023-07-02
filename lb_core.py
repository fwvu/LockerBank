import tkinter as tk
from tkinter import ttk

from lb_maintenance import *
from lb_operational import *
from lb_assets import *
from lb_menu import *



# Open a standard window
class Core(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        menuBar = menu_bar(self)
        self.config(menu=menuBar)

        # HEADER
        self.appName = tk.Label(self, text=appTitle, font="courier 40 bold", background=appGreen)
        self.appName.pack(pady=20)

        # creating a frame and assigning it to container
        container = tk.Frame(self, height=400, width=600)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # dictionary of frames
        self.frames = {}

        # list to store the 2 screens
        for F in (lbOperational, lbMaintenance):
            cont = F.__name__
            frame = F(container, self)
            self.frames[cont] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # first displayed frame
        self.show_frame('lbOperational')

    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()


# RUN
if __name__ == "__main__":
    app = Core()       
    app.title(appTitle)
    app.geometry(f'{mainWinSizeX}x{mainWinSizeY}')
    app.iconbitmap(iconImg)
    app.config(bg=appGreen)
    app.mainloop()