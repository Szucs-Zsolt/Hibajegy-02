import tkinter as tk
import tkinter.messagebox as mb
from view.hibabejelentogui import HibabejelentoGUI
from control.hibabejelentoctrl import HibabejelentoCtrl
from model.databasehandler import DatabaseHandler


class Hibabejelento(tk.Tk):
    """ Hibabejelentés felvétele, lezárása, vagy továbbküldése.

    Az ügyfélszolgálat fogadja és felveszi a hibabejelentéseket.
    Ha tudja megoldja és lezárja a problémát.
    Ha nem tudja megoldani, akkor továbbküldi.
    """

    def __init__(self):
        """ Betölti az Model-View-Controller elemeit és összeköti azokat egymással """

        super().__init__()
        self.title("Hibabejelentés")
        self.state("zoomed")

        # View (GUI): tk.Frame, ezért tudnia kell a parentet
        self.gui = HibabejelentoGUI(self)      

        # Controller (Logic): az itt lévő close_program() meghívásával zárja be a programot.
        self.ctrl= HibabejelentoCtrl(self)     # Logic 

        # Model (Database): előkészítjük a későbbi használatra
        try:
            self.db  = DatabaseHandler()       
            self.db.create_database_if_not_exists() 
        except:
            mb.showerror("HIBA!", "Nem sikerült megnyitni az adatbázist!")
            exit(1)

        # GUI-nak, hogy tudja: az eseményei a Controller-ben lévő metódusokat hívják meg
        self.gui.set_controller(self.ctrl)     

        # Controller, hogy tudja melyik GUI-ból vegye ki a beírt adatokat
        self.ctrl.set_gui(self.gui)            
        # Controller, hogy ezen keresztül írja/olvassa a lemezen lévő adatbázist
        self.ctrl.set_db(self.db)              

        self.gui.pack()


    def close_program(self):
        """ HibabejelentoCtrl hívja meg, hogy bezárja a programot. """
        self.destroy()


if __name__ == "__main__":
    app = Hibabejelento()
    app.mainloop()

