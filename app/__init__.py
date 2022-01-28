from re import A
from flask import Flask
from app.config import Config
from app.extensions import migrate, db, mail, jwt
from app.produto.routes import produto_api
from app.user.routes import user_api
from app.cart.routes import cart_api

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_api)
    app.register_blueprint(produto_api)
    app.register_blueprint(cart_api)

    return app