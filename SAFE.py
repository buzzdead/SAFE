import tkinter as tk

import RSA
import ScreenShot


class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a prompt, an input box, an output label,
        # and a button to do the computation
        #self.prompt = tk.Label(self, text="Enter a number:", anchor="w")
        #self.entry = tk.Entry(self)
        self.submit = tk.Button(self, text="Take Screenshot", command = self.calculate)
        self.output = tk.Label(self, text="")

        # lay the widgets out on the screen.
        #self.prompt.pack(side="top", fill="x")
        #self.entry.pack(side="top", fill="x", padx=20)
        self.output.pack(side="top", fill="x", expand=True)
        self.submit.pack(side="right")


    def calculate(self):
        root.withdraw()
        ScreenShot.activateScreenShot()
        pubkey, privkey = RSA.get_rsa_keys()
        ctxt = RSA.rsa_encrypt2("saved.png", pubkey)
        fd = open("encrypted", "wb")
        fd.write(ctxt)
        fd.close()

        fd = open("encrypted", "rb")
        ctxt2 = fd.read()
        fd.close()
        RSA.rsa_decrypt2(ctxt2, privkey)
        root.update()
        root.deiconify()

# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()