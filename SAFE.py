import fnmatch
import os
from tkinter import *
from tkinter import filedialog
import pyperclip


import Commands as cmd


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
        rt = cmd.decrypt_file(strFile, False).decode('utf-8')
        pyperclip.copy(rt)
        spam = pyperclip.paste()
        print(spam)



class Buttons(object):
    def __init__(self, master):
        self.master = master
        self.button_dict = {}
        self.option = {"Take Screenshot": self.take_screenshot,
                       "Generate Keys": cmd.generate_keys, "Decrypt file": self.decrypt}

        for i, k in self.option.items():
            self.button_dict[i] = Button(self.master, text=i, command=k)
            self.button_dict[i].pack()

    def take_screenshot(self):
        self.master.withdraw()
        cmd.take_screenshot()
        self.master.update()
        self.master.deiconify()
        path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=(("enc file", "*.enc"),))
        cmd.encrypt_file('files/saved.png', path, True)

    def decrypt(self):
        path = filedialog.askopenfile().name
        filename = cmd.path_leaf(path)[0]
        cmd.decrypt_file(filename, True)


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
