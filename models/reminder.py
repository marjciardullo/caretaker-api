from db import db


class Reminder(db.Model):
    __tablename__ = "lembrete"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    descricao = db.Column(db.String(500))
    data = db.Column(db.String(100))
    horario = db.Column(db.String(100))

    def __init__(
        self,
        usuario_id,
        descricao,
        data,
        horario,
    ):
        self.usuario_id = usuario_id
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
    def find_reminder_by_usuario_id(cls, _id):
        return cls.query.filter_by(usuario_id=usuario_id)
