import tkinter as tk
import datetime
import os

class GUI:
    def __init__(self, master):
        self.master = master
        master.title = 'Folderki'

        self.input_label = tk.Label(text='Numer pierwszego folderu')
        self.input_label.grid(row=0, column=0)

        self.input = tk.Entry()
        self.input.grid(row=0, column=1)

        self.button_3d = tk.Button(text='3D', command=lambda : self.make_dir('3D'))
        self.button_3d.grid(row=1, column=0)

        self.button_rel = tk.Button(text='RELIABILITY', command=lambda : self.make_dir('RELIBILITY'))
        self.button_rel.grid(row=1, column=1)

        self.button_ok = tk.Button(text='OK')
        self.button_ok.grid(row=2, columnspan=2)

        self.button_conifg = tk.Button(text='Wyjście', command=master.destroy)
        self.button_conifg.grid(row=3, columnspan=2)

    def make_dir(self, target):
        year = datetime.datetime.now().year
        f = int(self.input.get())
        l = f + 19
        firstDir = self._check_dir(f)
        lastDir = self._check_dir(l)
        
        path = "I:\\AG\\ag\\Quality\\Laboratory\\{}{}/{} - {}\\".format(target, year, firstDir, lastDir)

        for i in range(f, l + 1):
            currentDir = self._check_dir(i)
            cmd = "md \"{}{}\"".format(path,currentDir)
            os.system(cmd)

    def _check_dir(self, dirNumber):
        res = dirNumber
        tmp = dirNumber / 10
        if tmp < 1:
            res = "000{}".format(dirNumber)
            return res
        if 1 <= tmp < 10:
            res = "00{}".format(dirNumber)
            return res

        if 10 <= tmp < 100:
            res = "0{}".format(dirNumber)
            return res
        
        return res
        

root = tk.Tk()

app = GUI(root)
root.mainloop()