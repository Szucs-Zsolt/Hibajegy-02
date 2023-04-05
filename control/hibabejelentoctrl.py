import logging
import tkinter.messagebox as mb
from model.ticket import Ticket


class HibabejelentoCtrl(object):
    """ Controller: program logika + összeköti a grafikus felületet az adatbázissal + logolás. """

    # Logfájl helye.
    LOGFILE = "hibabejelento.log"
    # Logolt események súlyossága
    LOGLEVEL= logging.ERROR  #logging.ERROR  logging.DEBUG

    # Hibaüzenetek
    ERR_DB_WRITE    = "Nem sikerült az adatokat kiírni az adatbázisba!\n" \
                    + "Kérem próbálja újra, vagy vegye fel a helpdeskkel a kapcsolatot!\n" \
                    + "Tel: (xx)xxx-xxxx vagy email: helpdesk@xxxxx.xx"
    ERR_GUI_MISSING = "HIÁNYZÓ ADATOK\n" \
                    + "Az ügyfélazonosító, vagy a probléma leírása hiányzik!"
    ERR_GUI_STATE   = "STÁTUSZ ISMERETLEN\n" \
                    + "Beküldés előtt kérem állítsa be a hibabejelentés állapotát!"


    def __init__(self, parent):
        """ Elindítja a logolást, kapcsolatot teremt a főprogrammal.

        Parameter:
            parent: a főprogram (ebben van a programot leállító metódus)
        """

        # Logolás
        logging.basicConfig(filename=self.LOGFILE, encoding="utf-8", level=self.LOGLEVEL,
                            format="%(asctime)s %(levelname)s: %(message)s", 
                            datefmt = "%Y.%m.%d %H:%M.%S")

        # Főprogram: a teljes programot leállító metódus ebben van
        self.main_program = parent # főprogram

        # GUI (View): ebből kérdezzük le / írjuk vissza az ügyintéző által kezelt adatokat 
        # Kezdetben none, a főprogram majd akkor adja meg, amikor majd sorra kerül
        self.gui = None            

        # Adatbázis (Model): a lemezen lévő adatbázisba való írás/olvasáshoz
        # Kezdetben none, a főprogram majd akkor adja meg, amikor majd sorra kerül
        self.db  = None            


    def set_gui(self, gui):
        """ Megkapjuk a főprogramban létrehozott GUI-t.

        Ezt a GUI-ból való kiolvasáshoz és GUI-ba való beíráshoz használjuk.

        Parameter:
            gui (HibabejelentoGUI): ebben az objektumban vannak azok a metódusok, amiket 
                       meghívva kiolvassuk / beírjuk a képernyőn látható adatokat
         """
        logging.debug("GUI betöltése: {gui}")  
        self.gui = gui


    def set_db(self, db):
        """ Megkapjuk a főprogramban létrehozott adatbáziskezelőt.

        Ezt az adatbázisba való íráshoz / olvasáshoz használjuk.

        Parameter:
            db (DatabaseHandler): ebben az objektumban vannak azok a metódusok, amiket 
                       meghívva tudjuk írni/olvasni az adatbázist
         """

        logging.debug(f"Adatbáziskezelő betöltése: {db}")  
        self.db = db 


    def show_err_exit(self, msg):
        """ Ha javíthatatlan hiba történt hibaüzenetet ír a képernyőre, majd kilép.

        A logolást nem intézi! Azt a meghívás helyén oldjuk meg.
       
        Parameter:
            msg (str): a képernyőre kiirandó hibaüzenet

        """
        mb.showerror("Hiba", msg)
        self.main_program.close_program()


    def show_err_continue(self, msg, e=None):
        """ Hiba történt, de lehet, hogy helyrehozható. Csak hibaüzenetet ír a képernyőre.

        A logolást nem intézi! Azt a meghívás helyén oldjuk meg.
       
        Parameter:
            msg (str): a képernyőre kiirandó hibaüzenet
        """
        mb.showerror("Hiba", msg)


    def get_form_values(self):
        """ GUI adatmezői alapján visszaad egy hibajegy objektumot.

        Ha nem volt jól kitöltve a form, és nem érvényesek az abban lévő értékek,
        akkor figyelmeztető üzenetet küld a usernek és None-t ad vissza.

        Return:
           Ticket: A GUI-ból kiolvasott értékek alapján létrehozott Ticket objektum.
                   None, ha nem voltak érvényesek a kiolvasott értékek
        """                       

        # GUI-ból kiolvasott adatok + logolása
        state   = self.gui.get_ticket_state()
        user_id = self.gui.get_user_id().strip()
        problem = self.gui.get_problem().strip()
        logging.debug(f"get_form_values() state={state}, user_id={user_id}, problem={problem}") 

        # Lehetséges hiba: nincs kitöltve valamelyik mező: bejelentő vagy a hiba leírása
        if not user_id  or  not problem:   
            logging.debug("Valamelyik mező nincs kitöltve.")
            self.show_err_continue(self.ERR_GUI_MISSING)
            return None
        # Lehetséges hiba: nem állította be, hogy lezárta-e vagy továbbküldi
        elif state == Ticket.FOLYAMATBAN:  
            logging.debug("Ticket állapota nincs beállítva.")
            self.show_err_continue(self.ERR_GUI_STATE)  
            return None

        # Sikeresen létrehozva, logolva, visszaküldve
        ticket = Ticket(state=state, user_id=user_id, problem=problem)
        logging.debug(f"Ticket: {ticket}")
        return ticket


    def form_bekuldese(self):
        """ Az ügyintéző által kitöltött formot kimenti a lemezre (ha érvényes volt).

        Kiírja lemezre, ha érvényes a form.
        Ha ez sikerült (érvényes form + sikeres kiírás), akkor a GUI-ban a formot törli.

        Ha hibás volt a form (get_form_values küld hibaüzenetet), nem írja ki 
        és NEM törli a formot.
        
        Ha nem sikerült kiírni lemezre, akkor hibaüzenet és a GUI-ban NEM törli a formot.
        """

        # Ha hiba volt a form kitöltésénél, akkor nem folytatjuk
        # Hiba esetén a get_form_values küldi a hibaüzenetet a képernyőre
        ticket = self.get_form_values()
        if not ticket:
            return

        # kiíráskor a visszakapott ticketben már benne van a ticket_id is, 
        # amivel bekerült az adatbázisba
        try:
            ticket = self.db.write_new_ticket(ticket)
            logging.debug(f"Ticket kiírva lemezre: {ticket}")    
        except Exception as e:    
            # Hiba, de nem lépünk ki, nehogy elvesszen az eddig begépelt adat
            logging.error("Nem tudtuk a ticketet kiírni lemezre")
            logging.exception(e)
            self.show_err_continue(self.ERR_DB_WRITE)
            return
      
        # Sikerült beküldeni: a formon mindent visszaállítunk alapállapotba
        self.gui.clear_form()
        self.gui.clear_buttons_state()


