import tkinter as tk
from tkinter import ttk
import pickle

from lb_assets import *

def locker_state(self):

    pass

def locker_reset(self):  
    lockers = {}
    for lockerNumber in range(lockerTotal):
        lockerNumber += 1
        lockers.update({"locker " + str(lockerNumber) : "empty"})
    pickle.dump(lockers, open('lockertest.dat', 'wb'))
    print(lockers)


