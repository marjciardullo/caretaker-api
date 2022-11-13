from db import db


class Medication(db.Model):
    __tablename__ = "medicamento"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=False)
    dosagem = db.Column(db.String(200))
    qt_medicamento = db.Column(db.Float)
    obs_medicamento = db.Column(db.String(500))
    frequencia_diaria = db.Column(db.Integer)
    frequencia_horas = db.Column(db.Integer)

    def __init__(
        self,
        nome,
        dosagem,
        qt_medicamento,
        obs_medicamento,
        frequencia_diaria,
        frequencia_horas,
    ):
        self.nome = nome
        self.dosagem = dosagem
        self.qt_medicamento = qt_medicamento
        self.obs_medicamento = obs_medicamento
        self.frequencia_diaria = frequencia_diaria
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
    def find_medication_by_name(cls, nome):
        return cls.query.filter_by(nome=nome).first()
