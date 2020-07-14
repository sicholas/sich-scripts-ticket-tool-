

class Ticket:
  def __init__(self, message, user, request, ticket_id):
    self.message = message
    self.state = TicketState.OPENED
    self.user = user
    self.request = request
    self.ticket_id = ticket_id

from enum import Enum


class TicketState(Enum):
    OPENED = 1
    CLAIMED = 2
