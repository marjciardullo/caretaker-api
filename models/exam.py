from db import db


class Exam(db.Model):
    __tablename__ = "exame"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    medico = db.Column(db.String(100))
    exame = db.Column(db.String(100))
    local = db.Column(db.String(200))
    data = db.Column(db.String(100))
    horario = db.Column(db.String(100))

    def __init__(
        self,
        usuario_id,
        medico,
        exame,
        local,
        data,
        horario,
    ):
        self.usuario_id = usuario_id
        self.medico = medico
        self.exame = exame
        self.local = local
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
    def find_exam_by_usuario_id(cls, _id):
        return cls.query.filter_by(usuario_id=usuario_id)
