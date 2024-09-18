from flask import Flask
import peewee
import pymysql
import time, os

from models import db, Ticket

from router.main_page import main_page_bp
from router.tickets_page import tickets_bp
from router.news_page import news_bp
from router.dashboard_page import dashboard_bp

app = Flask(__name__)

# DB MySQL
if os.getenv('RUNNING_IN_DOCKER') == 'True':
    with app.app_context():
        retry_attempts = 5
        for attempt in range(retry_attempts):
            try:
                pymysql.install_as_MySQLdb()

                db.connect()
                print("Conectado ao MySQL com sucesso!")
                db.create_tables([Ticket], safe=True)
                print("Table Ticket criada com sucesso!")
                break

            except peewee.OperationalError as e:
                print(f"Erro ao conectar ao MySQL: {e}")
                time.sleep(5)  

# Routers
app.register_blueprint(main_page_bp)
app.register_blueprint(tickets_bp)
app.register_blueprint(news_bp)
app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# OUTRAS FORMAS DE RODAR:

# flask --app main run -
    # flask --app main run --port 3000
# flask --app main run --debug

# Atualizar requirements
# pip freeze > requirements.txt
# pip install -r requirements.txt

# DOCKER
# docker run <NAME IMAGE>
# docker ps
# docker ps -a
# docker stop <container_id>
# docker rm <container_id>

# docker build -t app_investment . -------------> Cria a imagem
# docker run -d -p 5000:5000 app_investment ----> sobe o container, pode ser substiruido pelo docker-compose

# docker-compose up
# docker-compose down
# docker-compose up --build --------------------> Reconstroi as imagens quando necessario (atualiza quando modificado)

# docker volume rm

# docker exec -it mysql-db mysql -u root -p ----> abre o mysql do container