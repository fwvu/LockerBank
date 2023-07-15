import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from lb_assets import *
from lb_maintenance_commands import *


# Maintenance frame -- used to reset the locker bank state
class lbMaintenance(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=appGreen)
        self.controller = controller

        self.bodyScreen = tk.Label(self, text="screen", image='')
        self.bodyScreen.pack()

        self.hold_img()


        # FOOTER FOR TESTING -- REMOVE --

        self.footer = tk.Label(self, text="Maintenance footer")
        self.footer.pack(side="bottom", pady=10)

        checkButton = ttk.Button(self.footer, text="Locker State",  command=lambda: locker_state(self))
        checkButton.grid(row=1, column=1, pady=20, padx=30)

        resetLockerButton = ttk.Button(self.footer, text="Locker Reset",  command=lambda: locker_reset(self))
        resetLockerButton.grid(row=1, column=3, pady=20, padx=30)

        switch_window_button = ttk.Button(self.footer, text="Operational", command=lambda: controller.show_frame('lbOperational'))
        switch_window_button.grid(row=2, column=2, pady=20, padx=30)

        ##################################


    def hold_img(self):
        appBodyimg = Image.open(holdImg)
        appBodyimg = appBodyimg.resize((bodySizeX, bodySizeY))
        self.appBodyimg = ImageTk.PhotoImage(appBodyimg)

        self.bodyScreen.configure(image=self.appBodyimg)
        self.bodyScreen.update()

