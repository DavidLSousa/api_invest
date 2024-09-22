from flask import (
    Blueprint,
    request,
    jsonify
)
from controller.ticket_controller import TicketController

tickets_bp = Blueprint('tickets', __name__)


@tickets_bp.route('/tickets/add')
def render_add_ticket_page():
  return TicketController.render_add_page()


@tickets_bp.route('/tickets/all')
def render_all_ticket_page():
  return TicketController.render_all_page()


@tickets_bp.route('/tickets', methods=['POST'])
def add_ticket():
  pass


@tickets_bp.route('/tickets', methods=['DELETE'])
def delete_ticket():
  pass


@tickets_bp.route('/tickets', methods=['PUT'])
def put_ticket():
  pass
