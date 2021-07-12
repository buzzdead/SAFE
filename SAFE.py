import fnmatch
import os
from tkinter import *
from tkinter import filedialog

import Commands as cmd


class StorePass(object):
    def __init__(self, master, str_file):
        top = self.top = Toplevel(master)
        self.l = Label(top, text="Hello World")
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()
        self.str_file = str_file

    def cleanup(self):
        value = self.e.get()
        fd = open("files/secret_pass.txt", 'w')
        fd.write(value)
        cmd.encrypt_file(fd)
        fd.close()
        os.remove(fd)
        self.top.destroy()


class StorageList(object):
    def __init__(self, master):
        self.master = master
        self.flist = fnmatch.filter(os.listdir('./encrypted_files'), '*.enc')
        self.optVariable = StringVar(master)
        self.optVariable.set("   Select   ")  # default value
        self.optFiles = OptionMenu(master, self.optVariable, *self.flist)
        self.optFiles.pack()
        self.optFiles.place(x=0, y=0)

        self.b = Button(master, text="Store Password", command=self.store_pass).place(x=100, y=0)
        self.rs = Button(self.master, text='Retrieve Secret', command=self.retrieveSecret,
                         width=10, bg='brown', fg='white').place(x=0, y=40)

    def store_pass(self):
        strFile = self.optVariable.get()
        self.w = StorePass(self.master, strFile)
        self.master.wait_window(self.w.top)

    def retrieveSecret(self):
        strFile = self.optVariable.get()
        cmd.decrypt_file(strFile)


class Buttons(object):
    def __init__(self, master):
        self.master = master
        self.button_dict = {}
        self.option = {"Take Screenshot": self.take_screenshot, "Generate Keys": cmd.generate_keys}

        for i, k in self.option.items():
            self.button_dict[i] = Button(self.master, text=i, command=k)
            self.button_dict[i].pack()

    def take_screenshot(self):
        self.master.withdraw()
        cmd.take_screenshot()
        self.master.update()
        self.master.deiconify()
        path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=(("enc file", "*.enc"),))
        cmd.encrypt_file(path)


class MainWindow(object):
    def __init__(self, master):
        self.master = master
        self.storage = StorageList(self.master)
        self.buttons = Buttons(self.master)


if __name__ == "__main__":
    root = Tk()
    root.geometry("750x250")
    m = MainWindow(root)
    root.mainloop()
