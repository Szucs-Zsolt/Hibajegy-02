import unittest
from model.ticket import Ticket


class MyTest(unittest.TestCase):
    def test_ticket_values_ticket_id_later(self):
        state   = 1
        user_id = 2
        problem = ["problem","problem"] 
        ticket = Ticket(state=state, user_id=user_id, problem=problem)
        self.assertEqual(ticket.get_ticket_id(), None)
        self.assertEqual(ticket.get_state(), state)
        self.assertEqual(ticket.get_user_id(), user_id) 
        self.assertEqual(ticket.get_problem(), problem)
        ticket.set_ticket_id(99)   
        self.assertEqual(ticket.get_ticket_id(), 99)

    def test_ticket_values_with_ticket_id(self):
        ticket_id = 99
        state   = 1
        user_id = 2
        problem = "problem\nproblem"
        ticket = Ticket(state=state, user_id=user_id, problem=problem, ticket_id=ticket_id)
        self.assertEqual(ticket.get_ticket_id(), ticket_id)
        self.assertEqual(ticket.get_state(), state)
        self.assertEqual(ticket.get_user_id(), user_id)
        self.assertEqual(ticket.get_problem(), problem)

    def test_ticket_as_string(self):
        ticket_id = 99
        state   = 1
        user_id = 2
        problem = "problem\nproblem"
        ticket = Ticket(state=state, user_id=user_id, problem=problem, ticket_id=ticket_id)
        self.assertEqual(str(ticket), 
           f"ticket_id={ticket_id}  state={state}  user_id={user_id}  problem={problem}")
       