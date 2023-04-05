import tkinter as tk
from view.font import FONT


class HibabejelentoForm(tk.Frame):
    """ Frame, amiben felvesszük a hibajegy adatait.
    """

    def __init__(self, parent):
        """ Megjeleníti azokat a vizuális elemeket, amibe majd beleírjuk az adatokat.
        Parameter:
            parent: mibe rakjuk ki ezt a frame-et
        """
        super().__init__(parent)

        self.user_id = tk.StringVar()

        # Adatok: bejelentő felhasználó azonosítója  és  a probléma leírása
        lbl_user_id = tk.Label(self, text="Ügyfélazonosító:", font=FONT)
        lbl_problem = tk.Label(self, text="A hiba leírása:", font=FONT)
        self.ent_user_id = tk.Entry(self, textvar=self.user_id, font=FONT)
        self.ent_problem = tk.Text(self, width=80, height=20, font=FONT)

        # Hiba leírása scrollozható
        self.scrollbar   = tk.Scrollbar(self, orient=tk.VERTICAL) 
        self.scrollbar.config(command=self.ent_problem.yview)
        self.ent_problem.config(yscrollcommand=self.scrollbar.set)

        # Elemek megjelenítése
        lbl_user_id.pack()
        self.ent_user_id.pack()
        lbl_problem.pack()
        self.ent_problem.pack(side=tk.LEFT, fill=tk.Y) 
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.ent_user_id.focus_set()


    def clear_form(self):
        """ Törlünk minden adatot a formból. """
        self.user_id.set("")
        self.ent_problem.delete("1.0", tk.END)  


    
    def get_user_id(self):
        """ Kiolvassuk a formból és visszaadjuk, hogy ki jelentette be a hibát. """ 
        return self.user_id.get()


    def get_problem(self):
        """ Kiolvassuk a formból és visszaadjuk a hiba leírását. """ 
        return self.ent_problem.get("1.0",tk.END)