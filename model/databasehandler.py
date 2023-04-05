import sqlite3
from model.ticket import Ticket

class DatabaseHandler():
    """ A lemezen lévő SQLite3 adatbázist kezeli.

    Minden egyes művelet végrehajtásakor megnyitja, majd lezárja az adatbázist.
    A fellépő hibákat továbbdobja a Controller felé, majd ott kezeljük azokat.
    """ 
    
    def __init__(self, name="ticket.db"):
        """ Ha nem adunk meg más nevet, akkor az adatbázis neve: ticket.db """
        super().__init__()

        self.name = name  


    def create_database_if_not_exists(self):
        """ Ha még nem létezik, akkor létrehozzuk az adatbázist
        Return:
            Exception: Ha nem sikerült, exception-t dob a Controllernek
        """
        with sqlite3.connect(self.name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS   tickets(
                    ticket_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    state       INTEGER,
                    user_id     TEXT,
                    problem     TEXT
                )""")  


    def write_new_ticket(self, ticket):
        """ Kiírunk egy új ticketet az adatbázisba, ticket_id nélkül (azt majd visszakapjuk)

        Parameter:
            ticket (Ticket): nem vesszük figylemebe a ticket_id-jét, 
                             ami új ticketnél úgyis None
        
        Return:
            Ticket   : miután az adatbázisba kiírtuk a ticket-et, a régi ticket
                       új egyedi ticket_id-t kap. Ezt az új ticketet adjuk vissza.
            Exception: Ha nem sikerült a kiírás, exception-t dob a Controllernek
        """ 

        state = ticket.get_state()
        user_id = ticket.get_user_id()
        problem = ticket.get_problem()

        with sqlite3.connect(self.name) as conn:
            # kiírjuk a ticket-et (ticket_id nélkül)
            cursor = conn.cursor()
            sql = """ INSERT INTO tickets (state, user_id, problem)
                      VALUES (?, ?, ?) """
            conn.execute(sql, (state, user_id, problem))

            # mi volt az utolsó ticket_id, amit kiosztott az adatbázis?
            sql = """ SELECT ticket_id   FROM tickets
                      ORDER BY ticket_id DESC    LIMIT 1 """ 
            cursor.execute(sql)
            # mivel tuple-t ad vissza!
            ticket_id=cursor.fetchone()[0]  

            # az adatok mellett most már az id is be van állítva
            ticket.set_ticket_id(ticket_id)  
            return ticket             


    def read_ticket(self, ticket_id):
        """ Beolvassuk a megadott ticket_id-vel rendelkező ticket-et a lemezen lévő adatbázisból.
        
        Parameter:
            ticket_id (int): a keresett ticket egyedi azonosítója

        Return:
            Ticket   : az adatbázisból beolvasott ticket
            None     : nem volt ilyen ticket
            Exception: ha nem sikerült a beolvasás, exception-t dob a Controllernek
        """

        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            sql = """SELECT state, user_id, problem, ticket_id    FROM tickets
                     WHERE ticket_id = ?"""
            cursor.execute(sql, (ticket_id,)) # ha csak egy paraméter van, akkor is tuple-ként
            result = cursor.fetchone()
            if result:
                return Ticket(*result)
            else:
                return None


    def update_ticket(self, ticket):
        """ A lemezen frissítjük ennek a ticketnek (ticket_id alapján) a tartalmát.
 
        Parameter:
            ticket (Ticket): ezzel írjuk felül a lemezen az azonos ticket_id-jű ticketet

        Return:
            Ticket   : ha sikerült a kiírás visszaadja a kiírt ticketet
            Exception: ha nem sikerült a kiírás, exception-t dob a Controllernek
        """
        ticket_id = ticket.get_ticket_id()
        state = ticket.get_state()
        user_id = ticket.get_user_id()
        problem = ticket.get_problem()
        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            sql = """UPDATE tickets 
                     SET state=?, user_id=?, problem=?
                     WHERE ticket_id = ?"""
            cursor.execute(sql, (state,user_id,problem,   ticket_id))
            conn.commit()

        return ticket                  
                     

    def ticket_waiting(self, problem_type):
        """ Van  egy ilyen problémához tartozó, lekezeletlen ticket az adatbázisban?

        Parameter:
            problem_type (int): ilyen típusú problémával rendelkező ticketet keresünk a lemezen

        Return
            boolean  : van / nincs ilyen problémájú ticket a lemezen
            Exception: ha nem sikerült az ellenőrzés, exception-t dob a Controllernek
        """

        with sqlite3.connect(self.name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT ticket_id, state, user_id, problem   FROM tickets   
                WHERE state = {problem_type}
                ORDER BY ticket_id ASC    LIMIT 1""") 
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False 


    def get_next_job(self, problem_type):
        """ A lemezről beolvas és visszaad egy ilyen állapotú, még megoldatlan ticketet.

        Parameter:
            problem_type (int): a keresett probléma típusa
         
        Return
            Ticket   : a legrégebbi, ilyen állapotú (state) ticket
            None     : he nincs több ilyen
            Exception: ha nem sikerült a beolvasás, exception-t dob a Controllernek
        """

        ticket_id = None 
        with sqlite3.connect(self.name) as conn:
            # a legrégebbi ilyen típusú hibajegy
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT ticket_id, state, user_id, problem   FROM tickets   
                WHERE state = {problem_type}
                ORDER BY ticket_id ASC    LIMIT 1""") 
            result = cursor.fetchone()

            if result: # volt ilyen adat
                ticket_id, state, user_id, problem = result[0:4]
            else:
                ticket_id = None

        # Visszaadjuk a talált ticketet. None=nincs ilyen ticket
        if ticket_id:
            ticket = Ticket(ticket_id=ticket_id, state=state, user_id=user_id, problem=problem)
            return ticket
        else:
            return None