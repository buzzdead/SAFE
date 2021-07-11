# Import the required Libraries
from tkinter import *
from tkinter import ttk

import Commands as cmd


# Create an instance of Tkinter frame
win = Tk()
# Set the geometry of the Tkinter frame
win.geometry("750x250")


# Create an Entry Widget
# Create Multiple Buttons with different commands

def take_screenshot():
    win.withdraw()
    cmd.take_screenshot()
    win.update()
    win.deiconify()


button_dict = {}
option = {"Take Screenshot": take_screenshot, "Generate Keys": cmd.generate_keys, "Decrypt File": cmd.decrypt_file}

for i, k in option.items():
    button_dict[i] = ttk.Button(win, text=i, command=k)
    button_dict[i].pack()

win.mainloop()
