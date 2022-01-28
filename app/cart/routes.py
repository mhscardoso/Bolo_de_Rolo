from flask import Blueprint
from app.cart.controller import CartG, CartId

cart_api = Blueprint("cart_api", __name__)

cart_api.add_url_rule("/cart", view_func=CartG.as_view("cart_geral"), methods=["POST", "GET"])
cart_api.add_url_rule("/cart/<int:id>", view_func=CartId.as_view("cart_id"), methods=["GET", "PUT", "PATCH", "DELETE"])