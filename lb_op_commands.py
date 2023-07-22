import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import pickle
from pyzbar import pyzbar
import numpy as np
#from gpiozero import AngularServo
from time import sleep

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
    pi_open_locker(chosenLocker)
    

# cycles through the saved file "lockertest.dat" and change the first empty value to avail   
def locker_select(self):
    lockers = pickle.load(open('lockertest.dat', 'rb'))
    found_empty = False
    # TEST ON PI - chosenLocker = None

    for key, value in lockers.items():
        if value == "empty":
            lockers[key] = "avail"
            found_empty = True
            break

    if found_empty:
        pickle.dump(lockers, open('lockertest.dat', 'wb'))
        locker_state(self)
        # TEST ON PI - if chosenLocker:
        # TEST ON PI -     pi_open_locker(chosenLocker)
    else:
        lockers_full(self)

# All lockers full display
def lockers_full(self):
    delete_img(self)
    self.clear_bodyScreen()
    lockerMessage = tk.Label(self.bodyScreen, text="\nAll lockers are FULL\n\n Call maintenance\n\nHave a nice day.", font=("Arial", 25))
    lockerMessage.pack(side="top", fill="both", expand=True)


# locker reset function
def locker_reset(self):  
    lockers = {}
    for lockerNumber in range(lockerTotal):
        lockerNumber += 1
        lockers.update({"locker " + str(lockerNumber) : "empty"})
    pickle.dump(lockers, open('lockertest.dat', 'wb'))
    print(lockers)
    delete_img(self)
    self.clear_bodyScreen()
    
    # opens the current lockertest.dat file and adds it to a dictionary
    lockers = {}
    lockers = pickle.load(open('lockertest.dat', 'rb'))
    
    # reset msg should be added to assests
    reset_msg = "\n Lockers Reset \n \n \n "

    # creates a label frame so grid can by used
    lockerMessage = tk.Label(self.bodyScreen, text=reset_msg)
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
        locker_column += 1

    lockerAssignMessage = tk.Label(self.bodyScreen, text="\nAll lockers are reset to empty\n\n Have a nice day.", font=("Arial", 25))
    lockerAssignMessage.pack(side="top", fill="both", expand=True)


###--- PI CODE ---###

def pi_open_locker(locker):
    _lockerNum = locker.split()
    lockerNum = _lockerNum[1]
    # can alter lockerNum to match used GPIO pin
    print(lockerNum)
    # hardset to 15 for testing because we only have 1 servo
    lockerNum = 15

            # call      # GPIO      # start freq          # stop freq
    servo = AngularServo(lockerNum, min_pulse_width=minpw, max_pulse_width=maxpw)

    servo.angle = 0
    sleep(2)
    servo.angle = -90
    sleep(2)

    #restart_full(self)
    
def pi_close_locker(self):
    lockerNum = 15

            # call      # GPIO      # start freq          # stop freq
    servo = AngularServo(lockerNum, min_pulse_width=minpw, max_pulse_width=maxpw)

    servo.angle = -90
    sleep(2)
    servo.angle = 0
    sleep(2)


###--- CAMERA CODE ---###

# Opens camera 
def open_cam(self):
    delete_img(self)
    self.cam = cv2.VideoCapture(0)
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
                    if processedData[0] == qrId:
                        # creates a global userID so it can be passed when locker is selected
                        global userId
                        userId = processedData[1] 
                        # triggers locker select function
                        locker_select(self)
                        #valid_user(self)
                    # if the QR decodes Maintenance it will perform a locker reset
                    elif processedData[0] == maintenanceId:                        
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

def restart_full(self):
    close_cam(self)
    sleep(1)
    open_cam(self)


# Function to automate process
def valid_user(self):
    self.after(1000, locker_select, self)
    self.after(2000, locker_state, self)
    self.after(3000, lb_firebase.firebase_deposit, userId, chosenLocker)
    self.after(4000, pi_open_locker, chosenLocker)
