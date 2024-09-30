from dataclasses import dataclass

from src.domain.entities.ticket_entity import TicketEntity
from src.domain.services.mysql_services import MysqlServices
from src.domain.interfaces.ticket_interface import TicketInterface

@dataclass
class DatabaseAdapter(TicketInterface):
    database: TicketInterface 

    def get_ticket(self, ticket_name: str) -> TicketEntity | None:
        return self.database.get_ticket(ticket_name)
    
    def get_all_ticket(self) -> list[TicketEntity] | None:
        return self.database.get_all_ticket()
    
    def create_ticket(self, ticket: TicketEntity):
        self.database.create_ticket(ticket)
    
    def update_ticket(self, ticket_id: int, ticket: TicketEntity):
        self.database.update_ticket(ticket_id, ticket)  
    
    def update_ticket_increment(self, ticket: TicketEntity):
        self.database.update_ticket_increment(ticket)
    
    def delete_ticket(self, ticket_id: int):
        self.database.delete_ticket(ticket_id)
