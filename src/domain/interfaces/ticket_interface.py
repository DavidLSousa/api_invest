from abc import ABC, abstractmethod

from src.domain.entities.ticket_entity import TicketEntity

class TicketInterface(ABC):
  @abstractmethod
  def get_ticket(self, ticket_name: str):
    pass

  @abstractmethod
  def get_all_ticket(self):
    pass

  @abstractmethod
  def create_ticket(self, ticket: TicketEntity):
    pass

  @abstractmethod
  def update_ticket(self, ticket_id: int, ticket: TicketEntity):
    pass

  @abstractmethod
  def delete_ticket(self, ticket_id: int):
    pass
