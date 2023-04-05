import unittest
import os
from model.databasehandler import DatabaseHandler
from model.ticket import Ticket


class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseHandler("test_databasehandler.db") 
        self.ticket_id = None
        self.user_id="12345"
        self.state = 2
        self.problem = "Sor1\nSor2\nSor3"
        self.ticket = Ticket(ticket_id=self.ticket_id, user_id=self.user_id, 
                             state=self.state, problem=self.problem)

    def tearDown(self):
        self.ticket = None
        self.db = None
        os.remove("test_databasehandler.db")


    def test_create_database_bad_path(self):
        self.assertRaises(Exception, DatabaseHandler, "A:\testdatabase.db")

    def test_database_write_new_ticket(self):
        result = self.db.write_new_ticket(self.ticket)
        self.assertNotEqual(result.get_ticket_id(), None, 
            "Kiírás után nem változtatta meg a ticket_id-t!")


    def test_database_write_read_new_ticket(self):
        self.ticket = self.db.write_new_ticket(self.ticket)
        db_ticket = self.db.read_ticket(self.ticket.get_ticket_id())
        self.assertEqual(str(self.ticket), str(db_ticket))	


    def test_database_update_ticket(self):
        # kiírjuk az eredeti és az új ticketet
        # a kettő közötti egyetlen különbség, hogy az új ticket state-je 0 (és nem 2)
        self.ticket = self.db.write_new_ticket(self.ticket)
        
        ticket_id = self.ticket.get_ticket_id()
        ticket2 = Ticket(ticket_id=self.ticket_id, user_id=self.user_id, 
                         state=0, problem=self.problem)
        ticket2.set_ticket_id(self.ticket.get_ticket_id())
        ticket2 = self.db.update_ticket(ticket2)

        # ha a régi ticket state-jét is átállítjuk 0-ra, akkor nem lesz közöttük különbség
        self.ticket.set_state(0)   
        self.assertEqual(str(self.ticket), str(ticket2))
        

    def test_database_ticket_waiting(self):
        # üres adatbázisban nincs 2-es állapotú várakozó ticket
        self.assertTrue(self.db.ticket_waiting, 2)    

        # kiírjunk egy 2-es állapotú ticket-et: most már van ami várakozik
        self.ticket = self.db.write_new_ticket(self.ticket)
        self.assertTrue(self.db.ticket_waiting, 2)  

        # állapotát módosítjuk 0-ra, most már nincs
        self.ticket.set_state(0)
        self.db.update_ticket(self.ticket)
        self.assertTrue(self.db.ticket_waiting, 2)    


    # visszaad egy olyan ticketet, aminek az állapota 2-es	
    def test_get_next_job(self):
        # üres adatbázisban nincs várakozó 2-es állapotú ticket
        self.assertEqual(self.db.get_next_job(2), None)

        # 1-es állapotú ticket van, de 2-es nincs
        self.ticket.set_state(1)
        self.db.write_new_ticket(self.ticket) 
        self.assertEqual(self.db.get_next_job(2), None)

        # most már van 2-es állapotú
        self.ticket.set_state(2)
        self.db.write_new_ticket(self.ticket) 
        self.assertEqual(str(self.db.get_next_job(2)), str(self.ticket))