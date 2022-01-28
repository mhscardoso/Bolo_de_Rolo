from flask import Blueprint
from app.user.controller import UserG, UserId, UserLogin

user_api = Blueprint("user_api", __name__)

user_api.add_url_rule("/user", view_func=UserG.as_view("user_geral"), methods=["POST", "GET"])
user_api.add_url_rule("/user/<int:id>", view_func=UserId.as_view("user_ids"), methods=["GET", "PUT", "PATCH", "DELETE"])
user_api.add_url_rule("/login", view_func=UserLogin.as_view("user_login"), methods=["POST"])