import fnmatch
import os
from tkinter import *
from tkinter import filedialog, messagebox

import SAFE

import Commands as cmd

global rsa_key


class StorePass(object):
    def __init__(self, master, str_file):
        top = self.top = Toplevel(master)
        self.l = Label(top, text="Hello World")
        self.file = str_file
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        value = self.e.get()
        temp_file = open("files/temp.txt", 'wb')
        value = str(value).encode('utf-8')
        temp_file.write(value)
        temp_file.close()

        cmd.encrypt_file('files/temp.txt', 'encrypted_files/' + self.file, True)
        self.top.destroy()


class StorageList(object):
    def __init__(self, master):
        self.master = master
        self.flist = fnmatch.filter(os.listdir('./encrypted_files'), '*.enc')
        self.optVariable = StringVar(master)
        self.optVariable.set("Select secret")  # default value
        self.optFiles = OptionMenu(master, self.optVariable, *self.flist)
        self.optFiles.pack()
        self.optFiles.place(x=0, y=0)

        self.secretImage = PhotoImage(file='assets/clipboard.png').subsample(2, 2)
        self.storeImage = PhotoImage(file='assets/store.png').subsample(2, 2)

        self.b = Button(master, text="Store \n Password", image=self.storeImage,
                        compound=LEFT, bg='red', fg='black', command=self.store_pass, width=85, height=30).place(x=115,
                                                                                                                 y=0)

        self.rs = Button(self.master, text=' Retrieve \n Secret', image=self.secretImage,
                         compound=LEFT, command=self.retrieveSecret, width=75, height=30, bg='red', fg='black')
        self.rs.place(x=220, y=0)

    def store_pass(self):
        strFile = self.optVariable.get()
        self.w = StorePass(self.master, strFile)
        self.master.wait_window(self.w.top)

    def retrieveSecret(self):
        strFile = self.optVariable.get()
        rt = cmd.decrypt_file(strFile, False).decode('utf-8')
        root.clipboard_clear()
        root.clipboard_append(rt)


class Buttons(object):
    def __init__(self, master):
        self.master = master
        self.button_dict = {}
        self.option = {"   Take \n   Screenshot": self.take_screenshot,
                       "   Generate \n   Keys": cmd.generate_keys, "   Decrypt \n   file": self.decrypt}
        self.images = {"   Take \n   Screenshot": PhotoImage(file='assets/image.png').subsample(2, 2),
                       "   Generate \n   Keys": PhotoImage(file='assets/key.png').subsample(2, 2),
                       "   Decrypt \n   file": PhotoImage(file='assets/decrypt.png').subsample(2, 2)}
        abc = 0.75
        for i, k in self.option.items():
            self.button_dict[i] = Button(self.master, text=i, image=self.images[i],
                                         compound=LEFT, command=k, bg="purple", fg="white", height=40, width=150)
            self.button_dict[i].place(x=abc * 150 + abc * len(i), y=200)

            # self.button_dict[i].pack()
            abc += 1

    def take_screenshot(self):
        self.master.withdraw()
        cmd.take_screenshot()
        self.master.update()
        self.master.deiconify()
        path = filedialog.asksaveasfilename \
            (defaultextension=".enc", filetypes=(("enc file", "*.enc"),), initialdir='encrypted_files/')
        if not path:
            os.remove('files/saved.png')
            return
        remove_file = messagebox.askyesno("Alert", "Delete original picture?")
        cmd.encrypt_file('files/saved.png', path, remove_file)

    def decrypt(self):
        path = filedialog.askopenfile(initialdir='encrypted_files/')
        if not path:
            return
        filename = cmd.path_leaf(path.name)[0]
        cmd.decrypt_file(filename, True)


class MainWindow(object):
    def __init__(self, master):
        self.master = master
        self.storage = StorageList(self.master)
        self.buttons = Buttons(self.master)


if __name__ == "__main__":
    root = Tk()
    root.title("Screen and File Encryption")
    root.iconbitmap(r'assets/safe.ico')
    root.geometry("750x450")
    root.resizable(0, 0)
    bg = PhotoImage(file="assets/bg.png").subsample(4, 4)
    label1 = Label(root, image=bg)
    label1.place(x=0, y=0)
    m = MainWindow(root)
    key = cmd.activated('12345'.encode('utf-8'))
    if key:
        SAFE.rsa_key = key
    root.mainloop()
