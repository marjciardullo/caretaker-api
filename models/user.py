from db import db


class User(db.Model):
    __bind_key__ = "caretaker"
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(100))
    senha = db.Column(db.String(10))
    nascimento = db.Column(db.String(100))

    def __init__(self, nome, email, senha, nascimento) -> None:
        self.nome = nome
        self.email = email
        self.senha = senha
        self.nascimento = nascimento

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
