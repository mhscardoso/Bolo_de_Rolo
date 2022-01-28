from app.cart.model import Cart
from flask import request, jsonify
from flask.views import MethodView

class CartG(MethodView):
    def post(self):
        body = request.json

        user = body.get("user_id")

        # Verificando dados
        if not (isinstance(user, int)):
            return {"code_status": "Invalid data in request"}, 400
        
        # Checando cart
        cart = Cart.query.filter_by(user_id=user).first()
        if cart:
            return {"code_status": "Cart already exists"}, 400        
        
        # Inserindo cart
        cart = Cart(user_id = user)
        cart.save()
        return cart.json(), 200
    
    def get(self):
        carts = Cart.query.all()
        return jsonify([cart.json() for cart in carts]), 200


class CartId(MethodView):
    def get(self, id):
        cart = Cart.query.get_or_404(id)
        return cart.json()

    def put(self, id):
        body = request.json

        user = body.get("user_id")

        # Verificando dados
        if not (isinstance(user, int)):
            return {"code_status": "Invalid data in request"}, 400
        
        # Checando cart
        cart = Cart.query.filter_by(user_id=user).first()
        if cart:
            if cart.id != id:
                return {"code_status": "Cart already exists"}, 400  
        
        # Modificando cart
        cart = Cart.query.get_or_404(id)
        cart.user_id = user
        return cart.json(), 200


    def patch(self, id):
        body = request.json

        user = body.get("user_id", self.user_id)

        # Verificando dados
        if not (isinstance(user, int)):
            return {"code_status": "Invalid data in request"}, 400
        
        # Checando cart
        cart = Cart.query.filter_by(user_id=user).first()
        if cart:
            if cart.id != self.id:
                return {"code_status": "Cart already exists"}, 400 
        
        # Modifica cart
        cart = Cart.query.get_or_404(id)
        cart.user_id = user
        cart.update()
        return cart.json(), 200

    # Deleta cart
    def delete(self, id):
        cart = Cart.query.get_or_404(id)
        cart.delete(cart)
        return {"code_status": "deleted"}, 200