# Import the required Libraries
import fnmatch
import os
from tkinter import *
from tkinter import filedialog

import Commands as cmd

# Create an instance of Tkinter frame
win = Tk()
# Set the geometry of the Tkinter frame
win.geometry("750x250")


def submitForm():
    strFile = optVariable.get()
    # Print the selected value from Option (Combo Box)
    if strFile != '':
        print('Selected Value is : ' + strFile)
    cmd.decrypt_file(strFile)


label_2 = Label(win, text="Choose Files ", width=20, font=("bold", 10))
label_2.place(x=68, y=250)

flist = fnmatch.filter(os.listdir('./encrypted_files'), '*.enc')
optVariable = StringVar(win)
optVariable.set("   Select   ")  # default value
optFiles = OptionMenu(win, optVariable, None, *flist)
optFiles.pack()
optFiles.place(x=0, y=40)

Button(win, text='Decrypt file', command=submitForm, width=20, bg='brown', fg='white').place(x=0, y=0)


def take_screenshot():
    win.withdraw()
    cmd.take_screenshot()
    win.update()
    win.deiconify()
    path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=(("enc file", "*.enc"),))
    cmd.encrypt_file(path)


button_dict = {}
option = {"Take Screenshot": take_screenshot, "Generate Keys": cmd.generate_keys}

for i, k in option.items():
    button_dict[i] = Button(win, text=i, command=k)
    button_dict[i].pack()

win.mainloop()
