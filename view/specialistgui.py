import tkinter as tk
from view.specialist.specialistform import SpecialistForm


class SpecialistGUI(tk.Frame):
    """ Frame, ami tartalmazza az összes megjelenítendő elemet.
    """
    def __init__(self, parent):
        """ Betölti máshonnan a kirakandó frame-eket és egyetlen közös frame-be rakja össze.
        """ 
        super().__init__(parent)

        # A főprogram mondja meg később, hogy mivel kommunikálunk        
        self.ctrl = None                    

        # Framek, amiből a GUI áll
        self.form = SpecialistForm(self)

        self.form.pack()


    def set_controller(self, ctrl):
        """ Ha esemény lesz, ebben az objektumban vannak a metódusok, amit majd meghív.

        Amikor a GUI-ban valamilyen esemény van (pl. gombnyomás), akkor ebben az 
        objektumban (a Controllerben) lévő metódust hívja meg.

        Továbbadja a Controller objektumokat azok felé az összetevői felé, amiből ez
        a GUI áll.

        ctrl (HibabejelentoCtrl): ebben az objektumban vannak a meghívandó metódusok.
        """ 
        self.ctrl = ctrl
        self.form.set_controller(self.ctrl)       


    def set_ticket_id(self, value):
        """ A megjelenített ticket azonosítót beállítja (azt tartalmazó összetevőt meghívja)."""
        self.form.set_ticket_id(value)


    def set_user_id(self, value):
        """ A megjelenített user azonosítóját beállítja (azt tartalmazó összetevőt meghívja)."""
        self.form.set_user_id(value)


    def set_problem(self, value):
        """ A megjelenített problémát kiírja (azt tartalmazó összetevőt meghívja)."""
        self.form.set_problem(value)


    def clear_form(self):
        """ Az összes megjelenített adatot törli. (azt tartalmazó összetevőt meghívja)."""
        self.form.clear_form()



    def enable_btn_lezarva(self):
        """ Form beküldését engedélyező gomb használható. (azt tartalmazó összetevőt meghívja)"""
        self.form.enable_btn_lezarva()


    def disable_btn_lezarva(self):
        """ Form beküldését engedélyező gomb nem használható. (azt tartalmazó összetevőt meghívja)"""
        self.form.disable_btn_lezarva()


    def enable_btn_get_next_job(self):
        """ Következő munkát lekérő gomb használható. (azt tartalmazó összetevőt meghívja)"""
        self.form.enable_btn_get_next_job()


    def disable_btn_get_next_job(self):
        """ Következő munkát lekérő gomb nem használható. (azt tartalmazó összetevőt meghívja)"""
        self.form.disable_btn_get_next_job()


    def get_ticket_id(self):
        """ Visszaadja a GUI-ban látható egyedi hibajegy-azonosítót

        Return:
            str: a hibajegy azonosítója (ticket_id)
                 egy GUI-t alkotó összetevőben van ez az adat, attól kérdezi le, majd adja vissza.
        """
        return self.form.get_ticket_id()


    def get_user_id(self):
        """ Visszaadja a GUI-ban látható azonosítót, hogy ki jelentette be a hibát

        Return:
            str: a hibát bejelentő felhasználó azonosítója (user_id)
                 egy GUI-t alkotó összetevőben van ez az adat, attól kérdezi le, majd adja vissza.
        """
        return self.form.get_user_id()


    def get_problem(self):
        """ Visszaadja a GUI-ban látható leírást, hogy mi a probléma

        Return:
            str: a probléma leírása (problem)
                 egy GUI-t alkotó összetevőben van ez az adat, attól kérdezi le, majd adja vissza.
        """
        return self.form.get_problem()


    def set_employee_working(self, value):
        """ Beállítjuk, hogy az ügyintéző épp dolgozik-e valamin
        
        Parameter:
            value (bool): True=dolgozik/foglalt, False=nem dolgozik/szabad
        """ 
        self.form.set_employee_working(value)


    def is_employee_working(self):
        """ Lekérdezzük, hogy az ügyintéző épp dolgozik-e valamin
        
        Return:
            boolean: True=dolgozik/foglalt, False=nem dolgozik/szabad
        """ 
        return self.form.is_employee_working() 

