import tkinter as tk
from tkinter.messagebox import showinfo
import sys
import pickle

from lb_assets import *

class menu_bar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        # sets up the menu bar
        
        # File menu
        file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)


        # Edit menu
        edit_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Settings", command=self.open_options)
        edit_menu.add_separator()
        edit_menu.add_command(label="Default")


        # Help menu
        help_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="No help here lol", command=self.no_help_window)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.about_window)
    
    def quit(self):
        sys.exit(0)

    def no_help_window(self):
        showinfo("No help", "I told you, \nNO HELP HERE")

    def about_window(self):
        about = tk.Toplevel()
        about.title('About')

        about_label = tk.Label(about, text="I am AWESOME")
        about_label.grid(row=0,column=0,padx=10,pady=10)

        about_button = tk.Button(about, text="Agree", command=about.destroy)
        about_button.grid(row=1,column=0,padx=10,pady=10,ipadx=10,ipady=10)

    def open_options(self):
        options_window = tk.Toplevel()
        options_window.title('Options')

        # Create labels and entry fields for each constant
        frame_rate_label = tk.Label(options_window, text="Frame Rate:")
        frame_rate_label.grid(row=0, column=0, padx=10, pady=10)
        frame_rate_entry = tk.Entry(options_window)
        frame_rate_entry.grid(row=0, column=1, padx=10, pady=10)
        frame_rate_entry.insert(0, frameRate)

        num_lockers_label = tk.Label(options_window, text="Number of lockers:")
        num_lockers_label.grid(row=1, column=0, padx=10, pady=10)
        num_lockers_entry = tk.Entry(options_window)
        num_lockers_entry.grid(row=1, column=1, padx=10, pady=10)
        num_lockers_entry.insert(0, lockerTotal)

        # Create a button to save the changes
        save_button = tk.Button(options_window, text="Save", command=lambda: self.save_options(options_window, frame_rate_entry.get(), num_lockers_entry.get()))
        save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10)

    def save_options(self, options_window, new_frame_rate, new_num_lockers):
        global frameRate, lockerTotal
        frameRate = new_frame_rate
        lockerTotal = new_num_lockers
        options_window.destroy()