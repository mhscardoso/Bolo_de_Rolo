from app.produto.model import Produto
from flask import request, jsonify
from flask.views import MethodView

class ProdutoG(MethodView):
    def post(self):
        body = request.json

        nome = body.get("nome")
        sabor = body.get("sabor")
        cod = body.get("code")
        preco = body.get("preco")
        cart_id = body.get("cart_id")

        # Verificando dados
        if not (isinstance(nome, str) and isinstance(sabor, str) and isinstance(cod, str) and isinstance(preco, float) and isinstance(cart_id, int)):
            return {"code_status": "Invalid data in request"}, 400
        
        # Checando cod
        produto = Produto.query.filter_by(cod=cod).first()
        if produto:
            return {"code_status": "Produto already exists"}, 400        
        
        # Inserindo produto
        produto = Produto(nome=nome, sabor=sabor, cod=cod, preco=preco, cart_id=cart_id)
        produto.save()
        return produto.json(), 200
    
    def get(self):
        produtos = Produto.query.all()
        return jsonify([produto.json() for produto in produtos]), 200


class ProdutoId(MethodView):
    def get(self, id):
        produto = Produto.query.get_or_404(id)
        return produto.json()

    def put(self, id):
        body = request.json

        nome = body.get("nome")
        sabor = body.get("sabor")
        cod = body.get("code")
        preco = body.get("preco")
        pedido = body.get("pedido")
        cart_id = body.get("cart_id")

        # Verificando dados
        if not (isinstance(nome, str) and isinstance(sabor, str) and isinstance(cod, str) and isinstance(preco, float) and isinstance(cart_id, int)):
            return {"code_status": "Invalid data in request"}, 400
        
        # Checando cod
        produto = Produto.query.filter_by(cod=cod).first()
        if produto:
            if produto.id != id:
                return {"code_status": "Produto already exists"}, 400 
        
        # Modificando produto
        produto = Produto.query.get_or_404(id)
        produto.nome = nome
        produto.sabor = sabor
        produto.cod = cod
        produto.preco = preco
        produto.pedido = pedido
        produto.cart_id = cart_id
        produto.update()
        return produto.json(), 200


    def patch(self, id):
        body = request.json

        nome = body.get("nome", self.nome)
        sabor = body.get("sabor", self.sabor)
        cod = body.get("code", self.cod)
        preco = body.get("preco", self.preco)
        pedido = body.get("pedido", self.pedido)
        cart_id = body.get("cart_id", self.cart_id)

        # Verificando dados
        if not (isinstance(nome, str) and isinstance(sabor, str) and isinstance(cod, str) and isinstance(preco, float) and isinstance(cart_id, int)):
            return {"code_status": "Invalid data in request"}, 400
        
        # Checando cod
        produto = Produto.query.filter_by(cod=cod).first()
        if produto:
            if produto.id != self.id:
                return {"code_status": "Produto already exists"}, 400 
        
        # Modificando produto
        produto = Produto.query.get_or_404(id)
        produto.nome = nome
        produto.sabor = sabor
        produto.cod = cod
        produto.preco = preco
        produto.pedido = pedido
        produto.cart_id = cart_id
        produto.update()
        return Produto.json(), 200

    # Deleta produto
    def delete(self, id):
        produto = Produto.query.get_or_404(id)
        produto.delete(produto)
        return {"code_status": "deleted"}, 200
