import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from lb_assets import *
from lb_op_commands import *


# Operational Frame -- main way public interacts with system
class lbOperational(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=appGreen)
        self.controller = controller

        # set up camera object called cam which we will be used with OpenCV
        self.cam = None

        # BODY FRAME 
        self.bodyScreen = tk.Label(self, text="Body Frame", image='')
        self.bodyScreen.pack()

        self.hold_img()

        # FOOTER FOR TESTING -- REMOVE or add to screen menu--

        self.footer = tk.Label(self, text="Operations footer")
        self.footer.pack(side="bottom", pady=10)

        startButton = ttk.Button(self.footer, text="Full Test",  command=lambda: open_cam(self))
        startButton.grid(row=1, column=0, pady=20, padx=30)

        resetButton = ttk.Button(self.footer, text="Reset",  command=lambda: close_cam(self))
        resetButton.grid(row=1, column=2, pady=20, padx=30)

        checkButton = ttk.Button(self.footer, text="Locker State",  command=lambda: locker_select(self))
        checkButton.grid(row=1, column=3, pady=20, padx=30)


        switch_window_button = ttk.Button(self.footer, text="Maintenance", command=lambda: controller.show_frame('lbMaintenance'))
        switch_window_button.grid(row=2, column=2, pady=20, padx=30)

        ##################################
   

    def clear_bodyScreen(self):
        for widgets in self.bodyScreen.winfo_children():
            widgets.destroy()


    def hold_img(self):
        self.clear_bodyScreen()
        # initial hold image
        appBodyimg = Image.open(holdImg)
        appBodyimg = appBodyimg.resize((bodySizeX, bodySizeY), Image.ANTIALIAS)
        self.appBodyimg = ImageTk.PhotoImage(appBodyimg)

        self.bodyScreen.configure(image=self.appBodyimg)
        self.bodyScreen.update()


    def update_video_img(self, cam_image):
        # pass cam_image into label frame
        cam_image = cv2.cvtColor(cam_image, cv2.COLOR_BGR2RGB)
        cam_image_converted = Image.fromarray(cam_image)
        cam_image_converted = cam_image_converted.resize((bodySizeX, bodySizeY), Image.ANTIALIAS)

        self.cam_image_converted = ImageTk.PhotoImage(cam_image_converted)
        self.bodyScreen.configure(image=self.cam_image_converted)



