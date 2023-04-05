import tkinter as tk
from view.font import FONT


class SpecialistForm(tk.Frame):
    """ Frame, amiben megjelenítjük és kezeljük egy hibajegy adatait.
    """

    def __init__(self, parent):
        """ Megjeleníti a vizuális elemeket a hibajegy adataival + eseményeket meghívó gombok.

        Parameter:
            parent: mibe rakjuk ki ezt a frame-et
        """

        super().__init__(parent)

        # Ezzel jelezzük, hogy az ügyintéző foglalt / dolgozik egy hibajegyen
        self.employee_working = False 

        # Még nincs kontroller hozzárendelve
        self.ctrl = None     

        # A hibabejelentő által rögzített adatok, amiket NEM lehet itt megváltoztatni
        # (a hibajegy egyedi azonosítója és hogy ki jelentette be a hibát) 
        self.ticket_id = tk.StringVar()
        self.user_id = tk.StringVar()

        lbl_ticket_id = tk.Label(self, text="Hibajegy száma:", font=FONT) 
        lbl_user_id = tk.Label(self, text="Ügyfélazonosító:", font=FONT)
        lbl_problem = tk.Label(self, text="A hiba leírása:", font=FONT) 

        # Ezeket nem lehet megváltoztatni: marad, ahogy az ügyfélszolgálat eredetileg rögzítette
        # (a hibajegy száma és a bejelentő azonosítója)
        self.ent_ticket_id = tk.Entry(self, textvar=self.ticket_id, font=FONT, state="disabled")  
        self.ent_user_id = tk.Entry(self, textvar=self.user_id, font=FONT, state="disabled") 


        # A probléma leírását meg lehet változtatni / hozzá lehet írni
        self.ent_problem = tk.Text(self, width=80, height=20, font=FONT)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.ent_problem.yview) 
        self.ent_problem.config(yscrollcommand=self.scrollbar.set)


        # Két lehetséges esemény (gomb): 
        # 1. Lekérjük a következő munkát (később rendeljük hozzá a meghívandó metódust)
        self.btn_get_next_job = tk.Button(self, text="Következő munka lekérése", font=FONT)
        # 2. Lezárjuk és beküldjük az aktuális munkát (kezdetben nem dolgozunk semmin=nem aktív)
        self.btn_lezarva = tk.Button(self, text="Lezárva", font=FONT)
        self.disable_btn_lezarva()            

        # Elemek kirakása          
        lbl_ticket_id.grid(row=1, column=1)
        self.ent_ticket_id.grid(row=1, column=2)
        lbl_user_id.grid(row=1, column=3)
        self.ent_user_id.grid(row=1, column=4)

        self.ent_problem.grid(row=2, column=1, columnspan=4)        
        self.scrollbar.grid(row=2, column=5, sticky="nws")


        self.btn_get_next_job.grid(row=3, column=1, columnspan=2, sticky="we") 
        self.btn_lezarva.grid(row=3, column=3, columnspan=2, sticky="we")

        self.ent_problem.focus_set()



    def set_controller(self, ctrl):
        """ Beállítjuk, hogy hol vannak a meghívandó metódusok. A gombokhoz hozzárendeljük azokat.

        Miután tudjuk, hogy melyik objektummal kommunikálunk, a következő munkát lekérő és az
        aktuális hibajegyet lezáró gombhoz hozzárendeljük a metódusokat.

        Parameter:
            ctrl (SpecialistCtrl): ebben az objektumban vannak az események által meghívandó
                                   metódusok.
        """
        self.ctrl = ctrl
        self.btn_get_next_job.config(command=ctrl.get_next_job)
        self.btn_lezarva.config(command=ctrl.form_bekuldese)


    def set_employee_working(self, value):
        """ Beállítjuk, hogy az ügyintéző épp dolgozik/foglalt-e, vagy sem (True,False)

        Parameter:
            value (bool): False = nem dolgozik / szabad
                          True  = dolgozik / foglalt (nem fogjuk majd a háttérben ellenőrizni,
                          hogy van-e új munka számára, amíg nem lesz újra szabad)

        """
        self.employee_working = value


    def is_employee_working(self):
        """ Visszaadjuk, hogy jelenleg dolgozik-e az ügyintéző.

        Return:
            boolean: False = nem dolgozik/szabad,   True=dolgozik/foglalt 
        """
        return self.employee_working 
 

 
    def set_ticket_id(self, value):
        """ Megjelenítjük a hibajegy egyedi azonosítóját.
 
        Parameter:
            value (str): a hibajegy egyedi azonosítója
        """ 
        self.ticket_id.set(value)
    def set_user_id(self, value):
        """ Megjelenítjük a hibát bejelentő felhasználó azonosítóját.
 
        Parameter:
            value (str): a hibát bejelentő felhasználó azonosítója
        """ 
        self.user_id.set(value)   

    def set_problem(self, value):
        """ Megjelenítjük a probléma leírását.
 
        Parameter:
            value (str): a probléma leírása
        """ 
        self.ent_problem.delete("1.0", tk.END)
        self.ent_problem.insert(tk.END, value)


    def clear_form(self):
        """ Minden megjelenített elem tartalmának törlése. Tiszta lappal kezdünk újra.
        """
        self.ticket_id.set("")
        self.user_id.set("")
        self.ent_problem.delete("1.0", tk.END)  


    def get_ticket_id(self):
        """ Visszaadjuk a képernyőn látható: egyedi hibajegy azonosítót.
 
        Return:
            string: egyedi hibajegy azonosító
        """ 
        return self.ticket_id.get()

    def get_user_id(self):
        """ Visszaadjuk a képernyőn látható: hibabejelentést tevő azonosítóját.
 
        Return:
            string: a hibabejelentést tevő azonosítója
        """ 
        return self.user_id.get()

    def get_problem(self):
        """ Visszaadjuk a képernyőn látható: probléma leírását.
 
        Return:
            string: a probléma leírása
        """ 
        return self.ent_problem.get("1.0",tk.END)


    def disable_btn_lezarva(self):
        """ Letiltjuk a ticket lezárása (és beküldése) gombot."""
        self.btn_lezarva.config(state="disabled")


    def enable_btn_lezarva(self): 
        """ Engedélyezzük a ticket lezárása (és beküldése) gombot."""
        self.btn_lezarva.config(state="normal")


    def disable_btn_get_next_job(self):
        """ Letiltjuk a következő munka lekérése gombot."""
        self.btn_get_next_job.config(state="disabled")


    def enable_btn_get_next_job(self):
        """ Engedélyezzük a következő munka lekérése gombot."""
        self.btn_get_next_job.config(state="normal")



