from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tarefa = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.Time, nullable=False)

    
    def __init__(self,tarefa, horario):
        self.tarefa = tarefa
        self.horario = horario

    
    def to_dict(self,columns=[]):
        if not columns:
            return {"id": self.id,
                    "tarefa":self.tarefa,
                    "horario":self.horario.strftime("%H:%M:%S") if self.horario else None
                    }
        
        else:
            return {col: getattr(self,col) for col in columns}
        

    
    
