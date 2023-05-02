from db import db


class Medication(db.Model):
    __tablename__ = "medicamento"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    nome = db.Column(db.String(100))
    dosagem = db.Column(db.String(200))
    qt_medicamento = db.Column(db.Float)
    obs_medicamento = db.Column(db.String(500))
    frequencia_horas = db.Column(db.Integer)

    def __init__(
        self,
        usuario_id,
        nome,
        dosagem,
        qt_medicamento,
        obs_medicamento,
        frequencia_horas,
    ):
        self.usuario_id = usuario_id
        self.nome = nome
        self.dosagem = dosagem
        self.qt_medicamento = qt_medicamento
        self.obs_medicamento = obs_medicamento
        self.frequencia_horas = frequencia_horas

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_medication_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_medication_by_usuario_id(cls, _id):
        return cls.query.filter_by(usuario_id=usuario_id)
