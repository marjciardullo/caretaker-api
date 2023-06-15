import os
from flask import Flask, request, jsonify
from models.user import User
from models.medication import Medication
from models.appointment import Appointment
from models.exam import Exam
from models.reminder import Reminder
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from db import db
from flask_cors import CORS
import json

# mysql://USER:PASSWORD@HOST:PORT/DATABASE
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://localhost:3306/caretaker' #os.getenv("MYSQL_DATABASE")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = '5_!!^./2.$0|p68{9#*g?.(x,i$[w}fa' #os.getenv("JWT_SECRET")

jwt = JWTManager(app)
CORS(app)

@app.before_first_request
def create_tables():
	print("Creating database...")
	db.create_all()

# -------------------------------------------------------------------------------------------------------------------
# LOGIN / SIGN UP FLOW ----------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------

@app.route("/usuario/registrar", methods=["POST"])
def register():

	user_email = User.find_user_by_email(email=request.json["email"])
	user_username = User.find_user_by_username(username=request.json["username"])

	if user_email:
		return {"message": "Esse email já está sendo utilizado. Se você já tiver uma conta, use a opção de 'Entrar'."}, 404

	if user_username:
		return {"message": "Esse nome de usuário já está sendo utilizado. Escolha outro nome de usuário (você pode colocar números ou símbolos (@#$&*) para deixá-lo mais único."}, 404

	new_user = User(
		request.json["username"],
		'', # nome
		request.json["email"],
		request.json["senha"],
		'', # nascimento
	)

	try:
		new_user.save_to_db()
	except Exception as err:
		return {"message": f"Error while register new user: {err}"}, 404

	access_token = create_access_token(identity=new_user.email)
	response = {}
	response["access_token"] = access_token
	response["usuario"] = {
		"id": new_user.id,
		"username": new_user.username,
		"nome": new_user.nome,
		"email": new_user.email,
		"nascimento": new_user.nascimento,
		"senha": new_user.senha,
	}
	return response, 200


@app.route("/login", methods=["POST"])
def login():
	user = User.find_user_by_login(username=request.json["username"], password=request.json["password"])

	if user:
		access_token = create_access_token(identity=user.email)
		response = {}
		response["access_token"] = access_token
		response["usuario"] = {
			"id": user.id,
			"username": user.username,
			"nome": user.nome,
			"email": user.email,
			"nascimento": user.nascimento,
			"senha": user.senha,
		}
		return response, 200

	return {"message": "Please, sign in to your account!"}, 404

# -------------------------------------------------------------------------------------------------------------------
# USER ROUTES -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------

