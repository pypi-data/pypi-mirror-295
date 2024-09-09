# GLPI API

A Python library to interact with GLPI API.

## Installation

You can install the package using pip:


## Usage

```python
from glpi_api import GLPIAPI

glpi = GLPIAPI(base_url="http://localhost:8090", username="glpi", password="glpi")
ticket_id = glpi.create_ticket(title="Sample Ticket", content="This is a sample ticket", urgency=3, requester_id=5, assigned_id=6)
print(f"Ticket created with ID: {ticket_id}")

