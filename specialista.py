import tkinter as tk
import tkinter.messagebox as mb
from model.ticket import Ticket
from model.databasehandler import DatabaseHandler
from view.specialistgui import SpecialistGUI
from control.specialistctrl import SpecialistCtrl


# Milyen típusú hibákat kezelünk
PROBLEM_TYPE = Ticket.TECHNEK_KULD


class Specialista(tk.Tk):
    """ Ha a problémát az ügyfélszolgálat továbbküldta, akkor mi fogjuk kezelni.

    Ha a hibajegy felvétele során az ügyfélszolgálat nem tudta lezárni a 
    hibajegyet, és továbbküldte, hogy egy adott típusú specialista foglalkozzon
    vele, akkor azt a hibát itt fogjuk lekérdezni és lezárni.
    """
    def __init__(self):
        """ Betölti az Model-View-Controller elemeit és összeköti azokat egymással """

        super().__init__()
       
        self.title("Specialista")
        self.state("zoomed")

        # Milyen típusú problémát tud megoldani ez a specialista  
        self.problem_type = PROBLEM_TYPE

        # View (GUI): tk.Frame, ezért tudnia kell a parentet
        self.gui = SpecialistGUI(self)

        # Controller (Logic): az itt lévő close_program() meghívásával zárja be a programot.       
        # Megtudja, hogy milyen típusú problémákat kezeljen (a többit típusút nem)
        self.ctrl= SpecialistCtrl(self, self.problem_type) 

        # Model (Database): ez kezeli (és létezik egyáltalán a file?)
        try:
            self.db  = DatabaseHandler()       
        except:
            mb.showerror("HIBA!", "Nem sikerült megnyitni az adatbázist!")
            exit(1)

        # GUI-nak, hogy tudja, hogy az eseményei a Controller-ben lévő metódusokat hívják meg
        self.gui.set_controller(self.ctrl)     	

        # Controller, hogy tudja melyik GUI-ból vegye ki a beírt adatokat
        self.ctrl.set_gui(self.gui) 
        # Controller, hogy ezen keresztül írja/olvassa a lemezen lévő adatbázist
        self.ctrl.set_db(self.db)              	

        self.gui.pack()

        # Miután már mindent kiraktunk és összekötöttünk és minden a helyén van,
        # Controller elkezdi ellenőrizni az adatbázist, hogy van-e várakozó hibajegy
        self.ctrl.start_check_for_tickets_thread() 


    def close_program(self):
        """ SpecialistaCtrl hívja meg, hogy bezárja a programot. """
        self.destroy()


if __name__ == "__main__":
    app = Specialista()
    app.mainloop()

