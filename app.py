from flask import Flask,render_template,request
from Models.models import db, Agenda
from flask import Blueprint
from Controller.agenda import app as agendaController

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///agenda.sqlite3'
app.config["SECRET_KEY"] = 'minhapalavraex'

app.register_blueprint(agendaController, url_prefix='/agenda/')
 
    
if __name__ == "__main__":    
    with app.app_context():
        db.init_app(app=app)
        db.create_all()
        app.run(debug=True)