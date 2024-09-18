from peewee import *
from dotenv import load_dotenv
import os

load_dotenv()

db = MySQLDatabase(
    os.getenv('MYSQL_DATABASE'),
    user=os.getenv('MYSQL_USER'),  
    password=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),    
    port=3306      
)

class Ticket(Model):
    nameTicket = CharField()
    ticket = CharField()
    number_of_tickets = IntegerField()
    total_value_purchased = FloatField()
    highest_price = FloatField()
    lowest_price = FloatField()
    average_price = FloatField()
    average_price = FloatField()
    history = TextField(null=True)

    class Meta:
        database = db