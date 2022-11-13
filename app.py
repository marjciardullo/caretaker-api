from flask import Flask, request
from flask_cors import CORS
from models.user import User
from models.medication import Medication
from models.appointment import Appointment
from models.exam import Exam
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from db import db


app = Flask(__name__)

# mysql://USER:PASSWORD@HOST:PORT/DATABASE
# "mysql://root:3YiF9fywkgT010NIQT3Z@containers-us-west-70.railway.app:7204/railway"
# "mysql://caretaker:caretaker1@127.0.0.1:3306/caretaker"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://s3kx1pfetx2agpt0:n5tqeu5t6tyt3p5k@qvti2nukhfiig51b.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/s1iottgcx110rvoj"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "caretaker"

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    print("Creating database...")
    db.create_all()


@app.route("/")
def home_view():
    return "<h1>Caretaker Flask Api</h1>"


@app.route("/usuario/registrar", methods=["POST"])
def register():

    user = User.find_user_by_email(email=request.json["email"])

    if user:
        return {"message": "Email already exists"}, 404

    new_user = User(
        request.json["nome"],
        request.json["email"],
        request.json["senha"],
        request.json["nascimento"],
    )

    try:
        new_user.save_to_db()
    except Exception as err:
        return {"menssage": f"Error while register new user: {err}"}, 404

    return {"message": "User registered succesfully!"}, 201


@app.route("/login", methods=["POST"])
def login():
    user = User.find_user_by_email(email=request.json["email"])

    if user:
        access_token = create_access_token(identity=user.email)
        return {"access_token": access_token}, 200

    return {"message": "Please, sign in to your account!"}, 404


@app.route("/usuario/<user_id>", methods=["GET"])
# @jwt_required()
def get_user(user_id):
    user = User.find_user_by_id(user_id)

    if not user:
        return {"message": "User not found!"}, 404

    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "senha": user.senha,
        "nascimento": user.nascimento,
    }, 200


@app.route("/usuario/<user_id>", methods=["PUT"])
# @jwt_required()
def update_user(user_id):
    user = User.find_user_by_id(user_id)

    if not user:
        return {"message": "User not found!"}, 404

    user.nome = request.json["nome"]
    user.email = request.json["email"]
    user.senha = request.json["senha"]
    user.nascimento = request.json["nascimento"]

    try:
        user.save_to_db()
    except Exception as err:
        return {"mensagem": f"Erro ao atualizar usuário: {err}"}, 400

    return {"message": "user updated succesfully!"}, 200


@app.route("/usuario/<user_id>", methods=["DELETE"])
# @jwt_required()
def delete_user(user_id):
    user = User.find_user_by_id(user_id)

    if user:
        user.delete_from_db()
        return {"message": "user deleted successfully!"}, 200

    return {"message": "Error while delete user"}, 400


@app.route("/medicamento", methods=["POST"])
# @jwt_required()
def create_medication():

    medication = Medication.find_medication_by_name(nome=request.json["nome"])

    if medication:
        return {"message": "Medication already exists"}, 404

    new_medication = Medication(
        request.json["nome"],
        request.json["dosagem"],
        request.json["qt_medicamento"],
        request.json["obs_medicamento"],
        request.json["frequencia_diaria"],
        request.json["frequencia_horas"],
    )

    try:
        new_medication.save_to_db()
    except Exception as err:
        return {"menssage": f"Error while register new medication: {err}"}, 404

    return {"message": "medication registered succesfully!"}, 201


@app.route("/medicamento/<med_id>", methods=["GET"])
# @jwt_required()
def get_medication(med_id):
    medication = Medication.find_medication_by_id(med_id)

    if not medication:
        return {"message": "Medication not found!"}, 404

    return {
        "id": medication.id,
        "nome": medication.nome,
        "dosagem": medication.dosagem,
        "qt_medicamento": medication.qt_medicamento,
        "obs_medicamento": medication.obs_medicamento,
        "frequencia_diaria": medication.frequencia_diaria,
        "frequencia_horas": medication.frequencia_horas,
    }, 200


@app.route("/medicamento/<med_id>", methods=["PUT"])
# @jwt_required()
def update_medication(med_id):
    medication = Medication.find_medication_by_id(med_id)

    if not medication:
        return {"message": "Medication not found!"}, 404

    medication.nome = request.json["nome"]
    medication.dosagem = request.json["dosagem"]
    medication.qt_medicamento = request.json["qt_medicamento"]
    medication.obs_medicamento = request.json["obs_medicamento"]
    medication.frequencia_diaria = request.json["frequencia_diaria"]
    medication.frequencia_horas = request.json["frequencia_horas"]

    try:
        medication.save_to_db()
    except Exception as err:
        return {"mensagem": f"Erro ao atualizar medicamento: {err}"}, 400

    return {"message": "medication updated succesfully!"}, 200


