import tkinter as tk
from view.hibabejelento.hibabejelentoform import HibabejelentoForm
from view.hibabejelento.gombok import Gombok
from model.ticket import Ticket

class HibabejelentoGUI(tk.Frame):
    """ Frame, ami tartalmazza az összes megjelenítendő elemet.
    """
    def __init__(self, parent):
        """ Betölti máshonnan a kirakandó frame-eket és egyetlen közös frame-be rakja össze.
        """ 
        super().__init__(parent)

        # később adjuk meg, hogy melyik controllerhez tartozik  
        self.ctrl = None                    

        # Framek, amiből a GUI áll
        self.form = HibabejelentoForm(self)
        self.btns = Gombok(self)
        self.form.pack()
        self.btns.pack()


    def set_controller(self, ctrl):
        """ Ha esemény lesz, ebben az objektumban vannak a metódusok, amit majd meghív.

        Amikor a GUI-ban valamilyen esemény van (pl. gombnyomás), akkor ebben az 
        objektumban (a Controllerben) lévő metódust hívja meg.

        Továbbadja a Controller objektumokat azok felé az összetevői felé, amiből ez
        a GUI áll.

        ctrl (HibabejelentoCtrl): ebben az objektumban vannak a meghívandó metódusok.
        """ 
        self.ctrl = ctrl
        self.btns.set_controller(self.ctrl)       


    def get_ticket_state(self):
        """ Mi a ticket állapota? Továbbkérdezi azt az összetevőjét, amiben ez benne van.
        Return:
            int: a hibajegy jelenlegi állapota (lezárva/folyamatban/kinek kell továbbküldeni)
                 egy GUI-t alkotó összetevőben van ez az adat, attól kérdezi le, majd adja vissza.
        """
        return self.btns.get_ticket_state()


    def get_user_id(self):
        """ Ki jelentette be a hibát? Továbbkérdezi azt az összetevőjét, amiben ez benne van.
        Return:
            str: a hibát bejelentő felhasználó azonosítója
                 egy GUI-t alkotó összetevőben van ez az adat, attól kérdezi le, majd adja vissza.
        """
        return self.form.get_user_id()


    def get_problem(self):
        """ Mi volt a hiba leírása? Továbbkérdezi azt az összetevőjét, amiben ez benne van.
        Return:
            str: a probléma leírása
                 egy GUI-t alkotó összetevőben van ez az adat, attól kérdezi le, majd adja vissza.
        """
        return self.form.get_problem()


    def clear_form(self):
        """ Töröljük a form (a gui egyik összetevőjének) a tartalmát """
        self.form.clear_form()


    def clear_buttons_state(self):
        """ Radiobuttonokat alaphelyzetbe állítja (a gui egyik összetevőjében vannak)"""
        self.btns.clear_buttons_state()
