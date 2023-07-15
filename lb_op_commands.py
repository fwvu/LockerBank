import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import pickle
from pyzbar import pyzbar
import numpy as np

from lb_assets import *
import lb_firebase


###--- LOCKER CODE ---####

# creates the grid for locker state and adds the corresponding image
def locker_state(self):
    delete_img(self)
    self.clear_bodyScreen()
    
    # opens the current lockertest.dat file and adds it to a dictionary
    lockers = {}
    lockers = pickle.load(open('lockertest.dat', 'rb'))
    
    # welcome msg should be added to assests
    welcome_msg = "\n Welcome Back \n \n \n "

    # creates a label frame so grid can by used
    lockerMessage = tk.Label(self.bodyScreen, text=welcome_msg)
    lockerMessage.pack(side="top", fill="both", expand=True)

    lockerBank = tk.Label(self.bodyScreen)
    lockerBank.pack(side="top", fill="both", expand=True)
    
    locker_column = 0
    for key, value in lockers.items():
        # image resizer cos tkinter is a lil bitch when it comes to images
        locker_state_img = Image.open(f'{value}.png')
        locker_resizer = locker_state_img.resize((50, 75))
        resized_locker_img = ImageTk.PhotoImage(locker_resizer)
        # creates a label frame for each of the keys in lockertest.dat
        locker_label = tk.Label(lockerBank, text=key, image=resized_locker_img)
        # adds the resized image taken from value in lockertest.dat
        locker_label.image = resized_locker_img
        locker_label.grid(row=0,column=locker_column, padx=20, pady=5 )
        # changes the value in lockertest.dat
        if value == "avail":
            chosenLocker = key
            lockers[key] = "full"
            pickle.dump(lockers, open('lockertest.dat', 'wb'))

        locker_column += 1

    lockerAssignMessage = tk.Label(self.bodyScreen, text="\nYour assigned locker is:\n\n" + chosenLocker + "\n\nHave a nice day.\n\n", font=("Arial", 25))
    lockerAssignMessage.pack(side="top", fill="both", expand=True)

    # passes userID and chosen locker to firebase fuction
    lb_firebase.firebase_deposit(userId, chosenLocker)
    

# cycles through the saved file "lockertest.dat" and change the first empty value to avail   
def locker_select(self):
    lockers = pickle.load(open('lockertest.dat', 'rb'))
    for key, value in lockers.items():
        if value == "empty":
            lockers[key] = "avail"
            pickle.dump(lockers, open('lockertest.dat', 'wb'))
            break
    locker_state(self)

# locker reset function
def locker_reset(self):  
    lockers = {}
    for lockerNumber in range(lockerTotal):
        lockerNumber += 1
        lockers.update({"locker " + str(lockerNumber) : "empty"})
    pickle.dump(lockers, open('lockertest.dat', 'wb'))
    print(lockers)
    close_cam(self)

###--- PI CODE ---###

def pi_open_locker():
    pass


###--- CAMERA CODE ---###

# Opens camera 
def open_cam(self):
    delete_img(self)
    self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    update_video(self)

# Checks for active camera then adds the QR scanner
def update_video(self):
    if self.cam is not None:
        ret, cam_image = self.cam.read()

        if ret == True:
            # The method to read the QR code by detecting the bounding box coords and decoding the hidden QR data 
            gray_image = cv2.cvtColor(cam_image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
            self.detector = pyzbar.decode(gray_image)
            
            if self.detector:
                for qr_code in self.detector:
                    data = qr_code.data.decode('utf-8')
                    pts = np.array([qr_code.polygon], np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(cam_image, [pts], True, (255, 100, 5), 2)
                    cv2.putText(cam_image, data, (50, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 100, 5), 2)

                if data:
                    # splits the qr code data
                    processedData = data.split()               
                    # check the first part of the QR code contains food_for_dirt
                    if processedData[0] == "Food_For_Dirt":
                        # creates a global userID so it can be passed when locker is selected
                        global userId
                        userId = processedData[1] 
                        # triggers locker select function
                        locker_select(self) 
                    # if the QR decodes Maintenance it will perform a locker reset
                    elif processedData[0] == "Food_For_Dirt_Maintenance":                        
                        locker_reset(self)

            # continually passes images to the bodyScreen frame to create video 
            self.update_video_img(cam_image)
            self.bodyScreen.after(frameRate, lambda: update_video(self))


# stops and releases camera
def delete_img(self):
    self.clear_bodyScreen()
    if self.cam is not None:
        self.cam.release()
        self.cam = None

# stops and releases camera REMOVE WHEN REMOVING TESTING BUTTONS
def close_cam(self):
    if self.cam is not None:
        self.cam.release()
        self.cam = None   
    self.clear_bodyScreen()
    self.hold_img()




