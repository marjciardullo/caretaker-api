from db import db


class Exam(db.Model):
    __tablename__ = "exame"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=False)
    descricao = db.Column(db.String(500))
    data = db.Column(db.String(100))
    horario = db.Column(db.String(100))

    def __init__(
        self,
        nome,
        descricao,
        data,
        horario,
    ):
        self.nome = nome
        self.descricao = descricao
        self.data = data
        self.horario = horario

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_exam_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_exam_by_name(cls, nome):
        return cls.query.filter_by(nome=nome).first()
