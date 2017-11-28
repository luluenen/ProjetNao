import sys
from Tkinter import *

class NaoGUI():
    values = None

    def __init__(self):
        self.loginGUI = Tk()
        self.loginGUI.title("NaoMultimedia")
        self.login(self.loginGUI)

    def login(self, master):
        # Login window
        Label(master, text="IP").grid(row=0)
        Label(master, text="Port").grid(row=1)
        Label(master, text="Login").grid(row=2)
        Label(master, text="Mot de passe").grid(row=3)

        self.ip_entry = Entry(master)
        self.port_entry = Entry(master)
        self.login_entry = Entry(master)
        self.pwd_entry = Entry(master, show = "*", width=15)

        self.ip_entry.insert(END,'169.254.14.64')#'169.254.155.63'
        self.port_entry.insert(END, '9559')
        self.login_entry.insert(END, 'nao')
        self.pwd_entry.insert(END, 'nao')

        self.ip_entry.grid(row=0, column=1)
        self.port_entry.grid(row=1, column=1)
        self.login_entry.grid(row=2, column=1)
        self.pwd_entry.grid(row=3, column=1)

        Button(master, text='Quit', command=master.quit).grid(row=4, column=0, sticky=W, pady=4)
        self.connectionButton = Button(master, text='Se connecter', command=self.establishConnection)
        self.connectionButton.grid(row=4, column=1, sticky=W, pady=4)
        mainloop( )

    def establishConnection(self):
        self.connectionButton.config(state = 'disabled')
        self.values = {"ip": self.ip_entry.get(),
                       "port": int(self.port_entry.get()),
                       "login": self.login_entry.get(),
                       "password": self.pwd_entry.get()}
        self.quit()

    def quit(self):
        self.loginGUI.destroy()

if __name__ == "__main__":
    gui = NaoGUI()
    print gui.values