@app.route("/usuario/<user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
	user = User.find_user_by_id(user_id)

	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	user_username = User.find_user_by_username(request.json["username"])
	if user_username:
		riseErr = user.id != user_username.id
		if riseErr:
			return {"message": "Esse nome de usuário já está sendo usado por outra pessoa"}, 404

	user_email = User.find_user_by_email(request.json["email"])
	if user_email:
		riseErr = user.id != user_email.id
		if riseErr:
			return {"message": "Esse e-mail já está sendo usado por outra pessoa"}, 404

	user.username = request.json["username"]
	user.nome = request.json["nome"]
	user.email = request.json["email"]
	user.nascimento = request.json["nascimento"]

	if request.json["senha"] != "":
		user.senha = request.json["senha"]

	try:
		user.save_to_db()
	except Exception as err:
		return {"mensagem": f"Erro ao atualizar usuário: {err}"}, 400

	response = {}
	response["usuario"] = {
		"id": user.id,
		"username": user.username,
		"nome": user.nome,
		"email": user.email,
		"nascimento": user.nascimento,
	}
	return response, 200


@app.route("/usuario/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
	user = User.find_user_by_id(user_id)

	if not user:
		return {"message": "Usuário não encontrado"}, 404

	all_items = Medication.find_all(user_id) + Exam.find_all(user_id) + Appointment.find_all(user_id) + Reminder.find_all(user_id)
	for item in all_items:
		item.delete_from_db()

	try:
		user.delete_from_db()
	except:
		return {"message": "Error while deleting user"}, 400

	return {"message": "user deleted successfully!"}, 200

# -------------------------------------------------------------------------------------------------------------------
# POST ROUTES -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------

@app.route("/medicamento", methods=["POST"])
@jwt_required()
def create_medication():
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	new_medication = Medication(
		user.id,
		request.json["nome"],
		request.json["dosagem"],
		float(request.json["qt_medicamento"]),
		request.json["obs_medicamento"],
		int(request.json["frequencia_horas"]),
	)

	try:
		new_medication.save_to_db()
	except Exception as err:
		return {"message": f"Error while register new medication: {err}"}, 404

	return {"message": "medication registered succesfully!"}, 201

@app.route("/consulta", methods=["POST"])
@jwt_required()
def create_appointment():
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	new_appointment = Appointment(
		user.id,
		request.json["nome"],
		request.json["descricao"],
		request.json["data"],
		request.json["horario"],
	)

	try:
		new_appointment.save_to_db()
	except Exception as err:
		return {"message": f"Error while register new appointment: {err}"}, 404

	return {"message": "appointment registered succesfully!"}, 201

@app.route("/exame", methods=["POST"])
@jwt_required()
def create_exam():
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	new_exam = Exam(
		user.id,
		request.json["medico"],
		request.json["exame"],
		request.json["local"],
		request.json["data"],
		request.json["horario"],
	)

	try:
		new_exam.save_to_db()
	except Exception as err:
		return {"message": f"Error while register new exam: {err}"}, 404

	return {"message": "exam registered succesfully!"}, 201

@app.route("/lembrete", methods=["POST"])
@jwt_required()
def create_reminder():
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	new_reminder = Reminder(
		user.id,
		request.json["descricao"],
		request.json["data"],
		request.json["horario"],
	)

	try:
		new_reminder.save_to_db()
	except Exception as err:
		return {"message": f"Error while registering new reminder: {err}"}, 404

	return {"message": "medication registered succesfully!"}, 201

# -------------------------------------------------------------------------------------------------------------------
# PUT ROUTES --------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------

@app.route("/medicamento/<med_id>", methods=["PUT"])
@jwt_required()
def update_medication(med_id):
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	medication = Medication.find_medication_by_id(med_id)

	if not medication:
		return {"message": "Medicamento não encontrado!"}, 404

	if not medication.usuario_id == user.id:
		return {"message": "Você não pode alterar essa informação!"}, 403

	medication.nome = request.json["nome"]
	medication.dosagem = request.json["dosagem"]
	medication.qt_medicamento = request.json["qt_medicamento"]
	medication.obs_medicamento = request.json["obs_medicamento"]
	medication.frequencia_horas = request.json["frequencia_horas"]

	try:
		medication.save_to_db()
	except Exception as err:
		return {"mensagem": f"Erro ao atualizar medicamento: {err}"}, 400

	return {"message": "medication updated succesfully!"}, 200


@app.route("/consulta/<cons_id>", methods=["PUT"])
@jwt_required()
def update_appointment(cons_id):
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	appointment = Appointment.find_appointment_by_id(cons_id)

	if not appointment:
		return {"message": "Consulta não encontrada!"}, 404

	if not appointment.usuario_id == user.id:
		return {"message": "Você não pode alterar essa informação!"}, 403

	appointment.nome = request.json["nome"]
	appointment.descricao = request.json["descricao"]
	appointment.data = request.json["data"]
	appointment.horario = request.json["horario"]

	try:
		appointment.save_to_db()
	except Exception as err:
		return {"mensagem": f"Erro ao atualizar consulta: {err}"}, 400

	return {"message": "appointment updated succesfully!"}, 200


@app.route("/exame/<exame_id>", methods=["PUT"])
@jwt_required()
def update_exam(exame_id):
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	exam = Exam.find_exam_by_id(exame_id)

	if not exam:
		return {"message": "Exame não encontrado!"}, 404

	if not exam.usuario_id == user.id:
		return {"message": "Você não pode alterar essa informação!"}, 403

	exam.medico = request.json["medico"]
	exam.exame = request.json["exame"]
	exam.local = request.json["local"]
	exam.data = request.json["data"]
	exam.horario = request.json["horario"]

	try:
		exam.save_to_db()
	except Exception as err:
		return {"mensagem": f"Erro ao atualizar exame: {err}"}, 400

	return {"message": "exam updated succesfully!"}, 200


@app.route("/lembrete/<lemb_id>", methods=["PUT"])
@jwt_required()
def update_reminder(lemb_id):
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	reminder = Reminder.find_reminder_by_id(lemb_id)

	if not reminder:
		return {"message": "Lembrete não encontrado!"}, 404

	if not reminder.usuario_id == user.id:
		return {"message": "Você não pode alterar essa informação!"}, 403

	reminder.descricao = request.json["descricao"]
	reminder.data = request.json["data"]
	reminder.horario = request.json["horario"]

	try:
		reminder.save_to_db()
	except Exception as err:
		return {"mensagem": f"Erro ao atualizar lembrete: {err}"}, 400

	return {"message": "appointment updated succesfully!"}, 200

# -------------------------------------------------------------------------------------------------------------------
# DELETE ROUTES -----------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------

@app.route("/exame/<exame_id>", methods=["DELETE"])
@jwt_required()
def delete_exam(exame_id):
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	exam = Exam.find_exam_by_id(exame_id)

	if not exam.usuario_id == user.id:
		return {"message": "Você não pode deletar essa informação!"}, 403

	if exam:
		exam.delete_from_db()
		return {"message": "Exame deletado com sucesso!"}, 200

	return {"message": "Error while delete exam"}, 400

@app.route("/medicamento/<med_id>", methods=["DELETE"])
@jwt_required()
def delete_medication(med_id):
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	medication = Medication.find_medication_by_id(med_id)

	if not medication.usuario_id == user.id:
		return {"message": "Você não pode deletar essa informação!"}, 403

	if medication:
		medication.delete_from_db()
		return {"message": "Medication deleted successfully!"}, 200

	return {"message": "Error while delete medication"}, 400


@app.route("/consulta/<cons_id>", methods=["DELETE"])
@jwt_required()
def delete_appointment(cons_id):
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	appointment = Appointment.find_appointment_by_id(cons_id)

	if not appointment.usuario_id == user.id:
		return {"message": "Você não pode deletar essa informação!"}, 403

	if appointment:
		appointment.delete_from_db()
		return {"message": "appointment deleted successfully!"}, 200

	return {"message": "Error while delete appointment"}, 400


@app.route("/lembrete/<lemb_id>", methods=["DELETE"])
@jwt_required()
def delete_reminder(lemb_id):
	token_email = get_jwt_identity()
	user = User.find_user_by_email(email=token_email)
	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	reminder = Reminder.find_reminder_by_id(lemb_id)

	if not reminder.usuario_id == user.id:
		return {"message": "Você não pode deletar essa informação!"}, 403

	if reminder:
		reminder.delete_from_db()
		return {"message": "Reminder deleted successfully!"}, 200

	return {"message": "Error while delete reminder"}, 400


# -------------------------------------------------------------------------------------------------------------------
# GET ROUTES -----------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------

@app.route("/calendario/<user_id>", methods=["GET"])
@jwt_required()
def get_data(user_id):
	user = User.find_user_by_id(user_id)

	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	fetched_data = []
	medications = Medication.find_all(user_id)
	for m in medications:
		fetched_data.append({
			'usuario_id': m.usuario_id,
			'item_id': m.id,
			'titulo': m.nome,
			'frequencia': m.frequencia_horas,
			'descricao': m.obs_medicamento,
			'dose': m.dosagem,
			'qt_medicamento': m.qt_medicamento,
			'local': '',
			'data': '',
			'horario': '',
			'tipo': 'medicamento'
		})
	exams = Exam.find_all(user_id)
	for e in exams:
		fetched_data.append({
			'usuario_id': e.usuario_id,
			'item_id': e.id,
			'titulo': e.exame,
			'frequencia': '',
			'descricao': e.medico,
			'local': e.local,
			'data': e.data,
			'horario': e.horario,
			'tipo': 'exame'
		})
	appointments = Appointment.find_all(user_id)
	for a in appointments:
		fetched_data.append({
			'usuario_id': a.usuario_id,
			'item_id': a.id,
			'titulo': a.nome,
			'frequencia': '',
			'descricao': a.descricao,
			'local': '',
			'data': a.data,
			'horario': a.horario,
			'tipo': 'consulta'
		})
	reminders = Reminder.find_all(user_id)
	for r in reminders:
		fetched_data.append({
			'usuario_id': r.usuario_id,
			'item_id': r.id,
			'titulo': 'Lembrar',
			'frequencia': '',
			'descricao': r.descricao,
			'local': '',
			'data': a.data,
			'horario': a.horario,
			'tipo': 'lembrete'
		})

	return {"message": "success", "fetched_data": fetched_data}, 200

"""
@app.route("/usuario/<user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
	user = User.find_user_by_id(user_id)

	if not user:
		return {"message": "Usuário não encontrado!"}, 404

	return {
		"id": user.id,
		"username": user.username,
		"nome": user.nome,
		"email": user.email,
		"nascimento": user.nascimento,
	}, 200

@app.route("/medicamento/<med_id>", methods=["GET"])
# @jwt_required()
def get_medication(med_id):
	medication = Medication.find_medication_by_id(med_id)

	if not medication:
		return {"message": "Medication não encontrado!"}, 404

	return {
		"id": medication.id,
		"nome": medication.nome,
		"dosagem": medication.dosagem,
		"qt_medicamento": medication.qt_medicamento,
		"obs_medicamento": medication.obs_medicamento,
		"frequencia_horas": medication.frequencia_horas,
	}, 200

@app.route("/consulta/<cons_id>", methods=["GET"])
# @jwt_required()
def get_appointment(cons_id):
	appointment = Appointment.find_appointment_by_id(cons_id)

	if not appointment:
		return {"message": "Appointment não encontrado!"}, 404

	return {
		"id": appointment.id,
		"nome": appointment.nome,
		"descricao": appointment.descricao,
		"data": appointment.data,
		"horario": appointment.horario,
	}, 200

@app.route("/exame/<exame_id>", methods=["GET"])
# @jwt_required()
def get_exam(exame_id):
	exam = Exam.find_exam_by_id(exame_id)

	if not exam:
		return {"message": "Exam não encontrado!"}, 404

	return {
		"id": exam.id,
		"nome": exam.nome,
		"descricao": exam.descricao,
		"data": exam.data,
		"horario": exam.horario,
	}, 200
"""