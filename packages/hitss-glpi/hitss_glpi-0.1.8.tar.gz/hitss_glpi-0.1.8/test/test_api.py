import unittest
from glpi_api import GLPIAPI

class TestGLPIAPI(unittest.TestCase):
    def setUp(self):
        self.glpi = GLPIAPI(base_url="http://localhost:8090", username="glpi", password="glpi")

    def test_create_ticket(self):
        ticket_id = self.glpi.create_ticket(title="Test Ticket", content="Testing ticket creation", urgency=3, requester_id=1, assigned_id=1)
        self.assertIsNotNone(ticket_id)

if __name__ == '__main__':
    unittest.main()
