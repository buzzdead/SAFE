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
        top.resizable(0, 0)
        self.l = Label(top, text="Enter your secret")
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


class AddSecret(object):
    def __init__(self, master, optFiles, optVariable):
        top = self.top = Toplevel(master)
        top.resizable(0, 0)
        self.master = master
        self.l = Label(top, text="Type a name for the file to the secret here.")
        self.optFiles = optFiles
        self.optVariable = optVariable
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        value = self.e.get()
        fd = open('encrypted_files/' + value + '.enc', 'w')
        fd.close()
        self.optFiles["menu"].add_command(
            label=value + '.enc', command=lambda st=value: self.optVariable.set(value + '.enc'))
        self.top.destroy()


class StorageList(object):
    def __init__(self, master):
        self.master = master
        self.flist = fnmatch.filter(os.listdir('./encrypted_files'), '*.enc')
        self.optVariable = StringVar(master)
        self.optVariable.set("Select secret")  # default value
        self.optFiles = OptionMenu(master, self.optVariable, *self.flist)
        self.optFiles.config(bg='blue', fg='white', width='38')
        self.optFiles["menu"].config(bg='blue', fg='white')
        self.optFiles.pack()
        self.optFiles.place(x=250, y=40)

        self.secretImage = PhotoImage(file='assets/clipboard.png').subsample(2, 2)
        self.storeImage = PhotoImage(file='assets/store.png').subsample(2, 2)

        self.s = Button(master, text="Store \n Secret", image=self.storeImage,
                        compound=LEFT, bg='grey', fg='white', command=self.store_pass, width=85, height=30).place(x=250,
                                                                                                                  y=0)

        self.rs = Button(self.master, text=' Retrieve \n Secret', image=self.secretImage,
                         compound=LEFT, command=self.retrieveSecret, width=85, height=30, bg='grey', fg='white')
        self.rs.place(x=340, y=0)

        self.ns = Button(master, text="Add \n Secret", image=self.storeImage,
                         compound=LEFT, bg='grey', fg='white', command=self.add_secret, width=85, height=30).place(
            x=430,
            y=0)

    def store_pass(self):
        strFile = self.optVariable.get()
        self.w = StorePass(self.master, strFile)
        self.master.wait_window(self.w.top)

    def add_secret(self):
        elements = os.listdir('./encrypted_files')
        if len(elements) >= 10:
            messagebox.showerror("Alert", "Maximum Secrets Reached")
            return
        self.w = AddSecret(self.master, self.optFiles, self.optVariable)
        self.master.wait_window(self.w.top)

    def retrieveSecret(self):
        strFile = self.optVariable.get()
        rt = cmd.decrypt_file(strFile, False).decode('utf-8')
        root.clipboard_clear()
        root.clipboard_append(rt)


class Buttons(object):
    def __init__(self, master, storage):
        self.master = master
        self.button_dict = {}
        self.storage = storage
        self.ebimage = PhotoImage(file='assets/encrypt.png').subsample(2, 2)
        self.eb = Button(self.master, text='   Encrypt \n   file',
                         image=self.ebimage, compound=LEFT,
                         command=self.encrypt, bg="light blue", fg="black",
                         font='Helvetica 12 bold', height=35, width=150).place(x=296, y=270)
        self.option = {"   Take \n   Screenshot": self.take_screenshot,
                       "   Decrypt \n   file": self.decrypt,
                       "   Generate \n   Keys": cmd.generate_keys}
        self.images = {"   Take \n   Screenshot": PhotoImage(file='assets/image.png').subsample(2, 2),
                       "   Generate \n   Keys": PhotoImage(file='assets/key.png').subsample(2, 2),
                       "   Decrypt \n   file": PhotoImage(file='assets/decrypt.png').subsample(2, 2)}
        abc = 0.75
        for i, k in self.option.items():
            self.button_dict[i] = Button(self.master, text=i, image=self.images[i],
                                         compound=LEFT, command=k, bg="light blue", fg="black",
                                         font='Helvetica 12 bold', height=35, width=150)
            self.button_dict[i].place(x=abc * 150 + abc * len(i), y=330)
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
        fn = cmd.path_leaf(path)[0]
        self.storage.optFiles["menu"].add_command(
            label=fn, command=lambda st=path: self.storage.optVariable.set(fn))
        cmd.encrypt_file('files/saved.png', path, remove_file)

    def decrypt(self):
        path = filedialog.askopenfile(initialdir='encrypted_files/')
        if not path:
            return
        filename = cmd.path_leaf(path.name)[0]
        cmd.decrypt_file(filename, True)

    def encrypt(self):
        path = filedialog.askopenfile(initialdir='files/')
        pathname = path.name
        path.close()
        if not path:
            return
        cmd.encrypt_file(pathname, 'encrypted_files/new_encrypted.enc', True)


class MainWindow(object):
    def __init__(self, master):
        self.master = master
        self.storage = StorageList(self.master)
        self.buttons = Buttons(self.master, self.storage)


if __name__ == "__main__":
    root = Tk()
    root.title("Screen and File Encryption")
    root.iconbitmap(r'assets/safe.ico')
    root.geometry("750x450")
    root.resizable(0, 0)
    bg = PhotoImage(file="assets/bg.png").subsample(4, 4)
    label1 = Label(root, image=bg)
    label1.place(x=-2, y=-2)
    m = MainWindow(root)
    key = cmd.activated('12345'.encode('utf-8'))
    if key:
        SAFE.rsa_key = key
    root.mainloop()
