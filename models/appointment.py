from db import db


class Appointment(db.Model):
    __tablename__ = "consulta"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(500))
    data = db.Column(db.String(100))
    horario = db.Column(db.String(100))

    def __init__(
        self,
        usuario_id,
        nome,
        descricao,
        data,
        horario,
    ):
        self.usuario_id = usuario_id
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
    def find_appointment_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls, usuario_id):
        return cls.query.filter_by(usuario_id=usuario_id).all()
