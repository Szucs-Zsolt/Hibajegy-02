class Ticket(object):
    """ Hibajegy: tartalmazza az összes adatot a bejelentéssel kapcsolatban.

    Az objektum változóit kívülről nem lehet elérni (aláhúzással kezdődnek), csak a
    getter, setter metódusokon keresztül.
    """

    # A ticket állapota lehet:
    LEZARVA         = 0
    FOLYAMATBAN     = 1
    TECHNEK_KULD    = 2
    PENZUGYNEK_KULD = 3

    def __init__(self, state, user_id, problem, ticket_id=None):
        """ Ticket (hibajegy) létrehozása.

        Létrehozáskor többnyire még nem tudjuk a ticket_id-t (None), mivel általában 
        ezt csak az adatbázisba írás után tudjuk meg és állítjuk be.

        Értékadáskor javasolt a paraméterekre a nevükkel hivatkozni, nehogy eltévesszük
        a sorrendet.

        Parameter:
           state     (int): állapota: lezárva / épp dolgoznak rajta / kinek kell továbbítani
           user_id   (str): a hibát bejelentő felhasználó azonosítója
           problem   (str): a probléma leírása
           ticket_id (str): a hibajegy egyedi azonosítója, kezdetben None, majd ha kiírtuk
                           az adatbázisba, akkor tudjuk meg, hogy milyen azonosítót kapott. 
        """

        # A változókat közvetlenül nem lehet kívülről elérni
        self._ticket_id = ticket_id     # adatbázistól visszakapott egyedi azonosító
        self._state = state             # le van-e zárva, vagy mit kell vele csinálni
        self._user_id = user_id         # ki jelentette be
        self._problem = problem         # probléma leírása


    def __str__(self):
        """Visszaadja a hibajegyet könnyen olvasható string formájában."""
        return f"ticket_id={self._ticket_id}  state={self._state}  user_id={self._user_id}  problem={self._problem}"


    def __repr__(self):
        """Visszaadja a hibajegyet tömören, minden magyarázat nélkül, string formában."""
        return f"Ticket({self._ticket_id}, {self._state}, {self._user_id}, {self._problem})"


    def set_ticket_id(self, ticket_id):
        """ Miután a ticket azonosítóját az adatbázisba írás után megkaptuk, itt állítjuk be
        Parameter:
            ticket_id (int): a ticket új, egyedi azonosítója  
        """
        self._ticket_id = ticket_id


    def get_ticket_id(self):
        """ A ticket egyedi azonosítóját adja vissza
        
        Retrun:
            int: az egyedi azonosító, amivel az adatbázisban a ticketre hivatkozunk
        """
        return self._ticket_id   


    def get_user_id(self):
        """ Visszaadjuk a hibát bejelentő felhasználó azonosítóját

        Return:
            str: a hibát bejelentő felhasználó azonosítója
        """
        return self._user_id


    def get_problem(self):
        """ Visszaadjuk a probléma leírását
        
        Return:
            str: a probléma leírása
        """
        return self._problem  


    def get_state(self):
        """ Visszadjuk a ticket állapotát
        
            int: a ticket állapota (kell-e vele valamit csinálni, ha igen mit)
        """ 
        return self._state


    def set_state(self, state):
        """ Megváltoztatjuk a hibajegy állapotát (state)
    
        Parameter:
            state (int): új állapot (lezárva / dolgoznak rajta / kinek kell továbbítani)
        """
        self._state = state



