import tkinter as tk
from view.font import FONT
from model.ticket import Ticket

class Gombok(tk.Frame):
    """ Frame, amiben megváltoztathatjuk a hibajegy jelenlegi állapotát.
    """

    STATES = [ ("Sikeresen lezárva", Ticket.LEZARVA),
               ("Műszakiaknak továbbküldve", Ticket.TECHNEK_KULD),
               ("Pénzügynek továbbküldve", Ticket.PENZUGYNEK_KULD) ]
    def __init__(self, parent):
        """ Kirakja az állapotváltoztatáshoz használt radiobuttonokat és a jóváhagyó gombot.

        Parameter:
            parent: ebbe a frame-be rakjuk majd ki
        """

        super().__init__(parent)

        # Még nem tudjuk, melyik controllerrel kommunikál 
        self.ctrl = None 

        # Befejeztük a hiba kezelését gomb: 
        # a meghívandó parancsot majd akkor kapja meg, amikor megkaptuk a Controller-t
        self.btn_ok = tk.Button(self, text="Beküldés", padx=20, pady=5, font=FONT)
        self.btn_ok.pack(side=tk.BOTTOM, fill=tk.BOTH)  

        # Ticket feldolgozottsági állapota. 
        # Kezdetben: FOLYAMATBAN (egy radiobutton sincs kiválasztva, ezzel nem engedi elküldeni)
        lbl = tk.Label(self, text="ÁLLAPOT:", font=FONT)
        lbl.pack(side=tk.LEFT, padx=5, pady=5)
        self.state= tk.IntVar()
        self.state.set(Ticket.FOLYAMATBAN)

        # Az lehetséges állapotok mindegyikéhez generálunk és kirakunk egy radiobuttont
        self.radiobuttons = [ self.create_radiobutton(state)   for state in Gombok.STATES ] 
        for radiobutton in self.radiobuttons:
            radiobutton.pack(side=tk.LEFT, padx=5, pady=5)


    def create_radiobutton(self, state):
        """ Létrehozunk egy radiobutton-t

        Parameter:
            state []: [0]: gomb felirata,  [1]: az érték, amit majd a Ticket állapotába (state) írunk
                      pl. ["Sikeresen lezárva", Ticket.LEZARVA] 
        Return:
            Radiobutton: be van állítva benne a felirat, az érték és az objektumhoz tartozó közös
                         változó (self.state), amibe az összes Radiobutton ír (hogy melyik
                         érték=állapot van kiválasztva)
        """
        felirat, ertek = state  
        return tk.Radiobutton(self, text=felirat, value=ertek, variable=self.state, font=FONT)



    def set_controller(self, ctrl):
        """ Controller beállítása, amiben a meghívandó metódusok vannak. Elküldő gomb beállítása.

        Miután tudjuk, hogy melyik objektumban vannak az események által meghívott metódusok,
        az elküldő gombhoz hozzárendeljük a form beküldése eseményt.
        Param:
            ctrl (HibabejelentoCtrl): ebben az objektumban vannak a helyi események által
                                      meghívandó metódusok
        """  

        self.ctrl = ctrl
        self.btn_ok.config(command=ctrl.form_bekuldese)



    def get_ticket_state(self):
        """ Visszaküldjük, hogy milyen állapot van kiválasztva a hibajegynek.

        Return:
             int: a radiobuttonok által közösen használt változó (self.state) tartalmazza,
                  hogy milyen állapotal küldjük be a hibajegyet. Ha nem választottunk ki semmit,
                  akkor FOLYAMAT-ban van (ezt küldi el).
        """
        return self.state.get()


    
    def clear_buttons_state(self):
        """ A következő ticket kezdeti állapota ismét FOLYAMATBAN
        
        A radiobuttonok visszaállítva alaphelyzetbe: amin most dolgozunk, az ismét FOLYAMATBAN.   
        """
        self.state.set(Ticket.FOLYAMATBAN)