@app.route("/medicamento/<med_id>", methods=["DELETE"])
# @jwt_required()
def delete_medication(med_id):
    medication = Medication.find_medication_by_id(med_id)

    if medication:
        medication.delete_from_db()
        return {"message": "medication deleted successfully!"}, 200

    return {"message": "Error while delete medication"}, 400


@app.route("/consulta", methods=["POST"])
# @jwt_required()
def create_appointment():

    appointment = Appointment.find_appointment_by_name(nome=request.json["nome"])

    if appointment:
        return {"message": "Appointment already exists"}, 404

    new_appointment = Appointment(
        request.json["nome"],
        request.json["descricao"],
        request.json["data"],
        request.json["horario"],
    )

    try:
        new_appointment.save_to_db()
    except Exception as err:
        return {"menssage": f"Error while register new appointment: {err}"}, 404

    return {"message": "appointment registered succesfully!"}, 201


@app.route("/consulta/<cons_id>", methods=["GET"])
# @jwt_required()
def get_appointment(cons_id):
    appointment = Appointment.find_appointment_by_id(cons_id)

    if not appointment:
        return {"message": "Appointment not found!"}, 404

    return {
        "id": appointment.id,
        "nome": appointment.nome,
        "descricao": appointment.descricao,
        "data": appointment.data,
        "horario": appointment.horario,
    }, 200


@app.route("/consulta/<cons_id>", methods=["PUT"])
# @jwt_required()
def update_appointment(cons_id):
    appointment = Appointment.find_appointment_by_id(cons_id)

    if not appointment:
        return {"message": "Appointment not found!"}, 404

    appointment.nome = request.json["nome"]
    appointment.descricao = request.json["descricao"]
    appointment.data = request.json["data"]
    appointment.horario = request.json["horario"]

    try:
        appointment.save_to_db()
    except Exception as err:
        return {"mensagem": f"Erro ao atualizar consulta: {err}"}, 400

    return {"message": "appointment updated succesfully!"}, 200


@app.route("/consulta/<cons_id>", methods=["DELETE"])
# @jwt_required()
def delete_appointment(cons_id):
    appointment = Appointment.find_appointment_by_id(cons_id)

    if appointment:
        appointment.delete_from_db()
        return {"message": "appointment deleted successfully!"}, 200

    return {"message": "Error while delete appointment"}, 400


@app.route("/exame", methods=["POST"])
# @jwt_required()
def create_exam():

    exam = Exam.find_exam_by_name(nome=request.json["nome"])

    if exam:
        return {"message": "Exam already exists"}, 404

    new_exam = Exam(
        request.json["nome"],
        request.json["descricao"],
        request.json["data"],
        request.json["horario"],
    )

    try:
        new_exam.save_to_db()
    except Exception as err:
        return {"menssage": f"Error while register new exam: {err}"}, 404

    return {"message": "exam registered succesfully!"}, 201


@app.route("/exame/<exame_id>", methods=["GET"])
# @jwt_required()
def get_exam(exame_id):
    exam = Exam.find_exam_by_id(exame_id)

    if not exam:
        return {"message": "Exam not found!"}, 404

    return {
        "id": exam.id,
        "nome": exam.nome,
        "descricao": exam.descricao,
        "data": exam.data,
        "horario": exam.horario,
    }, 200


@app.route("/exame/<exame_id>", methods=["PUT"])
# @jwt_required()
def update_exam(exame_id):
    exam = Exam.find_exam_by_id(exame_id)

    if not exam:
        return {"message": "Exam not found!"}, 404

    exam.nome = request.json["nome"]
    exam.descricao = request.json["descricao"]
    exam.data = request.json["data"]
    exam.horario = request.json["horario"]

    try:
        exam.save_to_db()
    except Exception as err:
        return {"mensagem": f"Erro ao atualizar exame: {err}"}, 400

    return {"message": "exam updated succesfully!"}, 200


@app.route("/exame/<exame_id>", methods=["DELETE"])
# @jwt_required()
def delete_exam(exame_id):
    exam = Exam.find_exam_by_id(exame_id)

    if exam:
        exam.delete_from_db()
        return {"message": "exam deleted successfully!"}, 200

    return {"message": "Error while delete exam"}, 400
