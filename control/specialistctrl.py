import logging
import time
import threading
import copy
import tkinter.messagebox as mb
from model.ticket import Ticket

class SpecialistCtrl(object):
    """ Controller: program logika + összeköti a grafikus felületet az adatbázissal + logolás. """

    # Logfile helye, logolás szintje
    LOGFILE = "specialista.log"
    LOGLEVEL= logging.ERROR  #logging.ERROR  logging.DEBUG

    # Hibaüzenetek
    ERR_DB_GENERIC  = "Az adatbázis nem elérhető\n" \
                    + "Kérem vegye fel a helpdeskkel a kapcsolatot!\n" \
                    + "Tel: (xx)xxx-xxxx vagy email: helpdesk@xxxxx.xx"
    ERR_DB_WRITE    = "Nem sikerült az adatokat kiírni az adatbázisba!\n" \
                    + "Kérem próbálja újra, vagy vegye fel a helpdeskkel a kapcsolatot!\n" \
                    + "Tel: (xx)xxx-xxxx vagy email: helpdesk@xxxxx.xx"
    ERR_GUI_MISSING = "HIÁNYZÓ ADATOK\n" \
                    + "Az ügyfélazonosító, vagy a probléma leírása hiányzik!"
    ERR_GUI_STATE   = "STÁTUSZ ISMERETLEN\n" \
                    + "Beküldés előtt kérem állítsa be a hibabejelentés állapotát!"




    def __init__(self, parent, problem_type):
        """ Elindítja a logolást, kapcsolatot teremt a főprogrammal.

        Parameter:
            parent: a főprogram (ebben van a programot leállító metódus)
        """
        # Logolás
        logging.basicConfig(filename=self.LOGFILE, encoding="utf-8", level=self.LOGLEVEL,
                            format="%(asctime)s %(levelname)s: %(message)s", 
                            datefmt = "%Y.%m.%d %H:%M.%S")

        # Főprogram: a teljes programot leállító metódus ebben van 
        self.main_program = parent

        # milyen típusú problémákat kezelünk (ilyen típusú hibajegyeket kérünk le az adatbázisból)
        self.problem_type = problem_type 

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
            gui (SpecialistGUI): ebben az objektumban vannak azok a metódusok, amiket 
                       meghívva kiolvassuk / beírjuk a képernyőn látható adatokat
         """
        logging.debug("GUI betöltése: {gui}")  
        self.gui = gui



    def set_db(self, db):
        """ Megkapjuk a főprogramban létrehozott adatbáziskezelőt.

        Ezt az adatbázisba való íráshoz / olvasáshoz használjuk.
        Egyúttal meghívunk egy ellenőrzést is, hogy most van-e várakozó hibajegy.

        Parameter:
            db (DatabaseHandler): ebben az objektumban vannak azok a metódusok, amiket 
                       meghívva tudjuk írni/olvasni az adatbázist
        """
        logging.debug(f"Adatbáziskezelő betöltése: {db}")  
        self.db = db                                  
        # Ha van várakozó hibajegy, akkor a lekérés gomb aktív, különben letiltva
        self.check_for_waiting_tickets_change_gui()


    def show_err_exit(self, msg):
        """ Ha javíthatatlan hiba történt hibaüzenetet ír a képernyőre, majd kilép.

        A logolást nem intézi! Azt a meghívás helyén oldjuk meg.
       
        Parameter:
            msg (str): a képernyőre kiirandó hibaüzenet

        """
        mb.showerror("Hiba", msg)
        self.main_program.close_program()


    def show_err_continue(self, msg):
        """ Hiba történt, de lehet, hogy helyrehozható. Csak hibaüzenetet ír a képernyőre.

        A logolást nem intézi! Azt a meghívás helyén oldjuk meg.
       
        Parameter:
            msg (str): a képernyőre kiirandó hibaüzenet
        """
        mb.showerror("Hiba", msg)
         

    def check_for_waiting_tickets_change_gui(self):
        """ Ellenőrzi, hogy az adatbázisban van-e olyan ticket, amit nekünk kell majd megoldani
        
        Ha van  : gui-ban engedélyezi a következő ticket lekérő gombot
        Ha nincs: gui-ban letiltja a következő ticket lekérő gombot
        
        Hiba esetén: hibaüzenet + logolás + kilép a programból
        """

        try:
            # Ha van olyan típusú munka, amivel mi foglalkozunk, akkor a lekérő gomb aktív
            if self.db.ticket_waiting(self.problem_type):
                 self.gui.enable_btn_get_next_job()
                 logging.debug("Van várakozó ticket: self.gui.enable_btn_get_next_job()")
            # Ha nincs, letiltja a gombot és majd csak a thread_check_for_tickets oldja fel
            else:                                  
                 self.gui.disable_btn_get_next_job()
                 logging.debug("Nincs várakozó ticket: self.gui.disable_btn_get_next_job()") 
        except Exception as e:
            logging.error("Nem tudtuk ellenőrizni, hogy van-e várakozó ticket.")
            logging.exception(e)
            self.show_err_exit(self.ERR_DB_GENERIC)


    def start_check_for_tickets_thread(self):
        """ Adatbázist figyelő thread indítása. Kívűlről, majd a főprogram indítja el.

        A program lezárásakor vége a threadnek is, nem kell rá várni.

        A főprogram (tehát NEM a controller) indítja el, amikor már minden 
        (gui, controller, stb) biztos, hogy a helyén van és össze is vannak kötve.
        """

        self.check_for_tickets = threading.Thread(target=self.thread_check_for_tickets,
                                                  daemon=True)
        self.check_for_tickets.start()


    def get_next_job(self):
       """ Olyan típusú munka lekérdezése az adatbázisból, amivel mi foglalkozunk.

       A Controller létrehozásakor beállított self.problem_type -ban tárolt állapotú (state)
       hibajegy beolvasása lemezről

       Return:
           Ticket: lemezről beolvasott hibajegy, ami olyan típusú feladat, amivel mi
                   foglalkozunk. Az első (legrégebbi) ilyen ticket.
           None  : nincs ilyen várakozó hibajegy az adatbázisban.
       """
       ticket = None
       # beolvasuk a hibajegyet, hiba esetén logol + hibaüzenet + kilép
       try:
           ticket = self.db.get_next_job(self.problem_type)
           logging.debug(f"Beolvastuk a várakozó ticketet self.problem_type={self.problem_type} ticket={ticket}") 
       except Exception as e:
           logging.error("Nem tudtuk beolvasni a várakozó ticketet")
           logging.exception(e)
           self.show_err_exit(self.ERR_DB_GENERIC)


       if ticket:
           try:
               # Az adatbázisban mostantól az állapota FOLYAMATBAN (más nem tudja lekérni)
               # egy másolatot használunk, azzal írjuk felül az eredetit, hogy a lemezen
               # FOLYAMATBAN lévő legyen az állapota
               ticket_tmp = copy.deepcopy(ticket)         
               ticket_tmp.set_state(Ticket.FOLYAMATBAN)
               self.db.update_ticket(ticket_tmp)
               logging.debug(f"A beolvasott ticket állapota a lemezen már: folyamatban lévő . Eredeti={ticket}, lemezen={ticket_tmp}")
           except Exception as e:
               logging.error("Nem tudtuk átírni a beolvasott ticket állapotát a lemezen folyamatban lévőre")
               logging.exception(e)
               self.show_err_exit(self.ERR_DB_GENERIC)
           
           # Megjelenítjük a ticket adatait a gui-n
           self.gui.set_ticket_id(ticket.get_ticket_id()) 
           self.gui.set_user_id(ticket.get_user_id())
           self.gui.set_problem(ticket.get_problem())

           # Mostantól nem lehet új munkát lekérni, csak ezt lezárni
           # Az ügyintéző dolgozik (pl. nem kell ellenőrizni a háttérben, hogy van-e új munka)
           self.gui.disable_btn_get_next_job()
           self.gui.enable_btn_lezarva()
           self.gui.set_employee_working(True)
       # Ha a lemezen nem volt várakozó hibajegy
       else:
           #GUI-n letiltjuk a köv. munkát lekérő gombot (majd csak a thread oldja fel, amikor lesz)
           self.gui.disable_btn_get_next_job() 
           logging.debug("get_next_job(): Nincs új lekérhető munka")

    def form_bekuldese(self):
        """ GUI-ból beolvasott adato alapján a lemezre írja a hibajegyet.

        Hiba esetén logolja, hibaüzenet, de nem zárja be a programot (nehogy elveszzenek az
        adatok).
        """

        # Létrehozzuk azt a hibajegyet, ami majd update-eli a lemezen lévőt (ticket_id alapján)
        state = Ticket.LEZARVA

        # form tartalmát egyenként kérdezzük le
        ticket_id = self.gui.get_ticket_id()
        user_id = self.gui.get_user_id()
        problem = self.gui.get_problem()
        ticket = Ticket(ticket_id=ticket_id, user_id=user_id, problem=problem,state=state)
        logging.debug(f"form_bekuldese() ticket={ticket}")

        try:
            # frissítjük a hibajegy adatait a lemezen
            self.db.update_ticket(ticket)
            logging.debug(f"Ticket kiírva lemezre: {ticket}")    

            # mostantól csak új munkát lehet lekérni (beküldeni nem létező munkát nem)
            self.gui.disable_btn_lezarva()
            # ticketlekérő gomb = aktív, ha van mit lekérni   
            self.check_for_waiting_tickets_change_gui() 

            self.gui.clear_form() 
            self.gui.set_employee_working(False)
        except Exception as e:
            logging.error("Nem tudtuk a ticketet kiírni lemezre")
            logging.exception(e)
            self.show_err_continue(self.ERR_DB_WRITE)




    def thread_check_for_tickets(self):
        """ Thread: ellenőrzi 5 másodpercentként hogy van-e nekünk szánt hibajegy.

        Controller létrehozásakor beállítottuk, hogy milyen típusú hibákat fogad
        ez az ügyintéző (self.problem_type).
    
        Ha az ügyintéző szabad (és nem dolgozik egy másik hibajegyen), akkor ez a 
        thread 5 másodpercenként ellenőrzi, hogy van-e neki szánt hibajegy. 
        Ha van, akkor a következő munkát lekérő gomb aktív lesz.
        Ha nincs (pl. egy másik ügyintéző elvitte elötte), akkor a következő munkát 
        lekérő gombot letiltja.

        Hiba esetén (ha nem tudja ellenőrizni az adatbázist): logol, hibaüzenet, kilép.
        """

        while True:
            if not self.gui.is_employee_working():
                try:
                    if self.db.ticket_waiting(self.problem_type):
                        self.gui.enable_btn_get_next_job()
                    time.sleep(5)
                except Exception as e:
                    logging.error("Nem tudtuk ellenőrizni, hogy van-e várakozó ticket")
                    logging.exception(e)
                    self.show_err_exit(self.ERR_DB_GENERIC)


