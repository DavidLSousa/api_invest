import yfinance as yf
import datetime 
import traceback
from flask import (
  current_app,
  render_template,
  request as req
  )
from dataclasses import dataclass

from adapters.database_adapter import DatabaseAdapter
from src.domain.services.mysql_services import MysqlServices
from src.domain.entities.ticket_entity import TicketEntity

@dataclass
class TicketController:
  database_adapter = DatabaseAdapter(database=MysqlServices())

  @classmethod
  def render_all_page(cls):
    test = [
      {
        'ticket': 'ITSA4',
        'nameTicket': 'Itausa',
        'average_price': 8.51,
        'number_of_tickets': 55,
        'total_value_purchased': 602.25
      },
      {
        'ticket': 'PETR3',
        'nameTicket': 'Petrobras',
        'average_price': 30.00,
        'number_of_tickets': 20,
        'total_value_purchased': 600.00
      },
      {
        'ticket': 'VALE3',
        'nameTicket': 'Vale',
        'average_price': 75.00,
        'number_of_tickets': 10,
        'total_value_purchased': 750.00
      }
    ]

    try:
      return render_template('all_tickets_page.html', title_page='Meus Ativos', tickets=test)
    
    except ValueError as err:
      stack_trace = traceback.format_exc()
      current_app.logger.error(f'ERRO render_all_page: {stack_trace}')
      return {'status': 500, 'error': 'Erro interno do servidor'}
  
  @classmethod
  def render_add_page(cls): # Pegar info do db e passar para renderizar a pagina com os dados dos tickets do db
  
    try:
      return render_template('add_tickets_page.html', title_page='Adicionar Ativos')
    
    except ValueError as err:
      stack_trace = traceback.format_exc()
      current_app.logger.error(f'ERRO render_add_page: {stack_trace}')
      return {'status': 500, 'error': 'Erro interno do servidor'}

  @classmethod
  def add_ticket_controller(cls):
    try:
      if not req.json:
        raise ValueError("Dados JSON não fornecidos")

      for current_ticket in req.json:
        check_ticket_in_db = cls.database_adapter.get_ticket(current_ticket['ticket']) 
        
        if check_ticket_in_db is None:
          cls.__handle_create_ticket(current_ticket)
        else:
          cls.__handle_update_ticket(current_ticket, check_ticket_in_db)

      return { "status": 200, 'message': 'Tudo certo' }
    
    except Exception as err:
      stack_trace = traceback.format_exc()
      current_app.logger.error(f'ERRO add_ticket_controller: {stack_trace}')
      return {'status': 500, 'error': 'Erro interno do servidor'}

  @classmethod
  def delete_ticket_controller(cls, ticker):
    try:
      print(f'Ticker del:  {ticker}')

      return { "status": 200 }
    
    except ValueError as err:
      stack_trace = traceback.format_exc()
      current_app.logger.error(f'ERRO delete_ticket_controller: {stack_trace}')
      return {'status': 500, 'error': 'Erro interno do servidor'}

  @classmethod
  def edit_ticket_controller(cls, ticker):
    try:
      # Não implementar até ajustar o front
        # É uma venda de ativos
      print(f'Ticker edit:  {ticker}')

      return { "status": 200 }
    
    except ValueError as err:
      stack_trace = traceback.format_exc()
      current_app.logger.error(f'ERRO edit_ticket_controller: {stack_trace}')
      return {'status': 500, 'error': 'Erro interno do servidor'}

  # ============================ Private methods ============================ #
  @classmethod
  def __handle_create_ticket(cls, current_ticket) -> None:
    ticket = str(current_ticket['ticket'])
    number_of_tickets = int(current_ticket['number_of_tickets'])
    total_value_purchased = float(current_ticket['total_value_purchased'])
      
    price_metrics = cls.__get_price_metrics(current_ticket)

    new_ticket = TicketEntity(
      _nameTicket=            cls.__get_ticket_name_api(current_ticket),
      _ticket=                ticket,
      _number_of_tickets=     number_of_tickets,
      _total_value_purchased= total_value_purchased,
      _highest_price=         price_metrics['highest_price'],
      _lowest_price=          price_metrics['lowest_price'],
      _average_price=         price_metrics['average_price'],
      _history=[
        {
          'qntTickets': number_of_tickets,
          'valuePerTicket': total_value_purchased / number_of_tickets,
          'date': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
      ]
    )

    cls.database_adapter.create_ticket(new_ticket)
  
  @classmethod
  def __handle_update_ticket(cls, new_ticket, db_ticket) -> None:
    updated_number_of_tickets = int(db_ticket['number_of_tickets']) + int(new_ticket['number_of_tickets'])
    updated_total_value_purchased = float(db_ticket['total_value_purchased']) + float(new_ticket['total_value_purchased'])
    db_history = eval(db_ticket['history']) 

    price_metrics = cls.__get_price_metrics(new_ticket, db_ticket)

    updated_ticket = TicketEntity(
      _nameTicket=            db_ticket['nameTicket'],
      _ticket=                db_ticket['ticket'],
      _number_of_tickets=     updated_number_of_tickets,
      _total_value_purchased= updated_total_value_purchased,
      _highest_price=         price_metrics['highest_price'],
      _lowest_price=          price_metrics['lowest_price'],
      _average_price=         price_metrics['average_price'],
      _history=               db_history + [
        {
          'qntTickets': new_ticket['number_of_tickets'],
          'valuePerTicket': float(new_ticket['total_value_purchased']) / int(new_ticket['number_of_tickets']),
          'date': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
      ]
    )

    cls.database_adapter.update_ticket_increment(updated_ticket)
  
  @classmethod
  def __get_ticket_name_api(cls, current_ticket) -> str:
    ticker = yf.Ticker(current_ticket['ticket'])
    ticketName = ticker.info.get('longName')

    if ticketName == None:
      raise ValueError('Ticket não encontrado')

    return ticketName
  
  @classmethod
  def __get_price_metrics(cls, new_ticket, db_ticket=None) -> dict[str, float]:
    new_total_value_purchased = float(new_ticket['total_value_purchased'])
    new_number_of_tickets = float(new_ticket['number_of_tickets'])
    new_price = new_total_value_purchased / new_number_of_tickets

    if db_ticket is None:
      return {
        'average_price': new_price,
        'highest_price': new_price,
        'lowest_price': new_price
      }
    
    total_tickets = db_ticket['number_of_tickets'] + new_number_of_tickets
    total_value_purchased = db_ticket['total_value_purchased'] + new_total_value_purchased
    new_average_price = total_value_purchased / total_tickets
    
    highest_price = max(db_ticket['highest_price'], new_price)
    lowest_price = min(db_ticket['lowest_price'], new_price)

    return {
      'average_price': new_average_price,
      'highest_price': highest_price,
      'lowest_price': lowest_price
    }