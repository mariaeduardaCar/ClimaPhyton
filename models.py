from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Clima(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(100), nullable=False)
    temperatura = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Clima {self.cidade}>'
