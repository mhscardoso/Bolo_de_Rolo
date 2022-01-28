from app.user.model import User
from flask import request, jsonify, render_template
from flask.views import MethodView
from flask_mail import Message
from app.extensions import mail, jwt
from flask_jwt_extended import create_access_token, jwt_required

import bcrypt

class UserG(MethodView): #/user
    def post(self):
        body = request.json

        nome = body.get("nome")
        email = body.get("email")
        cpf = body.get("cpf")
        tel = body.get("tel")
        endereco = body.get("endereco")
        password = body.get("password")

        # Verificando dados
        if not (isinstance(nome, str) and isinstance(email, str) and isinstance(cpf, str) and isinstance(tel, str) and isinstance(endereco, str) and isinstance(password, str)):
            return {"code_status": "Invalid data in request"}, 400
        
        # Checando email
        user = User.query.filter_by(email=email).first()
        if user:
            return {"code_status": "User already exists"}, 400
        # Checando CPF
        user = User.query.filter_by(cpf=cpf).first()
        if user:
            return {"code_status": "User already exists"}, 400
        
        # Inserindo usuario

        hash_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        user = User(nome=nome, email=email, cpf=cpf, tel=tel, endereco=endereco, hash_pass=hash_pass)
        user.save()

        msg = Message(
            sender = "mhcardoso@poli.ufrj.br",
            recipients=[email],
            subject="Êta, seja bem-vindo à nossa loja",
            html = render_template("email.html", nome = nome)
        )

        mail.send(msg)

        return user.json(), 200
    
    def get(self):
        users = User.query.all()
        return jsonify([user.json() for user in users]), 200


class UserId(MethodView): #/user/id
    decorators = [jwt_required()]
    def get(self, id):
        user = User.query.get_or_404(id)
        return user.json()

    def put(self, id):
        body = request.json

        nome = body.get("nome")
        email = body.get("email")
        cpf = body.get("cpf")
        tel = body.get("tel")
        endereco = body.get("endereco")
        hash_pass = body.get("hash_pass")

        # Chacando dados
        if not (isinstance(nome, str) and isinstance(email, str) and isinstance(cpf, str) and isinstance(tel, str) and isinstance(endereco, str) and isinstance(hash_pass, str)):
            return {"code_status": "Invalid data in request"}, 400

        # Conferindo com a tabela
        user = User.query.filter_by(email=email).first()
        if user:
            if user.id != id:
                return {"code_status": "Email already in use"}, 400
        
        user = User.query.filter_by(cpf=cpf).first()
        if user:
            if user.id != id:
                return {"code_status": "Data already used"}, 400
        
        # Inserindo usuario
        user = User.query.get_or_404(id)
        user.nome = nome
        user.email = email
        user.cpf = cpf
        user.tel = tel
        user.endereco = endereco
        user.hash_pass = hash_pass
        user.update()
        return user.json(), 200


    def patch(self, id):
        body = request.json

        nome = body.get("nome", self.nome)
        email = body.get("email", self.email)
        cpf = body.get("cpf", self.cpf)
        tel = body.get("tel", self.tel)
        endereco = body.get("endereco", self.endereco)
        hash_pass = body.get("hash_pass", self.hash_pass)

        # Chacando dados
        if not (isinstance(nome, str) and isinstance(email, str) and isinstance(cpf, str) and isinstance(tel, str) and isinstance(endereco, str) and isinstance(hash_pass, str)):
            return {"code_status": "Invalid data in request"}, 400

        # Conferindo com a tabela
        user = User.query.filter_by(email=email).first()
        if user:
            if user.id != self.id:
                return {"code_status": "Email already in use"}, 400
        
        user = User.query.filter_by(cpf=cpf).first()
        if user:
            if user.id != self.id:
                return {"code_status": "Email already in use"}, 400
        
        # Inserindo usuario
        user = User.query.get_or_404(id)
        user.nome = nome
        user.email = email
        user.cpf = cpf
        user.tel = tel
        user.endereco = endereco
        user.hash_pass = hash_pass
        user.update()
        return user.json(), 200

    # Deleta usuario
    def delete(self, id):
        user = User.query.get_or_404(id)
        user.delete(user)
        return {"code_status": "deleted"}, 200



class UserLogin(MethodView): #/login
    def post(self):
        body = request.json

        email = body.get("email")
        password = body.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.hashpw(password.encode(), bcrypt.gensalt()):
            return {"error": "Invalid email or password"}
        
        token = create_access_token(identity=user.id)
        return {"token": token}, 200
