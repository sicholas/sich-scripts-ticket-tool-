

class Ticket:
  def __init__(self, message, user, request):
    self.message = message
    self.state = TicketState.OPENED
    self.user = user
    self.request = request

from enum import Enum


class TicketState(Enum):
    OPENED = 1
    CLAIMED = 2